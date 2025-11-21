from fastapi import FastAPI
from app.database import Base, engine

# Import des routers (même s'ils sont vides pour l'instant)
from app.routers import auth, users, zones, indicators, sources, stats

# Création automatique des tables au démarrage
Base.metadata.create_all(bind=engine)

# Initialisation de FastAPI
app = FastAPI(
    title="EcoTrack API",
    description="API de suivi des indicateurs environnementaux locaux",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(zones.router, prefix="/zones", tags=["Zones"])
app.include_router(indicators.router, prefix="/indicators", tags=["Indicators"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])

# Route de test
@app.get("/")
def index():
    return {"message": "Bienvenue sur l'API EcoTrack"}
