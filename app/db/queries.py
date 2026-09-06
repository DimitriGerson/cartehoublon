GET_ALL_HOUBLONS = """
    SELECT *
    FROM houblon;
"""


GET_HOUBLONS_CARTE = """
    SELECT
        h.id,
        h.nom,
        h.sexe,
        p.latitude,
        p.longitude
    FROM houblon h
    INNER JOIN position p
        ON h.id = p.houblon_id;
"""


GET_HOUBLONS_BY_SEXE = """
    SELECT *
    FROM houblon
    WHERE sexe = %s;
"""


GET_HOUBLON_BY_ID = """
    SELECT *
    FROM houblon
    WHERE id = %s;
"""


GET_HOUBLONS_BY_NOM = """
    SELECT *
    FROM houblon
    WHERE nom = %s;
"""


SEARCH_HOUBLONS = """
    SELECT *
    FROM houblon
    WHERE nom LIKE %s;
"""


GET_FEMELLES_ISOLEES = """
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING MIN(distance_km) > 3
       AND MAX(distance_km) < 50;
"""


GET_FEMELLES_PROCHES = """
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING MIN(distance_km) < 0.660
       OR COUNT(
            DISTINCT CASE
                WHEN distance_km < 2.0
                THEN male_id
            END
       ) >= 2;
"""


GET_FEMELLES_UNIQUE_MALE = """
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING COUNT(
        DISTINCT CASE
            WHEN distance_km >= 0.660
             AND distance_km < 2.0
            THEN male_id
        END
    ) = 1;
"""


GET_FEMELLES_MALE_INTERMEDIAIRE = """
    SELECT femelle_id
    FROM relations
    GROUP BY femelle_id
    HAVING MIN(distance_km) >= 2.0
       AND MIN(distance_km) < 3.0;
"""
