from fastapi.testclient import TestClient

from app import validations
from app.main import app


client = TestClient(app)


def test_docs_without_credentials():
    response = client.get("/docs")

    assert response.status_code == 401


def test_redoc_without_credentials():
    response = client.get("/redoc")

    assert response.status_code == 401


def test_openapi_without_credentials():
    response = client.get("/openapi.json")

    assert response.status_code == 401


def test_docs_with_valid_credentials(monkeypatch):
    monkeypatch.setattr(validations, "DOCS_USER", "admin")
    monkeypatch.setattr(validations, "DOCS_PASSWORD", "secret")

    response = client.get(
        "/docs",
        auth=("admin", "secret"),
    )

    assert response.status_code == 200
