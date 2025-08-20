# config/config.example.py

# === API Configuration ===
API_BASE_URL = "https://api.example.com/company"
API_KEY = "YOUR_API_KEY_HERE"  # replace with your actual key

# === Database Configuration ===
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",            # your MySQL username
    "password": "your_password", # your MySQL password
    "database": "ml"            # name of your database
}

# === Excel File (Company IDs) ===
COMPANY_LIST_PATH = "data/companies.xlsx"

# Instructions:
# 1) Copy this file to config/config.py
# 2) Fill in your actual secrets (API_KEY and DB credentials)
# 3) Keep config/config.py out of version control (see .gitignore)