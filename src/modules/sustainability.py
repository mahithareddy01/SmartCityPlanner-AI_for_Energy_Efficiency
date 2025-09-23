from src.modules.predictive import forecast_energy
from src.db import database as db

def energy_efficiency_score(city_id: int) -> float:
    """
    Calculate a simple energy efficiency score based on predicted vs actual consumption
    """
    predicted = forecast_energy(city_id)
    
    usage_data = db.get_energy_usage()
    city_usage = [u["consumption"] for u in usage_data if u["cityid"] == city_id]
    
    if not city_usage:
        return 0.0
    
    actual = city_usage[-1]
    score = max(0, 100 - abs(predicted - actual)/predicted*100)
    return round(score, 2)
