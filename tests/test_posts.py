from fastapi import status

from tests.constants import POSTS
from schemas.post import PostResponse, Post, PostBase


def test_get_all_posts(client, create_posts):
    created_posts = create_posts()
    resp = client.get(POSTS)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == len(created_posts)

    posts_schema = [PostResponse(**p) for p in resp.json()]
    for schema, post_resp in zip(posts_schema, resp.json()):
        assert schema.Post.id == post_resp["Post"]["id"]


def test_get_one_posts(client, create_posts):
    created_posts = create_posts()
    resp = client.get(POSTS + str(created_posts[0].id))
    assert resp.status_code == status.HTTP_200_OK


def test_get_non_existent_posts(client):
    resp = client.get(POSTS + "99999999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_create_post(authorized_client):
    data = {"title": "test title", "content": "test content"}
    resp = authorized_client.post(POSTS, json=data)
    assert resp.status_code == status.HTTP_201_CREATED

    post = Post(**resp.json())
    assert data["title"] == post.title
    assert data["content"] == post.content
    assert post.published is True


def test_create_post_not_authorized_client(client):
    resp = client.post(POSTS, json={"title": "test title", "content": "test content"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(authorized_client, create_posts):
    created_posts = create_posts(authorized_client.user_id)
    resp = authorized_client.delete(POSTS + str(created_posts[0].id))
    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_delete_non_existing_post(authorized_client):
    resp = authorized_client.delete(POSTS + "999999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post_not_authorized_client(client):
    resp = client.delete(POSTS + "1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_of_another_user(authorized_client, create_posts, create_new_user):
    second_user = create_new_user(
        {"email": "seconduser@gmail.com", "password": "second"}
    )
    created_posts = create_posts(second_user.json().get("id"))
    resp = authorized_client.delete(POSTS + str(created_posts[0].id))
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, create_posts):
    created_posts = create_posts(authorized_client.user_id)
    data = {"title": "updated", "content": "updated"}
    resp = authorized_client.put(POSTS + str(created_posts[0].id), json=data)
    assert resp.status_code == status.HTTP_200_OK

    post = PostBase(**resp.json())
    assert post.title == data["title"] and post.content == data["content"]


def test_update_post_of_another_user(authorized_client, create_posts, create_new_user):
    second_user = create_new_user(
        {"email": "seconduser@gmail.com", "password": "second"}
    )
    created_posts = create_posts(second_user.json().get("id"))
    resp = authorized_client.put(
        POSTS + str(created_posts[0].id),
        json={"title": "updated", "content": "updated"},
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_update_non_existing_post(authorized_client):
    resp = authorized_client.put(
        POSTS + "999999999",
        json={"title": "updated", "content": "updated"},
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND
