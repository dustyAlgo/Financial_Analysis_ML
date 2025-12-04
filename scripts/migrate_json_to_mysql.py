import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import mysql.connector
from mysql.connector import Error
from config.config import DB_CONFIG


def get_connection():
    # You can tweak connection_timeout if needed
    return mysql.connector.connect(**DB_CONFIG)


def insert_company(cursor, company):
    sql = """
        INSERT INTO companies
        (id, company_logo, company_name, chart_link, about_company, website, nse_profile, bse_profile,
         face_value, book_value, roce_percentage, roe_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        company_logo=VALUES(company_logo), company_name=VALUES(company_name),
        chart_link=VALUES(chart_link), about_company=VALUES(about_company), website=VALUES(website),
        nse_profile=VALUES(nse_profile), bse_profile=VALUES(bse_profile),
        face_value=VALUES(face_value), book_value=VALUES(book_value),
        roce_percentage=VALUES(roce_percentage), roe_percentage=VALUES(roe_percentage)
    """
    vals = (
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
        company.get("roe_percentage"),
    )
    cursor.execute(sql, vals)


def insert_many(table, cursor, items, fields):
    if not items:
        return
    field_str = ', '.join(fields)
    value_str = ', '.join(['%s'] * len(fields))
    sql = f"INSERT IGNORE INTO {table} ({field_str}) VALUES ({value_str})"
    for item in items:
        vals = tuple(item.get(f) for f in fields)
        cursor.execute(sql, vals)


def process_file(raw_dir, fname):
    path = os.path.join(raw_dir, fname)
    print(f"\n📄 Processing {fname} ...")

    # Load JSON
    try:
        with open(path, encoding='utf-8') as fin:
            data = json.load(fin)
    except Exception as e:
        print(f"⚠️ Could not open or parse {fname}: {e}")
        return

    if "company" not in data:
        print(f"⚠️ Skipping {fname}: 'company' key not found.")
        return
    if "data" not in data:
        print(f"⚠️ Skipping {fname}: 'data' key not found.")
        return

    company = data["company"]
    dat = data.get("data", {})

    # New connection per file
    try:
        db = get_connection()
        cursor = db.cursor()

        db.start_transaction()
        insert_company(cursor, company)

        # Cashflow
        insert_many(
            "cashflow", cursor, dat.get("cashflow", []),
            ["id", "company_id", "year", "operating_activity", "investing_activity",
             "financing_activity", "net_cash_flow"]
        )
        # Balancesheet
        insert_many(
            "balancesheet", cursor, dat.get("balancesheet", []),
            ["id", "company_id", "year", "equity_capital", "reserves", "borrowings",
             "other_liabilities", "total_liabilities", "fixed_assets", "cwip",
             "investments", "other_asset", "total_assets"]
        )
        # Profit and Loss
        insert_many(
            "profitandloss", cursor, dat.get("profitandloss", []),
            ["id", "company_id", "year", "sales", "expenses", "operating_profit",
             "opm_percentage", "other_income", "interest", "depreciation",
             "profit_before_tax", "tax_percentage", "net_profit", "eps",
             "dividend_payout"]
        )
        # Pros and Cons
        insert_many(
            "prosandcons", cursor, dat.get("prosandcons", []),
            ["id", "company_id", "pros", "cons"]
        )
        # Analysis
        insert_many(
            "analysis", cursor, dat.get("analysis", []),
            ["id", "company_id", "compounded_sales_growth",
             "compounded_profit_growth", "stock_price_cagr", "roe"]
        )

        db.commit()
        print(f"✅ Imported {fname} successfully.")

    except Error as e:
        # If connection is lost mid-file, that file may be partial; rerun will fix thanks to
        # ON DUPLICATE KEY UPDATE + INSERT IGNORE
        print(f"❌ Error importing {fname}: {type(e).__name__}: {e}")
        try:
            db.rollback()
        except Exception:
            pass
    finally:
        try:
            cursor.close()
            db.close()
        except Exception:
            pass


def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    files = [f for f in os.listdir(raw_dir) if f.endswith('.json')]
    files.sort()  # deterministic order
    print(f"Found {len(files)} JSON files.")

    for fname in files:
        process_file(raw_dir, fname)

    print("\n🏁 Migration complete.")


if __name__ == "__main__":
    main()
