from src.db import database as db
from src.modules.realtime_monitor import monitor_city
from src.modules.planner_assist import suggest_improvements
from src.modules.sustainability import energy_efficiency_score
from src.modules.predictive import forecast_energy

def main():
    print("Welcome to Energy-Efficient Smart City Planner CLI\n")
    
    while True:
        print("\nChoose an option:")
        print("1. List all cities")
        print("2. Add a new city")
        print("3. List all sensors")
        print("4. Add a new sensor")
        print("5. List all energy usage records")
        print("6. Add energy usage record")
        print("7. List all planners")
        print("8. Add a planner")
        print("9. List all reports")
        print("10. Add a report")
        print("11. Monitor a city (real-time)")
        print("12. Forecast energy usage")
        print("13. Calculate energy efficiency score")
        print("14. Suggest improvements for city planners")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            cities = db.get_cities()
            for c in cities:
                print(f"ID: {c['cityid']}, Name: {c['name']}, Population: {c['population']}, Area: {c['area']}")
        
        elif choice == "2":
            name = input("City Name: ").strip()
            pop = int(input("Population: "))
            area = float(input("Area (km²): "))
            city = db.add_city(name, pop, area)
            print("Added City:", city)
        
        elif choice == "3":
            sensors = db.get_sensors()
            for s in sensors:
                print(f"ID: {s['sensorid']}, Type: {s['type']}, Location: {s['location']}, CityID: {s['cityid']}")
        
        elif choice == "4":
            city_id = int(input("City ID for Sensor: "))
            sensor_type = input("Sensor Type: ").strip()
            location = input("Location: ").strip()
            sensor = db.add_sensor(sensor_type, location, cityid=city_id)
            print("Added Sensor:", sensor)
        
        elif choice == "5":
            usage_list = db.get_energy_usage()
            for u in usage_list:
                print(f"UsageID: {u['usageid']}, CityID: {u['cityid']}, Timestamp: {u['timestamp']}, Consumption: {u['consumption']}")
        
        elif choice == "6":
            city_id = int(input("City ID: "))
            consumption = float(input("Energy Consumption: "))
            usage = db.add_energy_usage(cityid=city_id, consumption=consumption)
            print("Added Energy Usage:", usage)
        
        elif choice == "7":
            planners = db.get_planners()
            for p in planners:
                print(f"PlannerID: {p['plannerid']}, Name: {p['name']}, Email: {p['email']}")
        
        elif choice == "8":
            name = input("Planner Name: ").strip()
            email = input("Planner Email: ").strip()
            existing = db.get_planner_by_email(email)
            if existing:
                planner = existing
                print("Planner already exists:", planner)
            else:
                planner = db.add_planner(name, email)
                print("Added Planner:", planner)
        
        elif choice == "9":
            reports = db.get_reports()
            for r in reports:
                print(f"ReportID: {r['reportid']}, PlannerID: {r['plannerid']}, CityID: {r['cityid']}, Date: {r['date']}, Summary: {r['summary']}")
        
        elif choice == "10":
            planner_id = int(input("Planner ID: "))
            city_id = int(input("City ID: "))
            summary = input("Report Summary: ").strip()
            report = db.add_report(plannerid=planner_id, cityid=city_id, summary=summary)
            print("Added Report:", report)
        
        elif choice == "11":
            city_id = int(input("City ID: "))
            data = monitor_city(city_id)
            print("Real-Time Monitoring Data:", data)
        
        elif choice == "12":
            city_id = int(input("City ID: "))
            prediction = forecast_energy(city_id)
            print(f"Predicted Energy Usage for next day: {prediction:.2f}")
        
        elif choice == "13":
            city_id = int(input("City ID: "))
            score = energy_efficiency_score(city_id)
            print(f"Energy Efficiency Score: {score}%")
        
        elif choice == "14":
            city_id = int(input("City ID: "))
            advice = suggest_improvements(city_id)
            print(advice)
        
        elif choice == "0":
            print("Exiting... Stay efficient!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
