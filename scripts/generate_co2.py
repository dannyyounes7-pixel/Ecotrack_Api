import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.indicator import Indicator
from app.models.source import Source
from app.models.zone import Zone
from app.database import Base, DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_data():
    db = SessionLocal()
    try:
        # Get or create Simulation source
        source = db.query(Source).filter(Source.name == "Simulation").first()
        if not source:
            source = Source(name="Simulation", url="#", description="Données générées pour tests")
            db.add(source)
            db.commit()
            print("✅ Source 'Simulation' créée")
        else:
            print(f"ℹ️ Source 'Simulation' existe déjà (ID: {source.id})")

        # Get zones
        paris = db.query(Zone).filter(Zone.name == "Paris").first()
        lyon = db.query(Zone).filter(Zone.name == "Lyon").first()
        
        if not paris or not lyon:
            print("❌ Zones manquantes (d'abord lancer init_db.py)")
            return

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        count = 0
        current_date = start_date
        print("🔄 Génération des données en cours...")
        
        while current_date <= end_date:
            # Generate typical daily curve
            hour = current_date.hour
            # Peak at 8am and 7pm (rush hours for simulation)
            base_co2 = 50 + (20 * (1 if 7 <= hour <= 20 else 0.5)) 
            
            # Add randomness
            # Paris: Higher values
            val_paris = base_co2 + random.uniform(5, 25) + (hour % 5)
            # Lyon: Slightly lower
            val_lyon = base_co2 + random.uniform(-5, 15) + ((hour + 2) % 6)

            ind_paris = Indicator(
                source_id=source.id,
                zone_id=paris.id,
                type="co2",
                value=round(val_paris, 2),
                unit="gCO2/kWh",
                timestamp=current_date
            )
            
            ind_lyon = Indicator(
                source_id=source.id,
                zone_id=lyon.id,
                type="co2",
                value=round(val_lyon, 2),
                unit="gCO2/kWh",
                timestamp=current_date
            )

            db.add(ind_paris)
            db.add(ind_lyon)
            
            count += 2
            current_date += timedelta(hours=1)
        
        db.commit()
        print(f"✅ Succès ! {count} indicateurs CO2 ajoutés sur 30 jours.")
        print("   Zones: Paris, Lyon")
        print("   Source: Simulation")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_data()
