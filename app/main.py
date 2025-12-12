from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base
from app.database import engine

# IMPORTANT : importer les modèles avant create_all
from app.models.user import User  # noqa: F401

from app.routers import auth, users, zones, indicators, sources, stats
from app.models.zone import Zone  # noqa: F401
from app.models.source import Source  # noqa: F401
from app.models.indicator import Indicator  # noqa: F401

Base.metadata.create_all(bind=engine)
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi des indicateurs environnementaux locaux",
    version="1.0.0",
    security=[{"bearerAuth": []}]  
)
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="EcoTrack API",
        version="1.0.0",
        description="API de suivi des indicateurs environnementaux locaux",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# Configuration CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter les fichiers statiques du frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(zones.router, prefix="/zones", tags=["Zones"])
app.include_router(indicators.router, prefix="/indicators", tags=["Indicators"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])

@app.get("/")
def index():
    """Servir la page d'accueil du frontend"""
    return FileResponse("frontend/index.html")
