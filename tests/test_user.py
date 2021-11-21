from fastapi import status

from schemas import user
from tests.constants import USERS


def test_create_user(create_new_user):
    new_user = create_new_user()
    assert new_user.status_code == status.HTTP_201_CREATED
    created_user = user.UserResponse(**new_user.json())
    assert created_user.email == new_user.json().get("email")


def test_create_user_twice(client, create_new_user):
    resp1 = create_new_user()
    assert resp1.status_code == status.HTTP_201_CREATED
    resp2 = create_new_user()
    assert resp2.status_code == status.HTTP_409_CONFLICT
    assert f"User with email '{resp1.json().get('email')}' already exists" in resp2.text


def test_get_user(client, create_new_user):
    new_user = create_new_user()
    resp = client.get(f"{USERS}{new_user.json()['id']}")
    assert resp.json() == new_user.json()
