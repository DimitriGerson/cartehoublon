import os
import secrets
import sqlite3
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

# Configuration

BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "Houblon.db"

DOCS_USER = os.environ.get("DOCS_USER")
DOCS_PASSWORD = os.environ.get("DOCS_PASSWORD")

# Application FastAPI

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Authentification Swagger / Redoc

security = HTTPBasic()

def verify_docs(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Vérifie les identifiants permettant d'accéder
    à Swagger, Redoc et OpenAPI.
    """

    # Si les variables ne sont pas configurées,
    # on refuse l'accès.
    if not DOCS_USER or not DOCS_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Documentation non configurée."
        )

    correct_username = secrets.compare_digest(
        credentials.username,
        DOCS_USER
    )

    correct_password = secrets.compare_digest(
        credentials.password,
        DOCS_PASSWORD
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

# Documentation Swagger protégée

@app.get("/docs", include_in_schema=False)
def protected_docs(
    credentials: HTTPBasicCredentials = Depends(verify_docs)
):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Carte Houblon - Swagger"
    )

#Documentation ReDoc protégée

@app.get("/redoc", include_in_schema=False)
def protected_redoc(
    credentials: HTTPBasicCredentials = Depends(verify_docs)
):
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Carte Houblon - ReDoc"
    )

#OpenAPI JSON protégé

@app.get("/openapi.json", include_in_schema=False)
def protected_openapi(
    credentials: HTTPBasicCredentials = Depends(verify_docs)
):
    return JSONResponse(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
    )

# Fichiers statiques

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/houblons")
def liste_houblons():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon;
    """)

    rows = [dict(r) for r in cur.fetchall()]

    conn.close()

    return rows

@app.get("/carte")
def liste_carte():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT
            h.id,
            h.nom,
            h.sexe,
            p.latitude,
            p.longitude
        FROM houblon h
        INNER JOIN position p
            ON h.id = p.houblon_id;
    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data

@app.get("/males")
def males():
    
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon
        WHERE sexe='M'
    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data

@app.get("/femelles")
def femelles():

    conn =sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon
        WHERE sexe='F'
    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data
@app.get("/houblon/{id}")
def houblon(id: int):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon
        WHERE id=?
    """, (id,))

    row = cur.fetchone()

    conn.close()
    
    return dict(row) if row else {}

@app.get("/houblon/nom/{nom}")
def houblon_par_nom(nom: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon
        WHERE nom = ?
    """, (nom,))

    rows = [dict(r) for r in cur.fetchall()]

    conn.close()

    return rows

@app.get("/recherche/{texte}")
def recherche(texte: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM houblon
        WHERE nom LIKE ?
    """, (f"%{texte}%",))

    rows = [dict(r) for r in cur.fetchall()]

    conn.close()

    return rows
@app.get("/femelles-isolees")
def femelles_isolees():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT femelle_id
        FROM relations
        GROUP BY femelle_id
        HAVING MIN(distance_km) > 3
        AND MAX(distance_km) < 50
   """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data
@app.get("/femelles-proches")
def femelles_proches():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT femelle_id
        FROM relations
        GROUP BY femelle_id
        HAVING MIN(distance_km) < 0.660
        OR COUNT(DISTINCT CASE WHEN distance_km < 2.0 THEN male_id END) >=2;
    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data

@app.get("/femelles-unique-male")
def femelles_unique_male():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING
        COUNT(DISTINCT CASE
            WHEN distance_km >= 0.660 AND distance_km <2.0
            THEN male_id
        END) =1
    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return data

@app.get("/femelles-male-intermediaire")
def femelles_male_intermediaire():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING MIN(distance_km) >=2.0
        AND MIN(distance_km) < 3.0;
    """)

    data = [dict(r) for r in  cur.fetchall()]

    conn.close()

    return data
