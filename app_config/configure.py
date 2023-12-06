from sanic import Sanic
from app_config.routes import route_add_text, route_add_file, route_remove_text
from json import load


def read_config() -> dict:
    file_handler = open("app_config/settings.json")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_application():
    sanic_app = Sanic("TaskManagerAPI")
    sanic_app.config.update(
        read_config()
    )
    sanic_app.add_route(route_add_text, "/api/addtext/", methods=["POST"], ctx_config_get=sanic_app.config.get)
    sanic_app.add_route(route_add_file, "api/addfile/", methods=["POST"], ctx_config_get=sanic_app.config.get)
    sanic_app.add_route(route_remove_text, "api/removetext/", methods=["POST"], ctx_config_get=sanic_app.config.get)

    return sanic_app
