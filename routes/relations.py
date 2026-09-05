from fastapi import APIRouter

from db.connection import execute_query
from db.queries import (
    GET_FEMELLES_ISOLEES,
    GET_FEMELLES_MALE_INTERMEDIAIRE,
    GET_FEMELLES_PROCHES,
    GET_FEMELLES_UNIQUE_MALE,
)


router = APIRouter()


@router.get("/femelles-isolees")
def femelles_isolees():
    return execute_query(GET_FEMELLES_ISOLEES)


@router.get("/femelles-proches")
def femelles_proches():
    return execute_query(GET_FEMELLES_PROCHES)


@router.get("/femelles-unique-male")
def femelles_unique_male():
    return execute_query(GET_FEMELLES_UNIQUE_MALE)


@router.get("/femelles-male-intermediaire")
def femelles_male_intermediaire():
    return execute_query(GET_FEMELLES_MALE_INTERMEDIAIRE)
