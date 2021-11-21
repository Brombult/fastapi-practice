import pytest
from fastapi import status

from database.models import Vote
from tests.constants import VOTE


@pytest.fixture
def vote_for_post(authorized_client, create_posts, test_db_session):
    user_id = authorized_client.user_id
    posts = create_posts(user_id)
    new_vote = Vote(post_id=posts[0].id, user_id=user_id)
    test_db_session.add(new_vote)
    test_db_session.commit()


def test_vote(authorized_client, create_posts):
    posts = create_posts(authorized_client.user_id)
    resp = authorized_client.post(VOTE, json={"post_id": posts[0].id, "direction": 1})
    assert resp.status_code == status.HTTP_201_CREATED
    assert "vote added successfully" in resp.text

    resp = authorized_client.post(VOTE, json={"post_id": posts[0].id, "direction": 0})
    assert resp.status_code == status.HTTP_201_CREATED
    assert "vote removed successfully" in resp.text


def test_vote_for_already_voted_post(authorized_client, create_posts, vote_for_post):
    user_id = authorized_client.user_id
    posts = create_posts(user_id)
    post_id = posts[0].id
    resp = authorized_client.post(VOTE, json={"post_id": post_id, "direction": 1})
    assert resp.status_code == status.HTTP_409_CONFLICT
    assert f"user {user_id} has already voted on post {post_id}" in resp.text


def test_vote_for_non_existent_post(authorized_client):
    resp = authorized_client.post(VOTE, json={"post_id": 9999999999999, "direction": 1})
    assert resp.status_code == status.HTTP_404_NOT_FOUND
