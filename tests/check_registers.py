from modules import api_url, urls
from test_login import test_login
import requests


def test_register_reg_code():
    print(f"Creation of Registration Link ", end="")

    token, session_id, user_id = test_login()

    response = requests.post(
        api_url(urls["REG_CODE_CREATE"]),
        json={
            "token": token,
            "session_id": session_id,
            "user_id": user_id,
            "role": "admin"
        }
    )

    j_response = response.json()

    if response.status_code != 200:
        print(f"[BAD]:  {j_response}")

    assert response.status_code == 200
    print(f"[OK]:  {j_response}")


def test_check_register_code():
    print(f"Check Code ", end="")
    response = requests.post(
        api_url(urls["REG_CODE_CHECK"]),
        json={
            "register_code": "code_1234"
        }
    )

    j_response = response.json()

    if response.status_code != 200:
        print(f"[BAD]:  {j_response}")

    assert response.status_code == 200
    assert "not" not in j_response.get("description")
    print(f"[OK]:  {j_response}")
