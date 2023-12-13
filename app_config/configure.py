from sanic import Sanic
from app_config.routes import route_add_text
from json import load
from database.mongodb.startup import initialize_database
from functions.filesystem_utils import environment_get


def read_config() -> dict:
    file_handler = open("app_config/settings.json", "r")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_application():
    app_name = environment_get("SERVICE_NAME")
    sanic_app = Sanic(app_name)
    sanic_app.config.update(
        read_config()
    )

    sanic_app.register_listener(initialize_database, "before_server_start")
    sanic_app.add_route(route_add_text, "/api/addtext", methods=["POST"], ctx_refsanic=sanic_app)
    # sanic_app.add_route(route_add_file, "/api/addfile", methods=["POST"])
    # sanic_app.add_route(route_remove_text, "/api/removetext", methods=["POST"])
    # sanic_app.add_route(route_register_website, "/api/registerwebsite", methods=["POST"])

    return sanic_app
