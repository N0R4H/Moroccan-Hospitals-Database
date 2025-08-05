# 🇲🇦 Moroccan Hospital Management System

> 🏥 A modern web-based platform to manage, search, and analyze hospital data in Morocco.  
> 🚀 Built with **Flask** & **TinyDB**, designed for impact in public health and digital governance.

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![NoSQL](https://img.shields.io/badge/NoSQL-TinyDB-blue?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-blueviolet?style=for-the-badge&logo=bootstrap)
![Responsive](https://img.shields.io/badge/Responsive-Design-green?style=for-the-badge&logo=responsive-design)

---

## 📸 Live Demo

🖥️ [Click here to view the demo](#)  
📦 *Coming Soon...*

---

## 🧠 Features

- 🔄 Full CRUD operations on hospital records
- 🔍 Multi-criteria filtering (Region, Delegation, Category, etc.)
- 📥 Import & Export JSON datasets
- 🧭 Easy-to-use UI (French + Arabic support)
- 🧱 MVC architecture with modular codebase
- 🔐 CSRF protection, XSS prevention, secure sessions
- 📱 Fully responsive – Mobile-ready

---

## 🔧 Tech Stack

| Layer        | Technology |
|-------------|------------|
| **Backend**  | ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) + ![Flask](https://img.shields.io/badge/Flask-Microframework-black?logo=flask) |
| **Database** | ![TinyDB](https://img.shields.io/badge/TinyDB-NoSQL-lightgrey) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white) ![JS](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&logoColor=black) |
| **UI/UX**    | ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap) + Font Awesome |
| **Tools**    | ![Jinja2](https://img.shields.io/badge/Jinja2-Templating-red) |

---

## 🏗️ Project Structure

.
├── app.py # Main Flask app
├── data/ # JSON datasets
│ └── sample_hospitals.json
├── static/ # CSS & JS assets
│ ├── css/
│ └── js/
├── templates/ # Jinja2 templates (HTML)
├── requirements.txt # Python dependencies
└── venv/ # Virtual environment

## 🚀 Getting Started

# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/moroccan-hospital-management.git
cd moroccan-hospital-management

# 2. Create and activate virtual env
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
🧪 Then visit: http://localhost:5000
