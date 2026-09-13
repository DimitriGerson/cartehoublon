INSERT INTO houblon (id, nom, variete, sexe)
VALUES
    (1, 'Cascade', 'Cascade', 'M'),
    (2, 'Centennial', 'Centennial', 'M'),
    (3, 'Saaz', 'Saaz', 'F'),
    (4, 'Hallertau', 'Hallertau', 'F');


INSERT INTO position
    (houblon_id, localite, site_naturel, latitude, longitude)
VALUES
    (1, 'Nantes', 1, 47.2184, -1.5536),
    (2, 'Rennes', 1, 48.1173, -1.6778),
    (3, 'Angers', 1, 47.4784, -0.5632),
    (4, 'Vannes', 1, 47.6587, -2.7600);


INSERT INTO relations (male_id, femelle_id, distance_km)
VALUES

-- Femelle 3 : isolée
(1, 3, 3.01),
(2, 3, 49.99),

-- Femelle 4 : très proche
(1, 4, 0.659),

-- Femelle 5 : exactement à la frontière 0.660
(1, 5, 0.660),

-- Femelle 6 : un mâle entre 0.660 et 2 km
(1, 6, 1.000),

-- Femelle 7 : deux mâles entre 0.660 et 2 km
(1, 7, 1.000),
(2, 7, 1.500),

-- Femelle 8 : exactement à 2 km
(1, 8, 2.000),

-- Femelle 9 : mâle intermédiaire
(1, 9, 2.500),

-- Femelle 10 : exactement à 3 km
(1, 10, 3.000);
