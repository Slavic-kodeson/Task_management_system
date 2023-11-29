from sanic import Sanic
from tasks.routes import route_add_file, route_add_text, route_remove_document


def get_application():
    sanic_app = Sanic("TaskManagerApi")

    sanic_app.add_route(route_add_file, "/api/addfile/", methods=["POST"], ctx_config_get=sanic_app.config.get)
    sanic_app.add_route(route_add_text, "/api/addtext/", methods=["POST"], ctx_config_get=sanic_app.config.get)
    sanic_app.add_route(route_remove_document, "/api/removedocument/", methods=["POST"], ctx_config_get=sanic_app.config.get)

    return sanic_app
