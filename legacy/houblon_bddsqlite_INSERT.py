import sqlite3
from datetime import datetime

DB ="Houblon.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

def IdHoublonParNom(cur, id):
    cur.execute(
        "SELECT id FROM houblon WHERE lower(nom) = lower(?)",
        (nom,)
    )
    resultat = cur.fetchone()

    return resultat[0] if resultat else None

while True:
    print("\n=== MENU ===")
    print("1 - Ajouter un houblon")
    print("2 - Ajouter un suivi")
    print("3 - Ajouter une position")
    print("4 - Quitter")

    choix = input("Choix : ")

    if choix == "1":
        nom = input("Nom : ")
        variete = input("Variété : ")
        date_str = input("Date (AAAA-MM-JJ) : ")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            dateDebut = date_obj.date().isoformat()
        except ValueError:
            print("Format invalide")
            exit()

        cur.execute(
            """
            INSERT INTO houblon (nom, variete, date_debut)
            VALUES (?, ?, ?)
            """,
            (nom, variete, dateDebut)
        )

        conn.commit()
        print("Houblon ajouté.")
    elif choix == "2":
        nom = input("Nom du houblon en miniscule : ")
        houblon_id = IdHoublonParNom(cur,nom)

        if houblon_id is None:
            print("houblon introuvable.")
        else: 
            date_obs = input("Date (AAAA-MM-JJ) : ")
            hauteur = int(input("Hauteur (cm) : "))
            commentaire = input("Commentaire : ")

            cur.execute(
            """
            INSERT INTO suivi
            (houblon_id, date_observation, hauteur_cm, commentaire)
            VALUES(?, ?, ?, ?)
            """,
            (houblon_id, date_obs, hauteur, commentaire)
            )

            conn.commit()
            print("Suivi ajouté")

    elif choix == "3":
        nom = input("Nom du houblon : ")
        houblon_id = IdHoublonParNom(cur,nom)

        if houblon_id is None:
            print("Houblon introuvable")
        else:
            latitude = input("Latitude : ")
            longitude = input("longitude : ")
            localite = input("Localité : ")
            cur.execute(
            """
            INSERT INTO position
            (houblon_id, latitude, longitude, localite)
            VALUES(?, ?, ?, ?)
            """,
            (houblon_id, latitude, longitude,localite)
            )

            conn.commit()
            print("Position ajoutée")
    elif choix == "4":
        break

    else:
        print("Choix invalide.")

conn.close()

