from fastapi import APIRouter

from db.connection import execute_query
from db.queries import (
    GET_ALL_HOUBLONS,
    GET_HOUBLON_BY_ID,
    GET_HOUBLONS_BY_NOM,
    GET_HOUBLONS_BY_SEXE,
    GET_HOUBLONS_CARTE,
    SEARCH_HOUBLONS,
)


router = APIRouter()


@router.get("/houblons")
def liste_houblons():
    return execute_query(GET_ALL_HOUBLONS)


@router.get("/carte")
def liste_carte():
    return execute_query(GET_HOUBLONS_CARTE)


@router.get("/males")
def males():
    return execute_query(GET_HOUBLONS_BY_SEXE, ("M",))


@router.get("/femelles")
def femelles():
    return execute_query(GET_HOUBLONS_BY_SEXE, ("F",))


@router.get("/houblon/{id}")
def houblon(id: int):
    rows = execute_query(GET_HOUBLON_BY_ID, (id,))

    return rows[0] if rows else {}


@router.get("/houblon/nom/{nom}")
def houblon_par_nom(nom: str):
    return execute_query(GET_HOUBLONS_BY_NOM, (nom,))


@router.get("/recherche/{texte}")
def recherche(texte: str):
    return execute_query(SEARCH_HOUBLONS, (f"%{texte}%",))
