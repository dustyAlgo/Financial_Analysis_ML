# scripts/analyze_data.py

import os
import sys
import json
import mysql.connector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_CONFIG

PROCESSED_DATA_PATH = "data/processed"
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def safe_float(val):
    try:
        return float(val)
    except:
        return 0.0

def evaluate_metrics_ml(data, clf):
    # Extract features as in extraction
    roe = safe_float(data["company"].get("roe_percentage"))
    # Dividend payout: latest nonzero
    dividend_payout = 0
    for pl in reversed(data["data"].get("profitandloss", [])):
        payout = safe_float(pl.get("dividend_payout"))
        if payout > 0:
            dividend_payout = payout
            break
    # Sales growth (last 5 years)
    sales_data = data["data"].get("profitandloss", [])[-6:]
    sales_growth = 0
    if len(sales_data) >= 2:
        first = safe_float(sales_data[0].get("sales"))
        last = safe_float(sales_data[-1].get("sales"))
        if first > 0:
            sales_growth = ((last - first) / first) * 100
    # Debt ratio (latest year)
    bs = data["data"].get("balancesheet", [])
    debt_ratio = 0
    if bs:
        latest = bs[-1]
        borrowings = safe_float(latest.get("borrowings"))
        total_liabilities = safe_float(latest.get("total_liabilities"))
        debt_ratio = (borrowings / total_liabilities) if total_liabilities else 0
    # Predict pros
    X = [[roe, dividend_payout, sales_growth, debt_ratio]]
    preds = clf.predict(X)[0]
    pros = []
    cons = []
    # Map predictions to text (same as before)
    if preds[0]:
        pros.append(f"Company has a good ROE track record: 3 Years ROE {roe:.1f}%")
    else:
        cons.append(f"Company has a low return on equity of {roe:.1f}% over last 3 years.")
    if preds[1]:
        pros.append(f"Company has maintained a healthy dividend payout of {dividend_payout:.1f}%")
    else:
        cons.append("Company is not paying out dividend.")
    if preds[2]:
        pros.append(f"Company has shown strong sales growth of {sales_growth:.2f}% over last 5 years")
    else:
        cons.append(f"Company has delivered poor sales growth of {sales_growth:.2f}% over last 5 years")
    if preds[3]:
        pros.append("Company is almost debt-free.")
    elif debt_ratio > 0.5:
        cons.append("Company has high debt levels compared to liabilities.")
    return pros[:3], cons[:3]

def fetch_company_data_from_db(cursor, company_id):
    # Get company info
    cursor.execute("SELECT * FROM companies WHERE id=%s", (company_id,))
    company_row = cursor.fetchone()
    if not company_row:
        return None
    desc = [col[0] for col in cursor.description]
    company_dict = dict(zip(desc, company_row))
    # Get all cashflow, balancesheet, profitandloss rows for this company_id
    def fetch_table(table, flds=None):
        qfields = '*' if not flds else ', '.join(flds)
        cursor.execute(f"SELECT {qfields} FROM {table} WHERE company_id=%s ORDER BY year", (company_id,))
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    data_dict = {
        'cashflow': fetch_table('cashflow'),
        'balancesheet': fetch_table('balancesheet'),
        'profitandloss': fetch_table('profitandloss')
    }
    return {'company': company_dict, 'data': data_dict}

def extract_features_and_labels():
    import pandas as pd
    features = []
    labels = []
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    # Get all company IDs
    cursor.execute("SELECT id FROM companies")
    all_company_ids = [row[0] for row in cursor.fetchall()]
    for company_id in all_company_ids:
        full_data = fetch_company_data_from_db(cursor, company_id)
        if not full_data:
            print(f"Skipping {company_id}: not found in DB.")
            continue
        # --- Feature extraction --- (based on previous logic)
        roe = safe_float(full_data["company"].get("roe_percentage"))
        dividend_payout = 0
        for pl in reversed(full_data["data"].get("profitandloss", [])):
            payout = safe_float(pl.get("dividend_payout"))
            if payout > 0:
                dividend_payout = payout
                break
        sales_data = full_data["data"].get("profitandloss", [])[-6:]
        sales_growth = 0
        if len(sales_data) >= 2:
            first = safe_float(sales_data[0].get("sales"))
            last = safe_float(sales_data[-1].get("sales"))
            if first > 0:
                sales_growth = ((last - first) / first) * 100
        bs = full_data["data"].get("balancesheet", [])
        debt_ratio = 0
        if bs:
            latest = bs[-1]
            borrowings = safe_float(latest.get("borrowings"))
            total_liabilities = safe_float(latest.get("total_liabilities"))
            debt_ratio = (borrowings / total_liabilities) if total_liabilities else 0
        features.append({
            "company_id": company_id,
            "roe": roe,
            "dividend_payout": dividend_payout,
            "sales_growth": sales_growth,
            "debt_ratio": debt_ratio
        })
        # --- Label extraction ---
        # If processed data (pros/cons) is needed, could be loaded from prosandcons table if desired
        cursor.execute("SELECT pros FROM prosandcons WHERE company_id=%s", (company_id,))
        pros = []
        rows = cursor.fetchall()
        for row in rows:
            if row[0]:
                if isinstance(row[0], str):
                    pros.extend(row[0].split('\n'))
                elif isinstance(row[0], list):
                    pros.extend(row[0])
        labels.append({
            "company_id": company_id,
            "pro_roe": int(any("ROE" in p for p in pros)),
            "pro_dividend": int(any("dividend" in p for p in pros)),
            "pro_sales": int(any("sales growth" in p for p in pros)),
            "pro_debt": int(any("debt-free" in p for p in pros)),
        })
    df_feat = pd.DataFrame(features)
    df_lab = pd.DataFrame(labels)
    df = pd.merge(df_feat, df_lab, on="company_id")
    df.to_csv("ml_training_data.csv", index=False)
    print("✅ Extracted features and labels to ml_training_data.csv")
    cursor.close()
    db.close()

def main():
    import joblib
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    clf = joblib.load("ml_pros_classifier.joblib")
    cursor.execute("SELECT id FROM companies")
    all_company_ids = [row[0] for row in cursor.fetchall()]
    for company_id in all_company_ids:
        try:
            full_data = fetch_company_data_from_db(cursor, company_id)
            if not full_data:
                print(f"⚠️ Skipping {company_id}: not found in DB.")
                continue
            pros, cons = evaluate_metrics_ml(full_data, clf)
            result = {
                "company_id": company_id,
                "pros": pros,
                "cons": cons
            }
            # Optionally write to processed file (or could be inserted into DB later)
            out_path = os.path.join(PROCESSED_DATA_PATH, f"{company_id}.json")
            with open(out_path, "w", encoding="utf-8") as out_f:
                json.dump(result, out_f, indent=4)
            print(f"✅ Analyzed: {company_id}")
        except Exception as e:
            print(f"Error processing {company_id}: {type(e).__name__}: {e}")
    cursor.close()
    db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true", help="Extract features and labels for ML training")
    args = parser.parse_args()
    if args.extract:
        extract_features_and_labels()
    else:
        main()
