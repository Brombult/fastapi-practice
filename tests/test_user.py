from fastapi import status

from schemas import user

USERS = "/users/"


def test_create_user(client):
    new_user = {"email": "test@gmail.com", "password": "password1234"}
    resp = client.post(USERS, json=new_user)
    assert resp.status_code == status.HTTP_201_CREATED
    created_user = user.UserResponse(**resp.json())
    assert created_user.email == new_user.get("email")
