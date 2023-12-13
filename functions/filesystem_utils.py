from os import environ, getcwd
from os.path import isfile, join


def environment_set(key: str, value: str):
    environ[key] = value


def convert_to_bool(value: str):
    if value is None:
        return value

    cpy_value = value.lower()

    if 'true' in cpy_value:
        return True
    if 'false' in cpy_value:
        return False

    return None


def environment_get(key: str, strict=True):
    value = environ.get(key)

    if value is None and strict:
        raise KeyError

    value_bool = convert_to_bool(value)
    if value_bool is not None:
        return value_bool

    return value


def exist_file(path, error_message, error_object) -> bool:
    if not isfile(path):
        raise error_object(error_message)
    return True


def create_path(additional_path="", filename="", main_path=None) -> str:
    return join(getcwd() or main_path, additional_path, filename)
