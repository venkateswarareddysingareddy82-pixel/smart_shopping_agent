import os, tempfile

_tmp = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp}/test.db"
os.environ["AI_API_KEY"] = ""
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-only-0123456789"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


def login(client, email, password):
    r = client.post("/api/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['token']}"}


@pytest.fixture(scope="session")
def user_h(client):
    return login(client, "user@example.com", "User@12345")


@pytest.fixture(scope="session")
def admin_h(client):
    return login(client, "admin@example.com", "Admin@12345")
