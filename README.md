# 🗺️ Roadmap du projet

Ce projet est une application destinée à recenser et exploiter des observations de **houblons sauvages** dans une zone géographique donnée.

L'objectif est de construire progressivement une application réellement utilisable, en privilégiant une architecture simple, du code maintenable et une démarche de développement professionnelle.

---

## ✅ Déjà réalisé

* [x] Développement de l'API en **Python / FastAPI**
* [x] Mise en place d'une base de données **SQL**
* [x] Migration vers **PostgreSQL**
* [x] Mise en place de PostgreSQL dans **Docker** pour l'environnement local
* [x] Gestion de la configuration et des informations de connexion à la base de données
* [x] Première mise en production de l'application
* [x] Déploiement de l'application sur **Render**
* [x] Gestion du code avec **Git / GitHub**
* [x] Mise en place des **Pull Requests**
* [x] Validation du code avant déploiement
* [x] Mise en place d'un environnement de test permettant de valider les évolutions avant leur mise en production

---

## 🚧 En cours

### Refactorisation du backend

Le fichier initial `api_houblon.py` contient actuellement une partie importante de la logique de l'application.

L'objectif est de mieux séparer les responsabilités afin d'obtenir un code plus lisible et plus facile à maintenir.

* [x] Extraction de la connexion à la base de données
* [x] Séparation de la configuration et des informations sensibles
* [ ] Organisation des requêtes SQL
* [ ] Organisation des routes API
* [ ] Simplification et nettoyage du code existant

---

# 📋 Prochaines étapes

## 1. 🧪 Tests automatisés

Mettre en place une véritable suite de tests afin de sécuriser les évolutions de l'application.

* [ ] Mise en place de `pytest`
* [ ] Tests des endpoints FastAPI
* [ ] Tests des validations
* [ ] Tests des cas d'erreur
* [ ] Tests des accès à PostgreSQL
* [ ] Tests des cas limites
* [ ] Tests des futures fonctionnalités de calcul de distance

---

## 2. 🔄 CI / Qualité du code

Automatiser les contrôles lors des Pull Requests.

* [ ] Intégration des tests dans GitHub Actions
* [ ] Exécution automatique de `pytest`
* [ ] Intégration de **SonarQube**
* [ ] Analyse de la qualité du code
* [ ] Mise en place d'un Quality Gate
* [ ] Bloquer la validation d'une PR en cas d'échec des contrôles

Objectif :

```text
Pull Request
      ↓
   pytest
      ↓
  SonarQube
      ↓
 Quality Gate
      ↓
    Merge
```

---

## 3. 📖 Documentation

Créer une documentation permettant de comprendre rapidement le projet et de le reproduire.

* [x] Création de la roadmap
* [ ] Présentation détaillée du projet
* [ ] Documentation de l'architecture
* [ ] Documentation de l'installation locale
* [ ] Documentation de la configuration
* [ ] Documentation de l'API
* [ ] Documentation du déploiement
* [ ] Documentation des choix techniques
* [ ] Documentation du calcul des distances

---

## 4. 🗃️ Gestion des migrations avec Alembic

Mettre en place **Alembic** afin de versionner l'évolution du schéma PostgreSQL.

* [ ] Installation et configuration d'Alembic
* [ ] Création de la première migration
* [ ] Gestion des évolutions du schéma
* [ ] Intégration des migrations dans le processus de déploiement

Objectif :

```text
Code + migrations
        ↓
     PostgreSQL
```

La structure de la base de données pourra ainsi évoluer de manière contrôlée avec le code source.

---

## 5. 🌿 Fonctionnalités métier

Développer progressivement les fonctionnalités principales de l'application.

### CRUD des observations

* [ ] Création d'une observation
* [ ] Consultation d'une observation
* [ ] Modification d'une observation
* [ ] Suppression d'une observation
* [ ] Recherche et filtrage des observations

### Géolocalisation

* [ ] Recherche des observations dans un périmètre géographique
* [ ] Calcul des distances entre les observations
* [ ] Gestion des unités de distance
* [ ] Validation des résultats

### Analyse mâles / femelles

* [ ] Identification des plants mâles et femelles
* [ ] Calcul de la distance entre les plants
* [ ] Recherche des plants mâles proches des plants femelles
* [ ] Exploitation de ces informations dans l'application

Le principe et la méthode utilisés pour le calcul des distances seront documentés dans le README.

---

## 6. 🖥️ Évolution du client

Faire évoluer l'interface afin de permettre une meilleure exploitation des fonctionnalités de l'API.

* [ ] Amélioration de l'affichage des observations
* [ ] Utilisation du CRUD depuis le client
* [ ] Ajout / modification / suppression d'une observation
* [ ] Recherche géographique
* [ ] Amélioration de la présentation des informations
* [ ] Affichage des distances
* [ ] Amélioration de l'expérience utilisateur

---

## 7. 🐳 Dockerisation de l'application

Après stabilisation du backend et du client, conteneuriser l'ensemble de l'application.

* [ ] Dockeriser l'API FastAPI
* [ ] Finaliser l'utilisation de PostgreSQL avec Docker
* [ ] Créer un `docker-compose.yml`
* [ ] Tester l'ensemble de l'application dans un environnement Docker
* [ ] Documenter le lancement de l'application avec Docker

Objectif :

```text
┌───────────────────────────┐
│       Docker Compose      │
│                           │
│  ┌─────────┐ ┌─────────┐ │
│  │  API    │ │ Postgres│ │
│  │ FastAPI │ │         │ │
│  └─────────┘ └─────────┘ │
│                           │
└───────────────────────────┘
```

---

## 8. 🚀 Déploiement

Faire évoluer le déploiement afin de pouvoir installer l'application sur un serveur.

* [ ] Préparer l'image Docker de production
* [ ] Configurer les variables d'environnement
* [ ] Déployer PostgreSQL
* [ ] Déployer l'application conteneurisée
* [ ] Exécuter les migrations Alembic
* [ ] Vérifier la communication entre les différents composants
* [ ] Mettre en place un déploiement reproductible

Objectif final :

```text
GitHub
   │
   ▼
Pull Request
   │
   ├── pytest
   │
   └── SonarQube
          │
          ▼
        Merge
          │
          ▼
      Build Docker
          │
          ▼
       Déploiement
          │
          ▼
   Application en production
```

---

# 🎯 Objectif du projet

L'objectif n'est pas d'utiliser un maximum de technologies, mais de faire évoluer progressivement une application réelle.

Le projet privilégie :

* **la simplicité**
* **la lisibilité du code**
* **la maintenabilité**
* **les tests**
* **la qualité**
* **l'automatisation**
* **la documentation**
* **un déploiement reproductible**

Les nouvelles technologies sont ajoutées lorsqu'elles répondent à un besoin concret du projet.

---

## 🔮 Évolutions possibles

Certaines fonctionnalités pourront être étudiées ultérieurement en fonction des besoins réels :

* [ ] Cartographie des observations
* [ ] Recherche géographique avancée
* [ ] Authentification et gestion des utilisateurs
* [ ] Import / export des observations
* [ ] Statistiques sur les observations
* [ ] Amélioration de l'interface
* [ ] Optimisation des requêtes PostgreSQL
* [ ] Monitoring et logs
* [ ] Amélioration de l'infrastructure de déploiement

Cette liste pourra évoluer avec les besoins du projet.
