import pytest
from fastapi.testclient import TestClient

from database import database, db_for_testing, models
from main import app
from tests.constants import USERS, TEST_USER


@pytest.fixture
def db():
    models.Base.metadata.create_all(bind=db_for_testing.engine)
    yield
    models.Base.metadata.drop_all(bind=db_for_testing.engine)


@pytest.fixture
def client(db):
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
