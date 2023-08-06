from flask import Flask, request
from mindflow.db.objects.configurations import Configurations

from mindflow.input import Arguments, Command
from mindflow.settings import Settings
from mindflow.state import STATE

from mindflow.core.ask import ask

# from mindflow.commands.config import config
from mindflow.cli.new_click_cli.commands.delete import delete
from mindflow.cli.new_click_cli.commands.diff import diff
from mindflow.cli.new_click_cli.commands.index import index
from mindflow.cli.new_click_cli.commands.inspect import inspect
from mindflow.core.query import query


def trim_json(data: dict, keys: list) -> dict:
    return {key: data[key] for key in keys if key in data}


class API:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route("/ask", methods=["POST"])
        def ask_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["query", "return_prompt", "skip_clipboard"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            ask()

        @self.app.route("/config", methods=["POST"])
        def config_route():
            # Your implementation for Command.CONFIG
            pass

        @self.app.route("/delete", methods=["POST"])
        def delete_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]

            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            delete()

        @self.app.route("/diff", methods=["POST"])
        def diff_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["git_diff_args", "return_prompt", "skip_clipboard"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            diff()

        @self.app.route("/inspect", methods=["POST"])
        def inspect_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            inspect()

        @self.app.route("/query", methods=["POST"])
        def query_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = [
                "document_paths",
                "index",
                "query",
                "return_prompt",
                "skip_clipboard",
            ]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            query()

        @self.app.route("/refresh", methods=["POST"])
        def refresh_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths", "force"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            index()

        @self.app.route("/index", methods=["POST"])
        def index_route():
            params = request.get_json()
            arguments = params.get("arguments", {})
            keys_to_keep = ["document_paths"]
            arguments = trim_json(arguments, keys_to_keep)

            database = params.get("database", None)
            path = params.get("path", None)
            auth = params.get("auth", None)
            user_configurations = params.get("user_configurations", {})

            STATE.user_configurations = Configurations(
                user_configurations
            )
            STATE.settings = Settings.initialize(user_configurations)
            STATE.arguments = Arguments(arguments)
            STATE.command = Command.INDEX.value

            index()


api = API()
app = api.app
app.run()
