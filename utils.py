import json
import os
import csv


# Constants
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_PATH = os.path.join(DATA_DIR, 'sample_hospitals.json')


def load_hospitals():
    """Load hospital data from a JSON file."""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            hospitals = json.load(file)
        return hospitals
    except FileNotFoundError:
        print(f"[ERROR] Data file not found at {DATA_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error decoding JSON: {e}")
        return []


def save_hospitals(hospitals):
    """Save the hospital data back to the JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as file:
        json.dump(hospitals, file, indent=4, ensure_ascii=False)


def sanitize_hospital_entry(entry):
    """Ensure all expected fields are present and clean."""
    required_fields = ['name', 'city', 'region', 'specialties', 'beds', 'doctors']
    for field in required_fields:
        if field not in entry or entry[field] is None:
            entry[field] = 'Unknown' if field in ['name', 'city', 'region'] else 0
    if isinstance(entry.get("specialties"), str):
        entry["specialties"] = [s.strip() for s in entry["specialties"].split(',')]
    return entry


def sanitize_all(hospitals):
    """Sanitize all hospital records."""
    return [sanitize_hospital_entry(h) for h in hospitals]


def search_hospitals(city=None, region=None, specialty=None, partial=False):
    """Search hospitals by optional filters. Allows partial matches."""
    hospitals = sanitize_all(load_hospitals())
    results = hospitals

    if city:
        results = [h for h in results if city.lower() in h.get("city", "").lower()] if partial \
            else [h for h in results if h.get("city", "").lower() == city.lower()]
    if region:
        results = [h for h in results if region.lower() in h.get("region", "").lower()] if partial \
            else [h for h in results if h.get("region", "").lower() == region.lower()]
    if specialty:
        results = [
            h for h in results
            if any(specialty.lower() in s.lower() for s in h.get("specialties", []))
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
        print(f"[ERROR] Cannot sort by '{by}'. Use 'beds' or 'doctors'.")
        return hospitals
    return sorted(hospitals, key=lambda x: x.get(by, 0), reverse=descending)


def export_hospitals_to_csv(file_path="exported_hospitals.csv"):
    """Export hospital data to CSV."""
    hospitals = sanitize_all(load_hospitals())
    if not hospitals:
        print("[WARNING] No hospital data to export.")
        return

    fieldnames = ['name', 'city', 'region', 'specialties', 'beds', 'doctors']
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for h in hospitals:
            h['specialties'] = ', '.join(h.get('specialties', []))
            writer.writerow(h)
    print(f"[SUCCESS] Exported data to {file_path}")


def export_hospitals_to_json(file_path="exported_hospitals.json"):
    """Export hospital data to a new JSON file."""
    hospitals = sanitize_all(load_hospitals())
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(hospitals, f, indent=4, ensure_ascii=False)
    print(f"[SUCCESS] Exported data to {file_path}")


def add_hospital(entry):
    """Add a new hospital entry to the data."""
    hospitals = sanitize_all(load_hospitals())
    hospitals.append(sanitize_hospital_entry(entry))
    save_hospitals(hospitals)
    print("[INFO] Hospital added successfully.")


def delete_hospital(name):
    """Delete a hospital by name."""
    hospitals = sanitize_all(load_hospitals())
    updated = [h for h in hospitals if h.get("name", "").lower() != name.lower()]
    if len(hospitals) == len(updated):
        print(f"[WARNING] Hospital named '{name}' not found.")
    else:
        save_hospitals(updated)
        print(f"[INFO] Hospital '{name}' removed.")


def update_hospital(name, updated_fields):
    """Update an existing hospital with new field values."""
    hospitals = sanitize_all(load_hospitals())
    found = False
    for h in hospitals:
        if h.get("name", "").lower() == name.lower():
            h.update(updated_fields)
            found = True
            break
    if found:
        save_hospitals(hospitals)
        print(f"[INFO] Hospital '{name}' updated.")
    else:
        print(f"[WARNING] Hospital '{name}' not found.")


def display_hospitals(hospitals):
    """Nicely print hospital information."""
    if not hospitals:
        print("No hospitals found.")
        return
    for h in hospitals:
        print(f"🏥 {h['name']} | {h['city']} - {h['region']} | Beds: {h['beds']} | Doctors: {h['doctors']}")
        print(f"   Specialties: {', '.join(h['specialties'])}")
        print("-" * 60)



if __name__ == "__main__":
    print("🔍 Hospitals in Casablanca with Cardiology:")
    display_hospitals(search_hospitals(city="Casablanca", specialty="Cardiology"))

    print("\n📊 Hospital count by region:")
    for region, count in count_hospitals_by_region().items():
        print(f"{region}: {count} hospitals")

    print("\n⬇️ Top 5 hospitals by number of doctors:")
    display_hospitals(sort_hospitals(by='doctors')[:5])

    print("\n📤 Exporting hospital data to CSV & JSON...")
    export_hospitals_to_csv()
    export_hospitals_to_json()

    print("\n➕ Adding a dummy hospital for demo:")
    dummy_hospital = {
        "name": "Demo Health Center",
        "city": "Rabat",
        "region": "Rabat-Salé",
        "specialties": ["General", "Pediatrics"],
        "beds": 50,
        "doctors": 25
    }
    add_hospital(dummy_hospital)

    print("\n🧽 Now deleting 'Demo Health Center':")
    delete_hospital("Demo Health Center")

