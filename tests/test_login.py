import pytest
from fastapi import status
from jose import jwt

from schemas.token import Token
from settings import settings
from tests.constants import LOGIN

NEW_USER = {"email": "testlogin@gmail.com", "password": "12345"}
PARAMS = [
    pytest.param(
        NEW_USER.get("email"),
        "wrong_pass",
        status.HTTP_403_FORBIDDEN,
        id="correct user, wrong password",
    ),
    pytest.param(
        "wrong_user",
        NEW_USER.get("password"),
        status.HTTP_403_FORBIDDEN,
        id="wrong user, correct password",
    ),
    pytest.param(
        None,
        NEW_USER.get("password"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        id="No user",
    ),
    pytest.param(
        NEW_USER.get("email"),
        None,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        id="No password",
    ),
]


def test_login(client, create_new_user):
    create_new_user(NEW_USER)
    login_data = {
        "username": NEW_USER.get("email"),
        "password": NEW_USER.get("password"),
    }
    resp = client.post(LOGIN, data=login_data)
    assert resp.status_code == status.HTTP_200_OK

    token = Token(**resp.json())
    assert token.token_type == "bearer"

    payload = jwt.decode(
        token.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    assert payload.get("id") == resp.json().get("id")


@pytest.mark.parametrize(["username", "password", "status_code"], PARAMS)
def test_login_negative(username, password, status_code, client, create_new_user):
    create_new_user(NEW_USER)

    resp = client.post(LOGIN, data={"username": username, "password": password})
    assert resp.status_code == status_code
