from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal, Base, engine
from app.models.zone import Zone
from app.models.source import Source
from app.models.indicator import Indicator
from app.models.user import User  # Import User pour créer la table users

def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Vérifier si les données existent déjà
    existing_zones = db.query(Zone).count()
    if existing_zones > 0:
        print(f"⚠️  Base de données déjà initialisée ({existing_zones} zones trouvées).")
        print("Pour réinitialiser, supprimez ecotrack.db et relancez ce script.")
        db.close()
        return

    # Zones
    paris = Zone(name="Paris", postal_code="75000")
    lyon = Zone(name="Lyon", postal_code="69000")
    db.add_all([paris, lyon])
    db.commit()

    # Sources
    openaq = Source(name="OpenAQ", url="https://openaq.org", description="Qualité de l'air")
    ademe = Source(name="ADEME", url="https://data.ademe.fr", description="CO2 / énergie")
    db.add_all([openaq, ademe])
    db.commit()

    # Indicators tests (10 jours)
    now = datetime.utcnow()
    indicators = []
    for i in range(10):
        ts = now - timedelta(days=i)
        indicators.append(Indicator(
            source_id=openaq.id, zone_id=paris.id,
            type="air", value=10 + i, unit="µg/m3", timestamp=ts
        ))
        indicators.append(Indicator(
            source_id=ademe.id, zone_id=lyon.id,
            type="co2", value=50 + i*2, unit="kgCO2", timestamp=ts
        ))

    db.add_all(indicators)
    db.commit()
    db.close()
    print("✅ DB initialisée avec données de test.")
    print(f"   - 2 zones créées (Paris, Lyon)")
    print(f"   - 2 sources créées (OpenAQ, ADEME)")
    print(f"   - 20 indicateurs créés (10 jours de données)")

if __name__ == "__main__":
    init_db()
