# src/db/database.py
from supabase import create_client, Client
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User authentication functions
def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username from Supabase"""
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user by username: {e}")
        return None

def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email from Supabase"""
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None

def add_user(username: str, email: str, password_hash: str) -> Optional[Dict]:
    """Add new user to Supabase"""
    try:
        payload = {
            "username": username,
            "email": email,
            "password_hash": password_hash
        }
        response = supabase.table("users").insert(payload).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding user: {e}")
        raise e

# City management functions
def add_city(name: str, population: int, area: float) -> Optional[Dict]:
    data = {"name": name, "population": population, "area": area}
    response = supabase.table("city").insert(data).execute()
    return response.data[0] if response.data else None

def get_cities() -> List[Dict]:
    response = supabase.table("city").select("*").execute()
    return response.data

# Sensor management functions
def add_sensor(sensor_type: str, location: str, cityid: int, data: dict = None) -> Optional[Dict]:
    payload = {"type": sensor_type, "location": location, "cityid": cityid, "data": data or {}}
    response = supabase.table("sensor").insert(payload).execute()
    return response.data[0] if response.data else None

def get_sensors() -> List[Dict]:
    response = supabase.table("sensor").select("*").execute()
    return response.data

# Energy data functions
def add_energy_usage(cityid: int, consumption: float, timestamp: str = None) -> Optional[Dict]:
    payload = {"cityid": cityid, "consumption": consumption, "timestamp": timestamp or datetime.now().isoformat()}
    response = supabase.table("energyusage").insert(payload).execute()
    return response.data[0] if response.data else None

def get_energy_usage() -> List[Dict]:
    response = supabase.table("energyusage").select("*").execute()
    return response.data

# Planner management functions
def add_planner(name: str, email: str) -> Optional[Dict]:
    payload = {"name": name, "email": email}
    response = supabase.table("planner").insert(payload).execute()
    return response.data[0] if response.data else None

def get_planners() -> List[Dict]:
    response = supabase.table("planner").select("*").execute()
    return response.data

def get_planner_by_email(email: str) -> Optional[Dict]:
    response = supabase.table("planner").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

# Report management functions
def add_report(plannerid: int, cityid: int, summary: str, date: str = None) -> Optional[Dict]:
    payload = {"plannerid": plannerid, "cityid": cityid, "summary": summary, "date": date or datetime.now().isoformat()}
    response = supabase.table("report").insert(payload).execute()
    return response.data[0] if response.data else None

def get_reports() -> List[Dict]:
    response = supabase.table("report").select("*").execute()
    return response.data
