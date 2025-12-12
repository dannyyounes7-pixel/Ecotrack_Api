import sys
import os
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.indicator import Indicator
from app.models.source import Source
from app.models.zone import Zone
from app.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

API_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records"

def fetch_rte_data():
    db = SessionLocal()
    try:
        print("🌍 Connexion à l'API RTE (ÉCO2mix)...")
        
        # 1. Get/Create Source
        source = db.query(Source).filter(Source.name == "RTE").first()
        if not source:
            source = Source(
                name="RTE", 
                url="https://www.rte-france.com/eco2mix", 
                description="Intensité Carbone (France)"
            )
            db.add(source)
            db.commit()
            print("✅ Source 'RTE' créée")

        # 2. Get Zones
        zones = db.query(Zone).all()
        if not zones:
            print("❌ Aucune zone trouvée")
            return

        # 3. Fetch Data (Last 100 records ~ 2 days)
        params = {
            "limit": 100,
            "order_by": "date_heure desc",
            "where": "taux_co2 > 0"
        }
        
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = data.get("results", [])
        print(f"📥 Récupéré {len(records)} points de données")
        
        count = 0
        for record in records:
            timestamp_str = record.get("date_heure")
            timestamp = datetime.fromisoformat(timestamp_str)
            value = record.get("taux_co2")
            
            if value is None:
                continue

            # Add for each zone (since it's national data)
            for zone in zones:
                # Check existance
                exists = db.query(Indicator).filter(
                    Indicator.source_id == source.id,
                    Indicator.zone_id == zone.id,
                    Indicator.timestamp == timestamp,
                    Indicator.type == "co2"
                ).first()
                
                if not exists:
                    indic = Indicator(
                        source_id=source.id,
                        zone_id=zone.id,
                        type="co2",
                        value=value,
                        unit="gCO2/kWh",
                        timestamp=timestamp,
                        metadata_={"perimetre": "France", "source_originale": "Eco2Mix"}
                    )
                    db.add(indic)
                    count += 1
        
        db.commit()
        print(f"✅ Succès ! {count} nouveaux indicateurs RTE ajoutés.")

    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fetch_rte_data()
