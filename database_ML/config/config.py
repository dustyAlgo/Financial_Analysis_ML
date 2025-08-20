# config/config.py

# === API Configuration ===
API_BASE_URL = "https://bluemutualfund.in/server/api/company.php"
API_KEY = "ghfkffu6378382826hhdjgk"  # Replace with your actual key if needed

# === Database Configuration ===
DB_CONFIG = {
    "host": "localhost",      # or '127.0.0.1'
    "port": 3306,
    "user": "root",           # your MySQL username
    "password": "Xxxx@0000",  # your MySQL password
    "database": "ml"    # name of the DB you created
}

# === Excel File (Company IDs) ===
COMPANY_LIST_PATH = "data/Nifty100Companies.xlsx"
