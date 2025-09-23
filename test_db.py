# test_db.py
from src.db import database as db

# 1️⃣ Add a City
city = db.add_city("Test City", 100000, 150.5)
print("Added City:", city)

all_cities = db.get_cities()
print("All Cities:", all_cities)

# 2️⃣ Add a Sensor
sensor = db.add_sensor("Temperature", "Downtown", cityid=city["cityid"])
print("Added Sensor:", sensor)

all_sensors = db.get_sensors()
print("All Sensors:", all_sensors)

# 3️⃣ Add Energy Usage
usage = db.add_energy_usage(cityid=city["cityid"], consumption=1250.75)
print("Added Energy Usage:", usage)

all_usage = db.get_energy_usage()
print("All Energy Usage:", all_usage)

# 4️⃣ Add Planner (avoid duplicate email)
existing_planner = db.get_planner_by_email("john@example.com")
if existing_planner:
    planner = existing_planner
else:
    planner = db.add_planner("John Doe", "john@example.com")
print("Added Planner:", planner)

all_planners = db.get_planners()
print("All Planners:", all_planners)

# 5️⃣ Add Report
report = db.add_report(plannerid=planner["plannerid"], cityid=city["cityid"], summary="Test report")
print("Added Report:", report)

all_reports = db.get_all_reports()
print("All Reports:", all_reports)
