from sanic import exceptions, response


def raise_error(message, exception_object) -> None:
    raise exception_object(message)


def json_response(status: int, description=None, **kwargs):
    return response.json({"description": description, **kwargs}, status=status)
