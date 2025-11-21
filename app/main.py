from fastapi import FastAPI
from app.database import Base, engine

# ⚠️ IMPORTANT : importer les modèles avant create_all
from app.models.user import User  # noqa: F401

from app.routers import auth, users, zones, indicators, sources, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi des indicateurs environnementaux locaux",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(zones.router, prefix="/zones", tags=["Zones"])
app.include_router(indicators.router, prefix="/indicators", tags=["Indicators"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])

@app.get("/")
def index():
    return {"message": "Bienvenue sur l'API EcoTrack"}
