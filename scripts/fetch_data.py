# scripts/fetch_data.py

import os
import requests
import pandas as pd
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

def fetch_company_data(company_id):
    url = f"{config.API_BASE_URL}?id={company_id}&api_key={config.API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {company_id}: {e}")
        return None

def main():
    # Load Excel file (path from config)
    import pandas as pd
    excel_path = getattr(config, 'COMPANY_LIST_PATH', 'data/companies.xlsx')
    df = pd.read_excel(excel_path, engine='openpyxl')

    # Get only the company ID column (assume it's called 'id')
    company_ids = df['company_id'].dropna().unique()

    os.makedirs("data/raw", exist_ok=True)

    for company_id in company_ids:
        print(f"📡 Fetching data for {company_id}...")
        data = fetch_company_data(company_id)

        if data:
            file_path = f"data/raw/{company_id}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4))
            print(f"✅ Saved: {file_path}")
        else:
            print(f"❌ Skipped {company_id}")

if __name__ == "__main__":
    main()
