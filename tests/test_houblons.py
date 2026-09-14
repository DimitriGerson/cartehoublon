from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liste_houblons():
    response = client.get("/houblons")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_liste_carte():
    response = client.get("/carte")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_males():
    response = client.get("/males")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for houblon in response.json():
        assert houblon["sexe"] == "M"


def test_femelles():
    response = client.get("/femelles")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for houblon in response.json():
        assert houblon["sexe"] == "F"


def test_houblon_par_id_existant():
    response = client.get("/houblon/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["id"] == 1


def test_houblon_par_id_inexistant():
    response = client.get("/houblon/999999")

    assert response.status_code == 200
    assert response.json() == {}


def test_houblon_par_nom():
    # À adapter avec un nom réellement présent dans seed.sql.
    response = client.get("/houblon/nom/Cascade")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_recherche():
    # À adapter avec une partie d'un nom réellement présent dans seed.sql.
    response = client.get("/recherche/Cas")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

