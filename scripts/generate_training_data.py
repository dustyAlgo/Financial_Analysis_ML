# scripts/generate_training_data.py

import os
import sys
import pandas as pd
import mysql.connector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_CONFIG

def safe_float(val):
    """Safely convert value to float, return 0.0 if conversion fails"""
    try:
        return float(val)
    except:
        return 0.0

def fetch_company_data_from_db(cursor, company_id):
    """Fetch complete company data from database"""
    # Get company info
    cursor.execute("SELECT * FROM companies WHERE id=%s", (company_id,))
    company_row = cursor.fetchone()
    if not company_row:
        return None
    desc = [col[0] for col in cursor.description]
    company_dict = dict(zip(desc, company_row))
    
    # Get all financial data
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

def extract_features(company_data):
    """Extract financial features from company data"""
    roe = safe_float(company_data["company"].get("roe_percentage"))
    
    # Dividend payout: latest nonzero
    dividend_payout = 0
    for pl in reversed(company_data["data"].get("profitandloss", [])):
        payout = safe_float(pl.get("dividend_payout"))
        if payout > 0:
            dividend_payout = payout
            break
    
    # Sales growth (last 5 years)
    sales_data = company_data["data"].get("profitandloss", [])[-6:]
    sales_growth = 0
    if len(sales_data) >= 2:
        first = safe_float(sales_data[0].get("sales"))
        last = safe_float(sales_data[-1].get("sales"))
        if first > 0:
            sales_growth = ((last - first) / first) * 100
    
    # Debt ratio (latest year)
    bs = company_data["data"].get("balancesheet", [])
    debt_ratio = 0
    if bs:
        latest = bs[-1]
        borrowings = safe_float(latest.get("borrowings"))
        total_liabilities = safe_float(latest.get("total_liabilities"))
        debt_ratio = (borrowings / total_liabilities) if total_liabilities else 0
    
    return {
        "roe": roe,
        "dividend_payout": dividend_payout,
        "sales_growth": sales_growth,
        "debt_ratio": debt_ratio
    }

def extract_labels(cursor, company_id):
    """Extract labels from existing pros/cons data"""
    cursor.execute("SELECT pros FROM prosandcons WHERE company_id=%s", (company_id,))
    pros = []
    rows = cursor.fetchall()
    for row in rows:
        if row[0]:
            if isinstance(row[0], str):
                pros.extend(row[0].split('\n'))
            elif isinstance(row[0], list):
                pros.extend(row[0])
    
    return {
        "pro_roe": int(any("ROE" in p for p in pros)),
        "pro_dividend": int(any("dividend" in p for p in pros)),
        "pro_sales": int(any("sales growth" in p for p in pros)),
        "pro_debt": int(any("debt-free" in p for p in pros)),
    }

def main():
    """Main function to generate training data"""
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    
    features = []
    labels = []
    
    # Get all company IDs
    cursor.execute("SELECT id FROM companies")
    all_company_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"Processing {len(all_company_ids)} companies...")
    
    for company_id in all_company_ids:
        try:
            # Fetch company data
            company_data = fetch_company_data_from_db(cursor, company_id)
            if not company_data:
                print(f"Skipping {company_id}: not found in DB.")
                continue
            
            # Extract features
            feat = extract_features(company_data)
            feat["company_id"] = company_id
            features.append(feat)
            
            # Extract labels
            lab = extract_labels(cursor, company_id)
            lab["company_id"] = company_id
            labels.append(lab)
            
            print(f"Processed: {company_id}")
            
        except Exception as e:
            print(f"Error processing {company_id}: {type(e).__name__}: {e}")
    
    # Create DataFrames and merge
    df_feat = pd.DataFrame(features)
    df_lab = pd.DataFrame(labels)
    df = pd.merge(df_feat, df_lab, on="company_id")
    
    # Save to CSV
    df.to_csv("ml_training_data.csv", index=False)
    print(f"Training data saved to ml_training_data.csv")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {', '.join(df.columns)}")
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()