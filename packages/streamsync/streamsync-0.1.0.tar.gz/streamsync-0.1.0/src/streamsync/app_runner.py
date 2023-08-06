import inspect
from multiprocessing import Event, Pipe, Process
from multiprocessing.connection import Connection
import importlib
import os
import sys
from types import FunctionType, ModuleType
import json
from typing import Dict
import watchdog.observers
import watchdog.events


class AppProcess(Process):

    """
    Streamsync runs the user's app code using an isolated process, based on this class.
    The main process is able to communicate with the user app process via app messages (e.g. event, componentUpdate).
    """

    def __init__(self, parent_conn: Connection, app_conn: Connection, app_path: str, mode: str, run_code: str, components: Dict, is_ready: Event):
        super().__init__()
        self.parent_conn = parent_conn
        self.app_conn = app_conn
        self.app_path = app_path
        self.mode = mode
        self.run_code = run_code
        self.components = components
        self.is_ready = is_ready

    def load_module(self):
        """
        Loads the entry point for the user code in module streamsyncuserapp.
        """

        module_name = "streamsyncuserapp"
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module: ModuleType = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        globals()[module_name] = module
        return module

    def get_user_functions(self):
        """
        Returns functions exposed in the user code module, which are potential event handlers.
        """

        import streamsyncuserapp
        return list(
            map(lambda x: x[0], inspect.getmembers(
                streamsyncuserapp, inspect.isfunction))
        )

    def handle_session_init(self):
        """
        Handles session initialisation and provides a starter pack.
        """

        import streamsync
        from streamsync.sessions import session_manager
        import traceback as tb

        session = session_manager.get_new_session()
        payload = {"userState": {}}
        payload["sessionId"] = session.session_id

        try:
            payload["userState"] = session.session_state.user_state.to_dict()
        except BaseException:
            session.session_state.add_log_entry(
                "error", "Serialisation error", tb.format_exc())

        payload["mail"] = session.session_state.mail
        session.session_state.clear_mail()
        payload["components"] = streamsync.component_manager.to_dict()
        payload["userFunctions"] = self.get_user_functions()
        return payload

    def handle_message(self, session_id, message):
        """
        Handles messages from the main process to the app's isolated process.
        """

        import streamsync
        from streamsync.sessions import session_manager

        session = None
        type = message.get("type")
        payload = message.get("payload")
        response = {
            "status": "error"
        }

        if type == "sessionInit":
            response["payload"] = self.handle_session_init()
            response["status"] = "ok"
            return response
        elif type == "checkSession":
            session = session_manager.get_session(session_id)
            if session:
                response["status"] = "ok"
            return response

        session = session_manager.get_session(session_id)
        if not session:
            return response
        session.update_last_active_timestamp()

        if type == "event":
            response["payload"] = session.event_handler.handle(payload)
            response["status"] = "ok"
            response["mutations"] = session.session_state.user_state.mutations_as_dict()
            response["mail"] = session.session_state.mail
            session.session_state.clear_mail()
            return response

        if self.mode == "edit" and type == "componentUpdate":
            streamsync.component_manager.ingest(payload)
            response["status"] = "ok"
            return response

    def execute_user_code(self):
        """
        Executes the user code and captures standard output.
        """

        import streamsync
        from contextlib import redirect_stdout
        import io
        import streamsyncuserapp

        with redirect_stdout(io.StringIO()) as f:
            exec(self.run_code, streamsyncuserapp.__dict__)
        captured_stdout = f.getvalue()

        if captured_stdout:
            streamsync.initial_state.add_log_entry(
                "info", "Stdout message during initialisation", captured_stdout)

    def apply_configuration(self):
        import streamsync

        if self.mode == "edit":
            streamsync.Config.is_mail_enabled_for_log = True
        elif self.mode == "run":
            streamsync.Config.is_mail_enabled_for_log = False

    def main(self):
        self.apply_configuration()
        import os
        os.chdir(self.app_path)
        self.load_module()
        # Allows for relative imports from the app's path
        sys.path.append(self.app_path)
        import streamsync
        import traceback as tb
        import signal
        import threading

        try:
            self.execute_user_code()
        except BaseException:
            # Initialisation errors will be sent to all sessions via mail during session initialisation

            streamsync.initial_state.add_log_entry(
                "error", "Code Error", "Couldn't execute code. An exception was raised.", tb.format_exc())

        try:
            streamsync.component_manager.ingest(self.components)
        except BaseException:
            streamsync.initial_state.add_log_entry(
                "error", "UI Components Error", "Couldn't load components. An exception was raised.", tb.format_exc())

        self.is_ready.set()

        def signal_handler(sig, frame):
            self.app_conn.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        is_prune_terminated = threading.Event()
        session_pruner = threading.Thread(
            target=self.prune_sessions, args=(is_prune_terminated,))
        session_pruner.daemon = True
        session_pruner.start()

        while True:  # Starts app message server
            (session_id, message) = self.app_conn.recv()
            if message is None:  # An empty message terminates the process
                is_prune_terminated.set()
                session_pruner.join()
                return
            response = self.handle_message(session_id, message)
            self.app_conn.send((session_id, response))

    def prune_sessions(self, is_prune_terminated):
        from streamsync.sessions import session_manager
        PRUNE_SESSIONS_INTERVAL_SECONDS = 60
        while True:
            is_prune_terminated.wait(timeout=PRUNE_SESSIONS_INTERVAL_SECONDS)
            if is_prune_terminated.is_set():
                return
            session_manager.prune_sessions()

    def run(self):
        try:
            self.parent_conn.close()
            self.main()
        except BaseException:
            raise


class FileEventHandler(watchdog.events.PatternMatchingEventHandler):

    def __init__(self, update_callback: FunctionType):
        self.update_callback = update_callback
        super().__init__(patterns=["*.py", "assets/*.*"], ignore_patterns=[
            ".*"], ignore_directories=False, case_sensitive=False)

    def on_any_event(self, event):
        if event.event_type == "closed":
            return
        self.update_callback()


class AppRunner:

    """
    Starts a given user app in a separate process.
    Manages changes to the app.
    Allows for communication with the app via messages.
    """

    def __init__(self, app_path: str, mode: str):
        self.app_conn = None
        self.parent_conn = None
        self.app_process = None
        self.saved_code = None
        self.run_code = None
        self.components = None
        self.is_ready = Event()
        self.run_code_version = 0
        self.observer = None
        self.app_path = app_path

        if mode not in ("edit", "run"):
            raise ValueError("Invalid mode.")

        self.mode = mode

    def load(self):
        self.saved_code = self._load_persisted_script()
        self.run_code = self.saved_code
        self.components = self._load_persisted_components()

        if self.mode == "edit":
            self.observer = watchdog.observers.Observer()
            self.observer.schedule(
                FileEventHandler(self.reload_code_from_saved), path=self.app_path, recursive=True)
            self.observer.start()

        self._start_app_process()

    def get_run_code_version(self):
        return self.run_code_version

    def dispatch_message(self, session_id, message):
        self.parent_conn.send((session_id, message))
        (response_session_id, response) = self.parent_conn.recv()

        # Guardrail to protect against pipe issues

        if (session_id != response_session_id):
            raise PermissionError("Session mismatch.")

        return response

    def _load_persisted_script(self):
        with open(os.path.join(self.app_path, "main.py"), "r") as f:
            return f.read()

    def _load_persisted_components(self):
        with open(os.path.join(self.app_path, "ui.json"), "r") as f:
            return json.load(f)

    def check_session(self, session_id):
        response = self.dispatch_message(session_id, {
            "type": "checkSession"
        })
        is_ok = response["status"] == "ok"
        return is_ok

    def update_components(self, session_id, components):
        if self.mode != "edit":
            return

        self.components = components

        with open(os.path.join(self.app_path, "ui.json"), "w") as f:
            json.dump(components, f, indent=4)

        return self.dispatch_message(session_id, {
            "type": "componentUpdate",
            "payload": components
        })

    def save_code(self, session_id: str, saved_code: str):
        if self.mode != "edit":
            return

        with open(os.path.join(self.app_path, "main.py"), "w") as f:
            f.write(saved_code)
        self.saved_code = saved_code

    def _clean_process(self):
        # Terminate by sending empty message
        self.parent_conn.send((None, None))
        self.app_process.join()
        self.app_process.close()
        self.parent_conn.close()
        self.app_conn.close()

    def shut_down(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
        if self.app_process is not None:
            self._clean_process()

    def _start_app_process(self):
        self.is_ready.clear()
        self.parent_conn, self.app_conn = Pipe(duplex=True)
        self.app_process = AppProcess(
            parent_conn=self.parent_conn,
            app_conn=self.app_conn,
            app_path=self.app_path,
            mode=self.mode,
            run_code=self.run_code,
            components=self.components,
            is_ready=self.is_ready)
        self.app_process.start()

    def reload_code_from_saved(self):
        if not self.is_ready.is_set():
            return
        self.saved_code = self._load_persisted_script()
        self.update_code(None, self.saved_code)

    def update_code(self, session_id: str, run_code: str):
        if self.mode != "edit":
            return

        self.run_code = run_code
        self._clean_process()
        self._start_app_process()
        self.is_ready.wait()
        self.run_code_version += 1
