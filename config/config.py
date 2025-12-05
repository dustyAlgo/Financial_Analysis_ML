import os
# config/config.py

# === API Configuration ===
# API_BASE_URL = "https://bluemutualfund.in/server/api/company.php"
# API_KEY = "ghfkffu6378382826hhdjgk"  # Replace with your actual key if needed
from dotenv import load_dotenv
load_dotenv()
# === Database Configuration ===
DB_CONFIG = {
    "host":"shuttle.proxy.rlwy.net" ,
    "port":30500,
    "user":"root",
    "password":"YmxCcJfbGqOnIsLRsxtZnMXhVHtiQVyg",
    "database":"ml_db"
}

# === Excel File (Company IDs) ===
COMPANY_LIST_PATH = "data/Nifty100Companies.xlsx"
