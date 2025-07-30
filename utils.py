import json
import os
import csv


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


def sanitize_hospital_entry(entry):
    """Ensure all expected fields are present and clean."""
    required_fields = ['name', 'city', 'region', 'specialties', 'beds', 'doctors']
    for field in required_fields:
        if field not in entry:
            entry[field] = 'Unknown' if field in ['name', 'city', 'region'] else 0
    return entry


def sanitize_all(hospitals):
    """Sanitize all hospital records."""
    return [sanitize_hospital_entry(h) for h in hospitals]


def search_hospitals(city=None, region=None, specialty=None):
    """Search hospitals by optional filters."""
    hospitals = sanitize_all(load_hospitals())
    results = hospitals

    if city:
        results = [h for h in results if h.get("city", "").lower() == city.lower()]
    if region:
        results = [h for h in results if h.get("region", "").lower() == region.lower()]
    if specialty:
        results = [
            h for h in results
            if specialty.lower() in [s.lower() for s in h.get("specialties", [])]
        ]

    return results


def count_hospitals_by_region():
    """Count number of hospitals per region."""
    hospitals = sanitize_all(load_hospitals())
    region_counts = {}
    for h in hospitals:
        region = h.get("region", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1
    return region_counts


def sort_hospitals(by='beds', descending=True):
    """Sort hospitals by number of beds or doctors."""
    hospitals = sanitize_all(load_hospitals())
    if by not in ['beds', 'doctors']:
        print(f"Cannot sort by {by}. Use 'beds' or 'doctors'.")
        return hospitals
    return sorted(hospitals, key=lambda x: x.get(by, 0), reverse=descending)


def export_hospitals_to_csv(file_path="exported_hospitals.csv"):
    """Export hospital data to CSV."""
    hospitals = sanitize_all(load_hospitals())
    if not hospitals:
        print("No hospital data to export.")
        return

    fieldnames = ['name', 'city', 'region', 'specialties', 'beds', 'doctors']
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for h in hospitals:
            # Flatten specialties list for CSV export
            h['specialties'] = ', '.join(h.get('specialties', []))
            writer.writerow(h)

    print(f"Exported data to {file_path}")


# 🧪 Example usage
if __name__ == "__main__":
    print("🔍 Hospitals in Casablanca with cardiology:")
    matches = search_hospitals(city="Casablanca", specialty="Cardiology")
    for h in matches:
        print(f"- {h['name']} ({h['beds']} beds)")

    print("\n📊 Hospital count by region:")
    for region, count in count_hospitals_by_region().items():
        print(f"{region}: {count} hospitals")

    print("\n⬇️ Top 5 largest hospitals by number of doctors:")
    top = sort_hospitals(by='doctors')[:5]
    for h in top:
        print(f"{h['name']}: {h['doctors']} doctors")

    print("\n📤 Exporting hospital data to CSV...")
    export_hospitals_to_csv()
