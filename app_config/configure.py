from sanic import Sanic
from app_config.routes import route_add_text, route_add_file, route_remove_text, route_register_website
from json import load


def read_config() -> dict:
    file_handler = open("app_config/settings.json", "r")
    server_config = load(file_handler)
    file_handler.close()
    return server_config


def get_application():
    sanic_app = Sanic("TaskManagerAPI")
    sanic_app.config.update(
        read_config()
    )

    sanic_app.add_route(route_add_text, "/api/addtext", methods=["POST"])
    sanic_app.add_route(route_add_file, "/api/addfile", methods=["POST"])
    sanic_app.add_route(route_remove_text, "/api/removetext", methods=["POST"])
    sanic_app.add_route(route_register_website, "/api/registerwebsite", methods=["POST"])

    return sanic_app
