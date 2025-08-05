import json
import os
import csv
import datetime
import logging


def log_action(action):
    """Log an action to file."""
    logging.info(action)


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def print_divider():
    print("=" * 60)


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
        print(f"[ERROR] JSON decode failed: {e}")
        return []


def save_hospitals(hospitals):
    """Save hospital list to JSON file."""
    with open(DATA_PATH, 'w', encoding='utf-8') as file:
        json.dump(hospitals, file, indent=4, ensure_ascii=False)
    log_action("Saved hospital data.")


def sanitize_hospital_entry(entry):
    """Ensure entry is safe and complete."""
    default = {
        "name": "Unknown",
        "city": "Unknown",
        "region": "Unknown",
        "specialties": [],
        "beds": 0,
        "doctors": 0,
        "last_updated": current_timestamp()
    }
    for key in default:
        if key not in entry:
            entry[key] = default[key]
    if isinstance(entry["specialties"], str):
        entry["specialties"] = [s.strip() for s in entry["specialties"].split(',')]
    return entry


def sanitize_all(hospitals):
    return [sanitize_hospital_entry(h) for h in hospitals]


def add_hospital(entry):
    hospitals = sanitize_all(load_hospitals())
    entry = sanitize_hospital_entry(entry)
    hospitals.append(entry)
    save_hospitals(hospitals)
    print("[✔] Hospital added successfully.")
    log_action(f"Added hospital: {entry['name']}")


def delete_hospital(name):
    hospitals = sanitize_all(load_hospitals())
    new_list = [h for h in hospitals if h['name'].lower() != name.lower()]
    if len(new_list) == len(hospitals):
        print("[✘] No hospital with that name.")
    else:
        save_hospitals(new_list)
        print(f"[✔] Deleted '{name}'")
        log_action(f"Deleted hospital: {name}")


def update_hospital(name, updated_fields):
    hospitals = sanitize_all(load_hospitals())
    found = False
    for h in hospitals:
        if h['name'].lower() == name.lower():
            h.update(updated_fields)
            h['last_updated'] = current_timestamp()
            found = True
            break
    if found:
        save_hospitals(hospitals)
        print(f"[✔] Updated '{name}'")
        log_action(f"Updated hospital: {name}")
    else:
        print("[✘] Hospital not found.")


def search_hospitals(city=None, region=None, specialty=None, bed_min=None, bed_max=None, doc_min=None, doc_max=None):
    hospitals = sanitize_all(load_hospitals())
    results = hospitals
    if city:
        results = [h for h in results if city.lower() in h['city'].lower()]
    if region:
        results = [h for h in results if region.lower() in h['region'].lower()]
    if specialty:
        results = [h for h in results if any(specialty.lower() in s.lower() for s in h['specialties'])]
    if bed_min is not None:
        results = [h for h in results if h['beds'] >= bed_min]
    if bed_max is not None:
        results = [h for h in results if h['beds'] <= bed_max]
    if doc_min is not None:
        results = [h for h in results if h['doctors'] >= doc_min]
    if doc_max is not None:
        results = [h for h in results if h['doctors'] <= doc_max]
    return results


def count_hospitals_by_region():
    hospitals = sanitize_all(load_hospitals())
    counts = {}
    for h in hospitals:
        r = h['region']
        counts[r] = counts.get(r, 0) + 1
    return counts


def sort_hospitals(by='beds', desc=True):
    hospitals = sanitize_all(load_hospitals())
    return sorted(hospitals, key=lambda h: h.get(by, 0), reverse=desc)


def export_csv(path='exported_hospitals.csv'):
    hospitals = sanitize_all(load_hospitals())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'city', 'region', 'specialties', 'beds', 'doctors', 'last_updated'])
        writer.writeheader()
        for h in hospitals:
            h['specialties'] = ', '.join(h['specialties'])
            writer.writerow(h)
    print(f"[✔] CSV exported to {path}")
    log_action(f"Exported CSV: {path}")

def print_hospital(h):
    print_divider()
    print(f"🏥 {h['name']} | 📍 {h['city']} - {h['region']}")
    print(f"🛏 Beds: {h['beds']} | 🩺 Doctors: {h['doctors']}")
    print(f"🧬 Specialties: {', '.join(h['specialties'])}")
    print(f"🕓 Last Updated: {h['last_updated']}")


def list_hospitals(hospitals):
    if not hospitals:
        print("[!] No hospitals found.")
        return
    for h in hospitals:
        print_hospital(h)


def show_statistics():
    hospitals = sanitize_all(load_hospitals())
    total = len(hospitals)
    avg_beds = sum(h['beds'] for h in hospitals) / total if total else 0
    avg_docs = sum(h['doctors'] for h in hospitals) / total if total else 0
    print_divider()
    print(f"📊 Total hospitals: {total}")
    print(f"📈 Avg beds: {avg_beds:.2f}")
    print(f"📈 Avg doctors: {avg_docs:.2f}")
    print_divider()

def main_menu():
    while True:
        print_divider()
        print("🏥 HOSPITAL SYSTEM MENU")
        print("1. List all hospitals")
        print("2. Search hospitals")
        print("3. Add hospital")
        print("4. Update hospital")
        print("5. Delete hospital")
        print("6. Export to CSV")
        print("7. Show region stats")
        print("8. Show global stats")
        print("9. Exit")
        print_divider()

        choice = input("Choose an option (1-9): ").strip()
        if choice == "1":
            list_hospitals(sanitize_all(load_hospitals()))
        elif choice == "2":
            city = input("City? (optional): ").strip() or None
            region = input("Region? (optional): ").strip() or None
            specialty = input("Specialty? (optional): ").strip() or None
            results = search_hospitals(city=city, region=region, specialty=specialty)
            list_hospitals(results)
        elif choice == "3":
            entry = {
                "name": input("Hospital name: "),
                "city": input("City: "),
                "region": input("Region: "),
                "specialties": input("Specialties (comma-separated): "),
                "beds": int(input("Beds: ")),
                "doctors": int(input("Doctors: "))
            }
            add_hospital(entry)
        elif choice == "4":
            name = input("Hospital to update: ")
            field = input("Field to update (name, city, region, beds, doctors, specialties): ").strip()
            value = input("New value: ")
            if field in ['beds', 'doctors']:
                value = int(value)
            elif field == "specialties":
                value = [s.strip() for s in value.split(',')]
            update_hospital(name, {field: value})
        elif choice == "5":
            name = input("Hospital to delete: ")
            confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ")
            if confirm.lower() == "y":
                delete_hospital(name)
        elif choice == "6":
            export_csv()
        elif choice == "7":
            stats = count_hospitals_by_region()
            print_divider()
            for region, count in stats.items():
                print(f"{region}: {count} hospitals")
            print_divider()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")



if __name__ == "__main__":
    main_menu()


