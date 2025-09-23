from src.db import database as db
from datetime import datetime

def monitor_city(city_id: int) -> dict:
    """
    Return latest sensor readings and energy usage for a city
    """
    sensors = db.get_sensors()
    city_sensors = [s for s in sensors if s["cityid"] == city_id]

    energy_usage_data = db.get_energy_usage()
    city_energy = [e for e in energy_usage_data if e["cityid"] == city_id]

    latest_energy = city_energy[-1] if city_energy else {"consumption": 0, "timestamp": datetime.now().isoformat()}

    return {
        "cityid": city_id,
        "latest_energy_usage": latest_energy,
        "sensors": city_sensors
    }
