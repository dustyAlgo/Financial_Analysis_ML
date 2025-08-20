import os
import sys
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

def connect_to_db():
    return mysql.connector.connect(
        host=config.DB_CONFIG["host"],
        port=config.DB_CONFIG["port"],
        user=config.DB_CONFIG["user"],
        password=config.DB_CONFIG["password"],
        database=config.DB_CONFIG["database"]
    )

def display_company_analysis(company_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch from companies
    cursor.execute("SELECT company_name, roe_percentage FROM companies WHERE id = %s", (company_id,))
    company = cursor.fetchone()

    # Fetch from analysis
    cursor.execute("""
        SELECT compounded_sales_growth, compounded_profit_growth, roe
        FROM analysis WHERE company_id = %s
    """, (company_id,))
    analysis = cursor.fetchone()

    # Fetch from prosandcons
    cursor.execute("""
        SELECT pros, cons FROM prosandcons WHERE company_id = %s
    """, (company_id,))
    pros_cons = cursor.fetchall()

    print(f"\n📊 Analysis for: {company[0]} ({company_id})")
    print(f"ROE: {company[1]}%")

    print("\n🔍 Financial Metrics:")
    headers = ["Sales Growth", "Profit Growth", "ROE"]
    print(tabulate([analysis], headers=headers, tablefmt="pretty"))

    pros = [row[0] for row in pros_cons if row[0]]
    cons = [row[1] for row in pros_cons if row[1]]

    print("\n✅ Pros:")
    for pro in pros:
        print(f" - {pro}")

    print("\n⚠️ Cons:")
    for con in cons:
        print(f" - {con}")

    conn.close()

def main():
    company_id = input("Enter a company ID (e.g., ABB): ").strip().upper()
    display_company_analysis(company_id)

if __name__ == "__main__":
    main()
