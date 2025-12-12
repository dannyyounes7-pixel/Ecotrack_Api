# 🌍 EcoTrack API & Dashboard

> **Projet de Développement API (FastAPI + SQLite + Frontend Moderne)**

EcoTrack est une plateforme complète pour suivre et analyser les indicateurs environnementaux locaux (Qualité de l'Air, CO₂, Météo) à Paris et Lyon. Elle combine une API REST performante avec un tableau de bord moderne et interactif.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%2FJS-orange)

---

## 🚀 Fonctionnalités

### 🖥️ Dashboard Interactif
- **Design Moderne** : Interface "Glassmorphism" avec mode sombre et animations fluides.
- **Visualisation** : Graphiques interactifs (Chart.js) pour comparer la qualité de l'air et le CO₂.
- **Filtrage** : Filtrage dynamique par zone (Paris/Lyon), type de donnée et date.

### 🔌 API RESTful
- **Authentification Sécurisée** : JWT (JSON Web Tokens) pour l'accès aux données.
- **CRUD Complet** : Gestion des Zones, Sources et Indicateurs.
- **Endpoints Statistiques** : Calcul de moyennes, tendances et agrégations.

### 📊 Données Réelles
- **Qualité de l'Air** : Intégré avec l'API Open-Meteo (PM10, PM2.5, NO2, O3).
- **Intensité Carbone** : Connecté au réseau RTE (France) pour les émissions CO₂ réelles.
- **Simulation** : Générateur de données historiques pour les tests de charge.

---

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/dannyyounes7-pixel/Ecotrack_Api.git
cd Ecotrack_Api
# (Assurez-vous d'être sur la branche 'main')
```

### 2. Environnement Virtuel
```bash
# Création
python3 -m venv venv

# Activation (Linux/Mac)
source venv/bin/activate

# Activation (Windows)
# venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 💾 Initialisation des Données

Avant de lancer le serveur, préparez la base de données :

**1. Créer les tables et les données de test de base :**
```bash
python -m scripts.init_db
```

**2. (Optionnel) Récupérer des données réelles :**
```bash
# Qualité de l'Air (Open-Meteo - 24h dernières heures)
python scripts/fetch_openmeteo.py

# CO2 (RTE France - Temps réel)
python scripts/fetch_rte.py
```

**3. (Optionnel) Générer un historique complet (30 jours) :**
```bash
python scripts/generate_co2.py
```

---

## ▶️ Démarrage

### Lancer le serveur
```bash
./venv/bin/uvicorn app.main:app --reload
```
*Le serveur démarrera sur `http://127.0.0.1:8000`*

### Accéder à l'application
Ouvrez votre navigateur et allez sur :
👉 **http://127.0.0.1:8000**

---

## 🔑 Compte de Démonstration

Vous pouvez créer un compte ou utiliser le compte admin par défaut (si créé via init_db) :
- **Email** : `admin@ecotrack.com`
- **Password** : `admin123`

---

## 📂 Structure du Projet

```
Ecotrack_Api/
├── app/                    # Code source Backend (FastAPI)
│   ├── main.py             # Point d'entrée
│   ├── routers/            # Routes API (auth, zones, indicators...)
│   └── models/             # Modèles SQLAlchemy
├── frontend/               # Code source Frontend
│   ├── index.html          # Page unique (SPA)
│   ├── css/                # Styles modernes
│   └── js/                 # Logique client (Chart.js, Fetch)
├── scripts/                # Scripts utilitaires
│   ├── fetch_openmeteo.py  # Ingestion Air Quality
│   ├── fetch_rte.py        # Ingestion RTE CO2
│   └── generate_co2.py     # Simulation historique
├── ecotrack.db             # Base de données SQLite
└── requirements.txt        # Dépendances Python
```

---

## 📚 Documentation API (Swagger)

Une fois le serveur lancé, la documentation interactive est disponible ici :
👉 **http://127.0.0.1:8000/docs**

---

## 👤 Auteurs

Développé par **Nawfel chakib Younes** et **Danny Younes** dans le cadre du projet API.
