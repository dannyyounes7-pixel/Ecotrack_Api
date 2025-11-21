EcoTrack API — Projet API (FastAPI + SQLite)

EcoTrack API est une API REST permettant de gérer et analyser des indicateurs environnementaux locaux (qualité de l’air, CO₂, météo…), provenant de différentes sources de données réelles.

Ce projet a été développé dans le cadre du TP noté de Développement API.

Fonctionnalités principales

Authentification avec JWT (signup / login)

Gestion des utilisateurs (admin et user)

CRUD complet :

Zones

Sources de données

Indicateurs environnementaux

Filtres avancés :

Zone, source, type, dates, tri, pagination

Endpoints statistiques :

Moyennes (/stats/air/averages)

Tendances (/stats/co2/trend)

Scripts :

Initialisation BDD (init_db.py)

Ingestion de données externes (ingest_data.py)

Tests automatisés (pytest)

Technologies utilisées

FastAPI

SQLite + SQLAlchemy

Pydantic v2

JWT (python-jose)

httpx

pytest

Installation du projet

1. Cloner le dépôt
   git clone https://github.com/<VOTRE_USERNAME>/Ecotrack_Api.git
   cd Ecotrack_Api

2. Créer un environnement virtuel
   python3 -m venv venv
   source venv/bin/activate

3. Installer les dépendances
   pip install -r requirements.txt

Lancer l’API
uvicorn app.main:app --reload

Accès à l’API :
http://127.0.0.1:8000

Documentation Swagger :
http://127.0.0.1:8000/docs

Authentification
Exemple d’inscription
POST /auth/signup
{
"email": "test@example.com",
"password": "123456"
}

Exemple de connexion (renvoie un token)
POST /auth/login
{
"email": "test@example.com",
"password": "123456"
}

Utilisation dans Swagger

Dans le bouton "Authorize", entrer :

Bearer VOTRE_TOKEN

Endpoints principaux
Utilisateurs

POST /auth/signup

POST /auth/login

GET /users/me

GET /users (admin)

PUT /users/{id} (admin)

DELETE /users/{id} (admin)

Zones

POST /zones (admin)

GET /zones

PUT /zones/{id} (admin)

DELETE /zones/{id} (admin)

Sources

POST /sources (admin)

GET /sources

PUT /sources/{id} (admin)

DELETE /sources/{id} (admin)

Indicateurs

POST /indicators (admin)

GET /indicators (filtres : zone_id, source_id, type, from_date, to_date, skip, limit, sort)

PUT /indicators/{id} (admin)

DELETE /indicators/{id} (admin)

Endpoints statistiques
Moyenne de qualité de l'air

Exemple :

GET /stats/air/averages?from=2025-11-01T00:00:00&to=2025-11-15T23:00:00&zone=1

Tendance CO₂ (daily ou monthly)
GET /stats/co2/trend?zone=1&period=monthly

Script d’initialisation BDD

Pour remplir la base avec des données de test :

python3 -m scripts.init_db

Ce script crée des zones, des sources et des indicateurs de test.

Script d’ingestion de données externes
python3 -m scripts.ingest_data

Sources utilisées :

OpenAQ : données de qualité de l’air

Open-Meteo : données météo historiques

Tests

Exécution des tests automatisés :

pytest -q

Structure du projet
Ecotrack_Api/
│── app/
│ ├── main.py
│ ├── models/
│ ├── schemas/
│ ├── routers/
│ └── core/
│
│── scripts/
│ ├── init_db.py
│ └── ingest_data.py
│
│── tests/
│ └── test_api.py
│
│── ecotrack.db
│── requirements.txt
│── README.md

Projet réalisé dans le cadre du TP API.
Développé par : Nawfel chakib Younes
