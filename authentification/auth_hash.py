from hashlib import sha256
from rapidjson import dumps


def generate_user_id(user: dict, get_user=False):
    convert = {k: v for k, v in user.items()}
    user_id = sha256(
        dumps({
            "login": convert.get("login"),
            "password": convert.get("password")
        }).encode()
    ).hexdigest()

    if get_user:
        convert["id"] = user_id
        convert["password"] = sha256(convert["password"].encode()).hexdigest()
        return user_id, convert
    return user_id


def _hash_auth(auth: str) -> str:
    return sha256(auth.encode()).hexdigest()
