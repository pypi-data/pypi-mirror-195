import asyncio
from typing import Dict, List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocket, WebSocketDisconnect
from streamsync.types import StreamsyncWebsocketIncoming, StreamsyncWebsocketOutgoing
import os
import uvicorn
from streamsync.app_runner import AppRunner
import logging

user_app_path = None
asgi_app = FastAPI()
app_runner: AppRunner = None
serve_mode = None


@asgi_app.get("/api/init")
async def init():

    """
    Handles session init and provides a "starter pack" to the frontend.
    """

    response = app_runner.dispatch_message(None,
                                           {"type": "sessionInit"})
    payload = response["payload"]

    session_id: str = payload["sessionId"]
    user_state: Dict = payload["userState"]
    mail: List[Dict] = payload["mail"]  # TODO needs filtering
    components: Dict = payload["components"]

    if serve_mode == "run":
        return {
            "mode": "run",
            "sessionId": session_id,
            "userState": user_state,
            "mail": mail,
            "components": components,
        }

    if serve_mode == "edit":
        saved_code: str = app_runner.saved_code
        run_code: str = app_runner.run_code
        user_functions: List[str] = payload["userFunctions"]

        return {
            "mode": "edit",
            "sessionId": session_id,
            "userState": user_state,
            "mail": mail,
            "components": components,
            "userFunctions": user_functions,
            "savedCode": saved_code,
            "runCode": run_code
        }


async def stream_session_init(websocket: WebSocket):
    message: StreamsyncWebsocketIncoming
    session_id = None
    while session_id is None:
        try:
            message = await websocket.receive_json()
        except WebSocketDisconnect:
            return
        message_type = message["type"]
        if message_type == "streamInit":
            message_payload = message["payload"]
            session_id = message_payload["sessionId"]
    return session_id


async def stream_incoming_requests(websocket: WebSocket, session_id: str):
    message: StreamsyncWebsocketIncoming
    while True:
        try:
            message = await websocket.receive_json()
        except WebSocketDisconnect:
            return

        message_type = message["type"]
        message_payload = message["payload"]
        response: StreamsyncWebsocketOutgoing = {
            "messageType": f"{message_type}Response",
            "trackingId": message["trackingId"],
        }

        is_session_ok = app_runner.check_session(session_id)
        if not is_session_ok:
            await websocket.close(code=1000)
            return

        if message_type == "event":
            app_response = app_runner.dispatch_message(
                session_id, message)
            response["payload"] = app_response["payload"]
            response["mutations"] = app_response["mutations"]
            response["mail"] = app_response["mail"] # TODO needs filtering
        elif serve_mode == "edit" and message_type == "componentUpdate":
            response["payload"] = app_runner.update_components(
                session_id, message_payload["components"])
        elif serve_mode == "edit" and message_type == "codeSaveRequest":
            response["payload"] = app_runner.save_code(
                session_id, message_payload["code"])
        elif serve_mode == "edit" and message_type == "codeUpdate":
            response["payload"] = app_runner.update_code(
                session_id, message_payload["code"])

        try:
            await websocket.send_json(response)
        except (WebSocketDisconnect):
            return


async def stream_outgoing_announcements(websocket: WebSocket):
    from asyncio import sleep
    code_version = app_runner.get_run_code_version()
    while True:
        await sleep(1)
        current_code_version = app_runner.get_run_code_version()
        if code_version == current_code_version:
            continue
        code_version = current_code_version

        announcement: StreamsyncWebsocketOutgoing = {
            "messageType": "announcement",
            "trackingId": -1,
            "payload": {
                "announce": "codeUpdate"
            }
        }

        try:
            await websocket.send_json(announcement)
        except (WebSocketDisconnect):
            return


@asgi_app.websocket("/api/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    session_id = await stream_session_init(websocket)

    is_session_ok = app_runner.check_session(session_id)
    if not is_session_ok:
        await websocket.close(code=1008)  # Invalid permissions
        return

    task1 = asyncio.create_task(
        stream_incoming_requests(websocket, session_id))
    task2 = asyncio.create_task(stream_outgoing_announcements(websocket))

    await asyncio.wait((task1, task2), return_when=asyncio.FIRST_COMPLETED)
    task1.cancel()
    task2.cancel()

# def get_mail(state: StreamsyncState):
#     mail = state.mail
#     allowed_types = ["notification"]
#     if user_app.mode == "edit":
#         allowed_types.append("logEntry")
#     filtered_mail = list(filter(lambda x: x["type"] in allowed_types, mail))
#     return filtered_mail


@asgi_app.on_event("shutdown")
def shutdown_event():
    logging.info("Streamsync's app runner shutting down...")
    app_runner.shut_down()


def attach_static_paths(app_path):
    user_app_static_path = os.path.join(app_path, "static")
    asgi_app.mount(
        "/static", StaticFiles(directory=user_app_static_path), name="user_static")

    server_path = os.path.dirname(__file__)
    server_static_path = os.path.join(server_path, "static")
    asgi_app.mount(
        "/", StaticFiles(directory=server_static_path, html=True), name="server_static")


def serve(app_path: str, mode: str, port: int = 5000, host: str = "127.0.0.1"):
    global serve_mode, app_runner, user_app_path
    if mode not in ["run", "edit"]:
        raise ValueError("""Invalid mode. Must be either "run" or "edit".""")

    app_runner = AppRunner(app_path, mode)
    app_runner.load()
    serve_mode = mode

    attach_static_paths(app_path)
    uvicorn.run("streamsync.serve:asgi_app", host=host,
                port=port, log_level="info")
