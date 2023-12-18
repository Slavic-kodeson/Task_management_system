from modules import api_url, login_credential, urls
import requests


def test_login():
    print(f"Login ", end="")
    response = requests.post(
        api_url(urls["LOGIN"]),
        json=login_credential
    )
    j_response = response.json()

    if response.status_code != 200:
        print(f"[BAD]:  {j_response}", end="")

    token = j_response["token"]
    session_id = j_response["session_id"]
    user_id = j_response["user_id"]

    assert response.status_code == 200
    assert len(j_response.keys()) == 4
    for k, v in j_response.items():
        assert isinstance(v, str)
        assert len(v) > 0

    print(f"[OK]:  {j_response}")

    return token, session_id, user_id
