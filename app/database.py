from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base SQLite (simple et parfaite pour un TP)
DATABASE_URL = "sqlite:///./ecotrack.db"

# Création du moteur
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Obligatoire pour SQLite
)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles SQLAlchemy
Base = declarative_base()


# Dépendance FastAPI pour ouvrir/fermer une session DB proprement
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
