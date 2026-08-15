import sqlite3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

DB = "Houblon.db"

app.mount(
    "/static",
    StaticFiles(directory="static"),
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
