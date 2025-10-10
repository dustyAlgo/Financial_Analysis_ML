# scripts/store_results.py

import os
import sys
import json
import uuid
import mysql.connector
from mysql.connector import Error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

def connect_to_db():
    return mysql.connector.connect(
        host=config.DB_CONFIG["host"],
        port=config.DB_CONFIG["port"],
        user=config.DB_CONFIG["user"],
        password=config.DB_CONFIG["password"],
        database=config.DB_CONFIG["database"]
    )

def insert_into_companies(cursor, company):
    query = """
    INSERT INTO companies (id, company_logo, company_name, chart_link, about_company, website, nse_profile, bse_profile, face_value, book_value, roce_percentage, roe_percentage)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE company_name = VALUES(company_name), roe_percentage = VALUES(roe_percentage)
    """
    values = (
        company.get("id"),
        company.get("company_logo"),
        company.get("company_name"),
        company.get("chart_link"),
        company.get("about_company"),
        company.get("website"),
        company.get("nse_profile"),
        company.get("bse_profile"),
        company.get("face_value"),
        company.get("book_value"),
        company.get("roce_percentage"),
        company.get("roe_percentage") or None  # Convert empty string to None for MySQL
    )
    cursor.execute(query, values)

def insert_into_analysis(cursor, company_id, sales_growth, profit_growth, roe):
    query = """
    INSERT INTO analysis (id, company_id, compounded_sales_growth, compounded_profit_growth, stock_price_cagr, roe)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE compounded_sales_growth=VALUES(compounded_sales_growth), compounded_profit_growth=VALUES(compounded_profit_growth), roe=VALUES(roe)
    """
    values = (
        str(uuid.uuid4())[:8],  # generate short random ID
        company_id,
        f"{sales_growth:.2f}%",
        f"{profit_growth:.2f}%",
        "0%",  # Placeholder for stock_price_cagr if not available
        f"{roe:.2f}%"
    )
    cursor.execute(query, values)

def insert_into_prosandcons(cursor, company_id, pros, cons):
    # Delete old records first (if needed)
    cursor.execute("DELETE FROM prosandcons WHERE company_id = %s", (company_id,))
    
    records = []
    for pro in pros:
        records.append((company_id, pro, None))
    for con in cons:
        records.append((company_id, None, con))

    query = "INSERT INTO prosandcons (company_id, pros, cons) VALUES (%s, %s, %s)"
    cursor.executemany(query, records)

def compute_growth(data_list, field):
    if len(data_list) < 2:
        return 0.0
    first = float(data_list[0].get(field, 0))
    last = float(data_list[-1].get(field, 0))
    if first <= 0:
        return 0.0
    return ((last - first) / first) * 100

def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    for file in os.listdir(PROCESSED_PATH):
        if not file.endswith(".json"):
            continue

        company_id = file.replace(".json", "")
        processed_file = os.path.join(PROCESSED_PATH, file)
        raw_file = os.path.join(RAW_PATH, f"{company_id}.json")

        with open(processed_file, "r", encoding="utf-8") as pf, open(raw_file, "r", encoding="utf-8") as rf:
            processed_data = json.load(pf)
            raw_data = json.load(rf)

        company = raw_data["company"]
        pros = processed_data.get("pros", [])
        cons = processed_data.get("cons", [])
        roe_percentage = company.get("roe_percentage")
        roe = float(roe_percentage) if roe_percentage is not None else 0.0

        pl = raw_data["data"].get("profitandloss", [])[-6:]
        sales_growth = compute_growth(pl, "sales")
        profit_growth = compute_growth(pl, "net_profit")

        try:
            insert_into_companies(cursor, company)
            insert_into_analysis(cursor, company_id, sales_growth, profit_growth, roe)
            insert_into_prosandcons(cursor, company_id, pros, cons)
            print(f"Inserted into all tables: {company_id}")
        except Exception as e:
            print(f"Error processing {company_id}: {str(e)}")
            continue

    conn.commit()
    conn.close()
    print("All companies inserted into MySQL.")

if __name__ == "__main__":
    main()
