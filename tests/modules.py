urls = {
    "LOGIN": "/api/login",
    "REGISTRATION": "/api/registration",
    "REG_CODE_CHECK": "/api/registration/check_code",
    "REG_CODE_CREATE": "/api/admin/create_code"
}

registration_credentials = {
    "login": "gm",
    "password": "gem",
    "email": "gm@gmail.com",
    "registration_code": "code_1234"
}

login_credential = {
    "login": "gm",
    "password": "gem"
}


def api_url(path):
    return f"http://0.0.0.0:4000{path}"
