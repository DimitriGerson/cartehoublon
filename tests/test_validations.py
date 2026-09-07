import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from app import validations


@pytest.fixture
def docs_credentials(monkeypatch):
    monkeypatch.setattr(validations, "DOCS_USER", "admin")
    monkeypatch.setattr(validations, "DOCS_PASSWORD", "secret")

    return HTTPBasicCredentials(
        username="admin",
        password="secret",
    )


def test_verify_docs_valid_credentials(docs_credentials):
    result = validations.verify_docs(docs_credentials)

    assert result == "admin"


def test_verify_docs_invalid_username(docs_credentials):
    credentials = HTTPBasicCredentials(
        username="mauvais_utilisateur",
        password="secret",
    )

    with pytest.raises(HTTPException) as exc_info:
        validations.verify_docs(credentials)

    assert exc_info.value.status_code == 401


def test_verify_docs_invalid_password(docs_credentials):
    credentials = HTTPBasicCredentials(
        username="admin",
        password="mauvais_mot_de_passe",
    )

    with pytest.raises(HTTPException) as exc_info:
        validations.verify_docs(credentials)

    assert exc_info.value.status_code == 401

def test_verify_docs_not_configured(monkeypatch):
    monkeypatch.setattr(validations, "DOCS_USER", None)
    monkeypatch.setattr(validations, "DOCS_PASSWORD", None)

    credentials = HTTPBasicCredentials(
        username="admin",
        password="secret",
    )

    with pytest.raises(HTTPException) as exc_info:
        validations.verify_docs(credentials)

    assert exc_info.value.status_code == 503
