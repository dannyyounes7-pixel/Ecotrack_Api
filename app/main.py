from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.database import Base, engine

# IMPORTANT : importer les modèles avant create_all
from app.models.user import User  # noqa: F401
from app.models.zone import Zone  # noqa: F401
from app.models.source import Source  # noqa: F401
from app.models.indicator import Indicator  # noqa: F401

from app.routers import auth, users, zones, indicators, sources, stats

# Créer les tables
Base.metadata.create_all(bind=engine)

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Application FastAPI
app = FastAPI(
    title="EcoTrack API",
    description="API de suivi des indicateurs environnementaux locaux",
    version="1.0.0",
    security=[{"bearerAuth": []}]  
)

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


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(zones.router, prefix="/zones", tags=["Zones"])
app.include_router(indicators.router, prefix="/indicators", tags=["Indicators"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])

@app.get("/")
def index():
    return {"message": "Bienvenue sur l'API EcoTrack"}
