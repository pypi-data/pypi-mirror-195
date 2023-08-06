import streamsync.serve
import argparse
import os
import logging
import shutil


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Run, edit or create a Streamsync app.")
    parser.add_argument("command", choices=[
                        "run", "edit", "create", "hello"])
    parser.add_argument(
        "path", nargs='?', help="Path to the app's folder", default="")
    parser.add_argument(
        "--port", help="The port on which to run the server.", default="3005")
    parser.add_argument(
        "--host", help="The host on which to run the server.")
    parser.add_argument(
        "--log-level")

    args = parser.parse_args()

    mode = None
    mode = args.command

    app_path = extract_app_path(args)

    if mode in ("edit", "run"):
        logging.info(f"Path: {app_path}")
        logging.info(f"Mode: { mode }")
        port = int(args.port)
        streamsync.serve.serve(app_path, mode=mode, port=port)
    elif mode in ("create"):
        create_app(app_path)


def create_app(app_path, template_name="default"):
    server_path = os.path.dirname(__file__)
    template_path = os.path.join(server_path, "app_templates", template_name)

    shutil.copytree(template_path, app_path, dirs_exist_ok=True)


def extract_app_path(args):
    is_path_absolute = os.path.isabs(args.path)
    if is_path_absolute:
        return args.path
    else:
        return os.path.join(os.getcwd(), args.path)


if __name__ == "__main__":
    main()
