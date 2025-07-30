import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sample_hospitals.json')

def load_hospitals():
    """Load hospital data from a JSON file."""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            hospitals = json.load(file)
        return hospitals
    except FileNotFoundError:
        print(f"Data file not found at {DATA_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def search_hospitals_by_city(city_name):
    """Filter hospitals by city (case-insensitive)."""
    hospitals = load_hospitals()
    return [h for h in hospitals if h.get("city", "").lower() == city_name.lower()]

def count_hospitals_by_region():
    """Count the number of hospitals per region."""
    hospitals = load_hospitals()
    region_counts = {}
    for h in hospitals:
        region = h.get("region", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1
    return region_counts

# Example usage when running the script standalone
if __name__ == "__main__":
    print("Hospitals in Casablanca:")
    for h in search_hospitals_by_city("Casablanca"):
        print("-", h.get("name"))

    print("\nHospital count by region:")
    for region, count in count_hospitals_by_region().items():
        print(f"{region}: {count}")
