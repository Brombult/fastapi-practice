import pytest
from fastapi.testclient import TestClient

from database import database, db_for_testing, models
from main import app
from security.oath import create_access_token
from tests.constants import TEST_USER, USERS


@pytest.fixture
def test_db_session():
    models.Base.metadata.create_all(bind=db_for_testing.engine)
    db = db_for_testing.TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=db_for_testing.engine)


@pytest.fixture
def client(test_db_session):
    app.dependency_overrides[database.get_db] = db_for_testing.override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}


@pytest.fixture
def create_new_user(client):
    def _create_new_user(user_data=None):
        if user_data is None:
            user_data = TEST_USER
        return client.post(USERS, json=user_data)

    return _create_new_user


@pytest.fixture
def token(create_new_user):
    new_user = create_new_user()
    user_id = new_user.json().get("id")
    return create_access_token(data={"user_id": user_id}), user_id


@pytest.fixture
def authorized_client(client, token):
    access_token, user_id = token
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    client.user_id = user_id
    return client


@pytest.fixture
def create_posts(create_new_user, test_db_session):
    def _create_posts(user_id=None):
        if user_id is None:
            user_id = create_new_user().json()["id"]

        posts_data = [
            {
                "title": "first title",
                "content": "first content",
                "user_id": user_id,
            },
            {
                "title": "2nd title",
                "content": "2nd content",
                "user_id": user_id,
            },
            {
                "title": "3rd title",
                "content": "3rd content",
                "user_id": user_id,
            },
            {
                "title": "3rd title",
                "content": "3rd content",
                "user_id": user_id,
            },
        ]
        post_list = list(map(lambda post: models.Post(**post), posts_data))
        test_db_session.add_all(post_list)
        test_db_session.commit()

        return test_db_session.query(models.Post).all()

    return _create_posts
