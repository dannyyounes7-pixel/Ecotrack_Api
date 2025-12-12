"""
Script pour récupérer les données météo et de qualité de l'air depuis Open-Meteo
et les stocker dans la base de données EcoTrack.
"""
import sys
from pathlib import Path
from datetime import datetime
import requests

# Ajouter le répertoire parent au path pour importer les modules de l'app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.zone import Zone
from app.models.source import Source
from app.models.indicator import Indicator

# Coordonnées des villes
CITIES = {
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Lyon": {"lat": 45.7640, "lon": 4.8357}
}

# Configuration Open-Meteo
OPENMETEO_AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_air_quality_data(city_name, lat, lon):
    """Récupère les données de qualité de l'air pour une ville."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide",
        "timezone": "Europe/Paris"
    }
    
    try:
        response = requests.get(OPENMETEO_AIR_QUALITY_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Erreur lors de la récupération des données pour {city_name}: {e}")
        return None


def store_indicators(db, zone_id, source_id, data, city_name):
    """Stocke les indicateurs dans la base de données."""
    if not data or "hourly" not in data:
        print(f"⚠️  Pas de données horaires pour {city_name}")
        return 0
    
    hourly = data["hourly"]
    times = hourly.get("time", [])
    
    # Prendre seulement les 24 dernières heures
    count = 0
    for i in range(min(24, len(times))):
        timestamp = datetime.fromisoformat(times[i])
        
        # PM10
        if hourly.get("pm10") and hourly["pm10"][i] is not None:
            indicator = Indicator(
                source_id=source_id,
                zone_id=zone_id,
                type="air",
                value=round(hourly["pm10"][i], 2),
                unit="µg/m³",
                timestamp=timestamp,
                metadata={"pollutant": "PM10"}
            )
            db.add(indicator)
            count += 1
        
        # PM2.5
        if hourly.get("pm2_5") and hourly["pm2_5"][i] is not None:
            indicator = Indicator(
                source_id=source_id,
                zone_id=zone_id,
                type="air",
                value=round(hourly["pm2_5"][i], 2),
                unit="µg/m³",
                timestamp=timestamp,
                metadata={"pollutant": "PM2.5"}
            )
            db.add(indicator)
            count += 1
        
        # NO2
        if hourly.get("nitrogen_dioxide") and hourly["nitrogen_dioxide"][i] is not None:
            indicator = Indicator(
                source_id=source_id,
                zone_id=zone_id,
                type="air",
                value=round(hourly["nitrogen_dioxide"][i], 2),
                unit="µg/m³",
                timestamp=timestamp,
                metadata={"pollutant": "NO2"}
            )
            db.add(indicator)
            count += 1
        
        # O3
        if hourly.get("ozone") and hourly["ozone"][i] is not None:
            indicator = Indicator(
                source_id=source_id,
                zone_id=zone_id,
                type="air",
                value=round(hourly["ozone"][i], 2),
                unit="µg/m³",
                timestamp=timestamp,
                metadata={"pollutant": "O3"}
            )
            db.add(indicator)
            count += 1
        
        # CO
        if hourly.get("carbon_monoxide") and hourly["carbon_monoxide"][i] is not None:
            indicator = Indicator(
                source_id=source_id,
                zone_id=zone_id,
                type="air",
                value=round(hourly["carbon_monoxide"][i], 2),
                unit="µg/m³",
                timestamp=timestamp,
                metadata={"pollutant": "CO"}
            )
            db.add(indicator)
            count += 1
    
    return count


def main():
    """Fonction principale."""
    print("🌍 Récupération des données Open-Meteo...")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Vérifier/créer la source Open-Meteo
        source = db.query(Source).filter(Source.name == "Open-Meteo").first()
        if not source:
            source = Source(
                name="Open-Meteo",
                url="https://open-meteo.com",
                description="Données météo et qualité de l'air en temps réel"
            )
            db.add(source)
            db.commit()
            db.refresh(source)
            print(f"✅ Source 'Open-Meteo' créée (ID: {source.id})")
        else:
            print(f"✅ Source 'Open-Meteo' trouvée (ID: {source.id})")
        
        total_indicators = 0
        
        # Récupérer les données pour chaque ville
        for city_name, coords in CITIES.items():
            print(f"\n📍 {city_name} ({coords['lat']}, {coords['lon']})")
            
            # Trouver la zone correspondante
            zone = db.query(Zone).filter(Zone.name == city_name).first()
            if not zone:
                print(f"⚠️  Zone '{city_name}' non trouvée dans la base de données")
                continue
            
            # Récupérer les données
            data = fetch_air_quality_data(city_name, coords["lat"], coords["lon"])
            
            if data:
                # Stocker les indicateurs
                count = store_indicators(db, zone.id, source.id, data, city_name)
                total_indicators += count
                print(f"   ✅ {count} indicateurs ajoutés")
        
        # Commit final
        db.commit()
        
        print("\n" + "=" * 60)
        print(f"✅ Récupération terminée !")
        print(f"   Total: {total_indicators} indicateurs ajoutés")
        print(f"   Source: Open-Meteo")
        print(f"   Villes: {', '.join(CITIES.keys())}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
