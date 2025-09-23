from src.db import database as db
from src.modules.predictive import forecast_energy
from src.modules.sustainability import energy_efficiency_score

def suggest_improvements(city_id: int) -> str:
    forecast = forecast_energy(city_id)
    efficiency = energy_efficiency_score(city_id)

    if efficiency < 70:
        advice = "High inefficiency detected. Consider optimizing energy distribution and upgrading infrastructure."
    elif efficiency < 90:
        advice = "Moderate efficiency. Monitor high-consumption areas and plan targeted improvements."
    else:
        advice = "Excellent efficiency. Maintain current strategies and continue monitoring."

    return f"City ID: {city_id}\nPredicted Energy Usage: {forecast:.2f}\nEfficiency Score: {efficiency}%\nRecommendation: {advice}"
