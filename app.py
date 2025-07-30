import json
import os
from datetime import datetime
from tinydb import TinyDB, Query
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Create necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Initialize TinyDB database
db = TinyDB('moroccan_hospitals.json')
hospitals_table = db.table('hospitals')

class HospitalCRUD:
    def __init__(self):
        self.query = Query()
    
    def load_initial_data(self, json_file_path):
        """Load initial data from JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Clear existing data
                hospitals_table.truncate()
                
                # Handle different JSON structures
                if isinstance(data, list):
                    # If it's a list of hospitals
                    for i, hospital in enumerate(data):
                        if '_id' not in hospital:
                            hospital['_id'] = f"HOSP_{i+1:04d}"
                        hospital['created_at'] = datetime.now().isoformat()
                    hospitals_table.insert_multiple(data)
                elif isinstance(data, dict):
                    # If it's a single hospital object
                    if '_id' not in data:
                        data['_id'] = "HOSP_0001"
                    data['created_at'] = datetime.now().isoformat()
                    hospitals_table.insert(data)
                
                return True, len(data) if isinstance(data, list) else 1
        except FileNotFoundError:
            return False, f"File {json_file_path} not found"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON format: {str(e)}"
        except Exception as e:
            return False, f"Error loading data: {str(e)}"
    
    def create_hospital(self, hospital_data):
        """Create a new hospital record"""
        # Auto-generate ID if not provided
        if '_id' not in hospital_data or not hospital_data['_id']:
            existing_count = len(hospitals_table.all())
            hospital_data['_id'] = f"HOSP_{existing_count + 1:04d}"
        
        hospital_data['created_at'] = datetime.now().isoformat()
        hospital_data['updated_at'] = datetime.now().isoformat()
        
        return hospitals_table.insert(hospital_data)
    
    def read_all_hospitals(self):
        """Read all hospital records"""
        return hospitals_table.all()
    
    def read_hospital_by_id(self, hospital_id):
        """Read a specific hospital by ID"""
        if isinstance(hospital_id, int):
            return hospitals_table.get(doc_id=hospital_id)
        else:
            return hospitals_table.search(self.query._id == hospital_id)
    
    def search_hospitals(self, **kwargs):
        """Search hospitals by various criteria"""
        if not any(kwargs.values()):
            return self.read_all_hospitals()
        
        results = []
        all_hospitals = self.read_all_hospitals()
        
        for hospital in all_hospitals:
            match = True
            for key, value in kwargs.items():
                if value and value.strip():
                    hospital_value = str(hospital.get(key, '')).lower()
                    search_value = str(value).lower()
                    if search_value not in hospital_value:
                        match = False
                        break
            if match:
                results.append(hospital)
        
        return results
    
    def update_hospital(self, hospital_id, updated_data):
        """Update a hospital record"""
        updated_data['updated_at'] = datetime.now().isoformat()
        
        if isinstance(hospital_id, int):
            return hospitals_table.update(updated_data, doc_ids=[hospital_id])
        else:
            return hospitals_table.update(updated_data, self.query._id == hospital_id)
    
    def delete_hospital(self, hospital_id):
        """Delete a hospital record"""
        if isinstance(hospital_id, int):
            return hospitals_table.remove(doc_ids=[hospital_id])
        else:
            return hospitals_table.remove(self.query._id == hospital_id)
    
    def get_statistics(self):
        """Get comprehensive statistics about the dataset"""
        all_hospitals = self.read_all_hospitals()
        stats = {
            'total_hospitals': len(all_hospitals),
            'regions': {},
            'categories': {},
            'delegations': {},
            'communes': {}
        }
        
        for hospital in all_hospitals:
            # Count by region
            region = hospital.get('region', 'Unknown')
            stats['regions'][region] = stats['regions'].get(region, 0) + 1
            
            # Count by category
            category = hospital.get('categorie', 'Unknown')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Count by delegation
            delegation = hospital.get('delegation', 'Unknown')
            stats['delegations'][delegation] = stats['delegations'].get(delegation, 0) + 1
            
            # Count by commune
            commune = hospital.get('commune', 'Unknown')
            stats['communes'][commune] = stats['communes'].get(commune, 0) + 1
        
        return stats
    
    def create_sample_data(self):
        """Create sample data for testing"""
        sample_hospitals = [
                {
    "_id": "HOSP_0006",
    "nom_etablissement": "Hôpital Ibn Sina",
    "region": "Rabat-Salé-Kénitra",
    "delegation": "Rabat",
    "commune": "Rabat",
    "categorie": "CHU"
  },
  {
    "_id": "HOSP_0007",
    "nom_etablissement": "Centre Hospitalier Ibn Rochd",
    "region": "Casablanca-Settat",
    "delegation": "Casablanca",
    "commune": "Casablanca",
    "categorie": "CHU"
  },
  {
    "_id": "HOSP_0008",
    "nom_etablissement": "Hôpital Provincial Al Hoceima",
    "region": "Tanger-Tétouan-Al Hoceïma",
    "delegation": "Al Hoceima",
    "commune": "Al Hoceima",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0009",
    "nom_etablissement": "Centre Hospitalier Regional Oujda",
    "region": "L'Oriental",
    "delegation": "Oujda-Angad",
    "commune": "Oujda",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0010",
    "nom_etablissement": "Hôpital Mohammed VI Marrakech",
    "region": "Marrakech-Safi",
    "delegation": "Marrakech",
    "commune": "Marrakech",
    "categorie": "CHU"
  },
  {
    "_id": "HOSP_0011",
    "nom_etablissement": "Hôpital Provincial Nador",
    "region": "L'Oriental",
    "delegation": "Nador",
    "commune": "Nador",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0012",
    "nom_etablissement": "Centre de Santé Urbain Témara",
    "region": "Rabat-Salé-Kénitra",
    "delegation": "Skhirate-Témara",
    "commune": "Témara",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0013",
    "nom_etablissement": "Hôpital Régional Errachidia",
    "region": "Drâa-Tafilalet",
    "delegation": "Errachidia",
    "commune": "Errachidia",
    "categorie": "Hôpital Régional"
  },
  {
    "_id": "HOSP_0014",
    "nom_etablissement": "Centre Hospitalier Mohamed V Meknès",
    "region": "Fès-Meknès",
    "delegation": "Meknès",
    "commune": "Meknès",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0015",
    "nom_etablissement": "Hôpital Provincial Taza",
    "region": "Fès-Meknès",
    "delegation": "Taza",
    "commune": "Taza",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0016",
    "nom_etablissement": "Centre Hospitalier Regional Beni Mellal",
    "region": "Béni Mellal-Khénifra",
    "delegation": "Béni Mellal",
    "commune": "Béni Mellal",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0017",
    "nom_etablissement": "Hôpital Mohammed V Tanger",
    "region": "Tanger-Tétouan-Al Hoceïma",
    "delegation": "Tanger-Assilah",
    "commune": "Tanger",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0018",
    "nom_etablissement": "Centre de Santé Urbain Salé",
    "region": "Rabat-Salé-Kénitra",
    "delegation": "Salé",
    "commune": "Salé",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0019",
    "nom_etablissement": "Hôpital Provincial Tiznit",
    "region": "Souss-Massa",
    "delegation": "Tiznit",
    "commune": "Tiznit",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0020",
    "nom_etablissement": "Centre Hospitalier Hassan II Settat",
    "region": "Casablanca-Settat",
    "delegation": "Settat",
    "commune": "Settat",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0021",
    "nom_etablissement": "Hôpital Provincial Tétouan",
    "region": "Tanger-Tétouan-Al Hoceïma",
    "delegation": "Tétouan",
    "commune": "Tétouan",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0022",
    "nom_etablissement": "Centre de Santé Urbain Kenitra",
    "region": "Rabat-Salé-Kénitra",
    "delegation": "Kenitra",
    "commune": "Kenitra",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0023",
    "nom_etablissement": "Hôpital Régional Laâyoune",
    "region": "Laâyoune-Sakia El Hamra",
    "delegation": "Laâyoune",
    "commune": "Laâyoune",
    "categorie": "Hôpital Régional"
  },
  {
    "_id": "HOSP_0024",
    "nom_etablissement": "Centre Hospitalier El Jadida",
    "region": "Casablanca-Settat",
    "delegation": "El Jadida",
    "commune": "El Jadida",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0025",
    "nom_etablissement": "Hôpital Provincial Khouribga",
    "region": "Casablanca-Settat",
    "delegation": "Khouribga",
    "commune": "Khouribga",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0026",
    "nom_etablissement": "Centre de Santé Urbain Mohammedia",
    "region": "Casablanca-Settat",
    "delegation": "Mohammedia",
    "commune": "Mohammedia",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0027",
    "nom_etablissement": "Hôpital Provincial Larache",
    "region": "Tanger-Tétouan-Al Hoceïma",
    "delegation": "Larache",
    "commune": "Larache",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0028",
    "nom_etablissement": "Centre Hospitalier Regional Safi",
    "region": "Marrakech-Safi",
    "delegation": "Safi",
    "commune": "Safi",
    "categorie": "CHR"
  },
  {
    "_id": "HOSP_0029",
    "nom_etablissement": "Hôpital Provincial Khénifra",
    "region": "Béni Mellal-Khénifra",
    "delegation": "Khénifra",
    "commune": "Khénifra",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0030",
    "nom_etablissement": "Centre de Santé Urbain Essaouira",
    "region": "Marrakech-Safi",
    "delegation": "Essaouira",
    "commune": "Essaouira",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0031",
    "nom_etablissement": "Hôpital Provincial Berkane",
    "region": "L'Oriental",
    "delegation": "Berkane",
    "commune": "Berkane",
    "categorie": "Hôpital Provincial"
  },
  {
    "_id": "HOSP_0032",
    "nom_etablissement": "Centre Hospitalier Boulemane",
    "region": "Fès-Meknès",
    "delegation": "Boulemane",
    "commune": "Boulemane",
    "categorie": "Hôpital Local"
  },
  {
    "_id": "HOSP_0033",
    "nom_etablissement": "Hôpital Régional Dakhla",
    "region": "Dakhla-Oued Ed-Dahab",
    "delegation": "Oued Ed-Dahab",
    "commune": "Dakhla",
    "categorie": "Hôpital Régional"
  },
  {
    "_id": "HOSP_0034",
    "nom_etablissement": "Centre de Santé Urbain Berrechid",
    "region": "Casablanca-Settat",
    "delegation": "Berrechid",
    "commune": "Berrechid",
    "categorie": "Centre de Santé"
  },
  {
    "_id": "HOSP_0035",
    "nom_etablissement": "Hôpital Provincial Azilal",
    "region": "Béni Mellal-Khénifra",
    "delegation": "Azilal",
    "commune": "Azilal",
    "categorie": "Hôpital Provincial"
  }
        ]
        
        # Save sample data to file
        with open('data/sample_hospitals.json', 'w', encoding='utf-8') as f:
            json.dump(sample_hospitals, f, indent=2, ensure_ascii=False)
        
        # Load into database
        hospitals_table.truncate()
        for hospital in sample_hospitals:
            hospital['created_at'] = datetime.now().isoformat()
            hospital['updated_at'] = datetime.now().isoformat()
        hospitals_table.insert_multiple(sample_hospitals)
        
        return len(sample_hospitals)

# Initialize CRUD operations
hospital_crud = HospitalCRUD()

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    hospitals = hospital_crud.read_all_hospitals()
    stats = hospital_crud.get_statistics()
    return render_template('index.html', hospitals=hospitals, stats=stats)

# API Routes
@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    """Get all hospitals"""
    hospitals = hospital_crud.read_all_hospitals()
    return jsonify(hospitals)

@app.route('/api/hospitals/<hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    """Get specific hospital"""
    try:
        # Try as integer first (doc_id), then as string (_id)
        hospital = hospital_crud.read_hospital_by_id(int(hospital_id))
        if not hospital:
            hospital = hospital_crud.read_hospital_by_id(hospital_id)
        
        if hospital:
            return jsonify(hospital)
        return jsonify({'error': 'Hospital not found'}), 404
    except ValueError:
        hospital = hospital_crud.read_hospital_by_id(hospital_id)
        if hospital:
            return jsonify(hospital)
        return jsonify({'error': 'Hospital not found'}), 404

@app.route('/api/hospitals', methods=['POST'])
def create_hospital():
    """Create new hospital"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        hospital_id = hospital_crud.create_hospital(data)
        return jsonify({'message': 'Hospital created successfully', 'id': hospital_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/hospitals/<hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    """Update hospital"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Try updating by doc_id first, then by _id
        try:
            success = hospital_crud.update_hospital(int(hospital_id), data)
        except ValueError:
            success = hospital_crud.update_hospital(hospital_id, data)
        
        if success:
            return jsonify({'message': 'Hospital updated successfully'})
        return jsonify({'error': 'Hospital not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/hospitals/<hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    """Delete hospital"""
    try:
        # Try deleting by doc_id first, then by _id
        try:
            success = hospital_crud.delete_hospital(int(hospital_id))
        except ValueError:
            success = hospital_crud.delete_hospital(hospital_id)
        
        if success:
            return jsonify({'message': 'Hospital deleted successfully'})
        return jsonify({'error': 'Hospital not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/search', methods=['GET'])
def search_hospitals():
    """Search hospitals"""
    region = request.args.get('region', '')
    delegation = request.args.get('delegation', '')
    commune = request.args.get('commune', '')
    categorie = request.args.get('categorie', '')
    nom_etablissement = request.args.get('nom_etablissement', '')
    
    results = hospital_crud.search_hospitals(
        region=region,
        delegation=delegation,
        commune=commune,
        categorie=categorie,
        nom_etablissement=nom_etablissement
    )
    return jsonify(results)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get dataset statistics"""
    stats = hospital_crud.get_statistics()
    return jsonify(stats)

# Data Management Routes
@app.route('/load_data', methods=['POST'])
def load_data():
    """Load data from uploaded JSON file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.json'):
            # Save uploaded file temporarily
            file_path = 'temp_upload.json'
            file.save(file_path)
            
            # Load data into database
            success, message = hospital_crud.load_initial_data(file_path)
            
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            if success:
                return jsonify({'message': f'Data loaded successfully! {message} hospitals imported.'})
            else:
                return jsonify({'error': message}), 400
        
        return jsonify({'error': 'Invalid file format. Please upload a JSON file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/create_sample', methods=['POST'])
def create_sample_data():
    """Create sample data for testing"""
    try:
        count = hospital_crud.create_sample_data()
        return jsonify({'message': f'Sample data created successfully! {count} hospitals added.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/export_data')
def export_data():
    """Export all data as JSON"""
    hospitals = hospital_crud.read_all_hospitals()
    return jsonify(hospitals)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create sample data if database is empty
    if len(hospital_crud.read_all_hospitals()) == 0:
        print("Creating sample data...")
        hospital_crud.create_sample_data()
        print("Sample data created!")
    
    print("🏥 Moroccan Hospitals Management System")
    print("📊 TinyDB NoSQL Database")
    print("🌐 Server starting at http://localhost:5000")
    print("📁 Upload your JSON file or use the sample data")
    
    app.run(debug=True, host='0.0.0.0', port=5002)