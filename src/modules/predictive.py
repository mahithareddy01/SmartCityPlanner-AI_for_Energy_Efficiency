from typing import Dict, List
import numpy as np
from sklearn.linear_model import LinearRegression
from src.db import database as db

def forecast_energy(city_id: int, past_days: int = 7) -> float:
    """
    Predict next day's energy consumption for a given city using simple linear regression
    """
    usage_data = db.get_energy_usage()
    city_usage = [u["consumption"] for u in usage_data if u["cityid"] == city_id][-past_days:]
    
    if len(city_usage) < 2:
        return np.mean(city_usage) if city_usage else 0

    X = np.arange(len(city_usage)).reshape(-1, 1)
    y = np.array(city_usage)
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(np.array([[len(city_usage)]]))
    return float(prediction[0])
