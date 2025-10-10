# scripts/analyze_data.py

import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

RAW_DATA_PATH = "data/raw"
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

def extract_features_and_labels():
    import pandas as pd
    features = []
    labels = []
    files = os.listdir(RAW_DATA_PATH)
    for filename in files:
        if not filename.endswith(".json"): continue
        company_id = filename.replace(".json", "")
        raw_path = os.path.join(RAW_DATA_PATH, filename)
        processed_path = os.path.join(PROCESSED_DATA_PATH, filename)
        if not os.path.exists(processed_path): continue
        with open(raw_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        with open(processed_path, "r", encoding="utf-8") as f:
            processed = json.load(f)
        # --- Feature extraction ---
        roe = safe_float(raw["company"].get("roe_percentage"))
        # Dividend payout: latest nonzero
        dividend_payout = 0
        for pl in reversed(raw["data"].get("profitandloss", [])):
            payout = safe_float(pl.get("dividend_payout"))
            if payout > 0:
                dividend_payout = payout
                break
        # Sales growth (last 5 years)
        sales_data = raw["data"].get("profitandloss", [])[-6:]
        sales_growth = 0
        if len(sales_data) >= 2:
            first = safe_float(sales_data[0].get("sales"))
            last = safe_float(sales_data[-1].get("sales"))
            if first > 0:
                sales_growth = ((last - first) / first) * 100
        # Debt ratio (latest year)
        bs = raw["data"].get("balancesheet", [])
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
        # --- Label extraction (pros only) ---
        pros = processed.get("pros", [])
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

def main():
    files = os.listdir(RAW_DATA_PATH)
    import joblib
    clf = joblib.load("ml_pros_classifier.joblib")
    for filename in files:
        if not filename.endswith(".json"):
            continue
        company_id = filename.replace(".json", "")
        filepath = os.path.join(RAW_DATA_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "company" not in data:
            print(f"⚠️ Skipping {company_id}: missing 'company' key")
            continue
        pros, cons = evaluate_metrics_ml(data, clf)
        result = {
            "company_id": company_id,
            "pros": pros,
            "cons": cons
        }
        # Save to processed directory
        out_path = os.path.join(PROCESSED_DATA_PATH, f"{company_id}.json")
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=4)
        print(f"✅ Analyzed: {company_id}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true", help="Extract features and labels for ML training")
    args = parser.parse_args()
    if args.extract:
        extract_features_and_labels()
    else:
        main()
