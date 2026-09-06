from fastapi.security import HTTPBasicCredentials

from app.validations import verify_docs


def test_verify_docs_valid_credentials():
    credentials = HTTPBasicCredentials(
        username="admin",
        password="secret",
    )

    # Pour ce premier test, on utilise les valeurs du module
    import app.validations as validations

    validations.DOCS_USER = "admin"
    validations.DOCS_PASSWORD = "secret"

    result = verify_docs(credentials)

    assert result == "admin"
