import pytest
from fastapi.testclient import TestClient

from database import database, db_for_testing, models
from main import app


@pytest.fixture(scope="session")
def client():
    """Creates and drops test db and returns test client"""
    models.Base.metadata.create_all(bind=db_for_testing.engine)
    app.dependency_overrides[database.get_db] = db_for_testing.override_get_db
    yield TestClient(app)
    models.Base.metadata.drop_all(bind=db_for_testing.engine)
    app.dependency_overrides = {}
