from flask import Flask, render_template, request
import mysql.connector
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config.config as config

app = Flask(__name__)

data_processed_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed'))

def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_CONFIG["host"],
        port=config.DB_CONFIG["port"],
        user=config.DB_CONFIG["user"],
        password=config.DB_CONFIG["password"],
        database=config.DB_CONFIG["database"]
    )

@app.route("/")
def home():
    """Homepage with company list"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all companies with basic info
    cursor.execute("""
        SELECT c.id, c.company_name, c.roe_percentage, 
               a.compounded_sales_growth, a.compounded_profit_growth,
               COUNT(pc.pros) as pros_count,
               COUNT(pc.cons) as cons_count
        FROM companies c
        LEFT JOIN analysis a ON c.id = a.company_id
        LEFT JOIN prosandcons pc ON c.id = pc.company_id
        GROUP BY c.id, c.company_name, c.roe_percentage, a.compounded_sales_growth, a.compounded_profit_growth
        ORDER BY c.company_name
        LIMIT 20
    """)
    
    companies = cursor.fetchall()
    
    # Get total count for stats
    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]
    
    # Count processed companies for ML insights
    try:
        processed_count = len([f for f in os.listdir(data_processed_path) if f.endswith('.json')])
    except Exception:
        processed_count = 0
    
    conn.close()
    
    return render_template("home.html", 
                         companies=companies, 
                         total_companies=total_companies,
                         processed_count=processed_count,
                         show_insights=processed_count >= 70)

@app.route("/company/<company_id>")
def company(company_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
    company = cursor.fetchone()

    cursor.execute("SELECT * FROM analysis WHERE company_id = %s", (company_id,))
    analysis = cursor.fetchone()

    cursor.execute("SELECT pros, cons FROM prosandcons WHERE company_id = %s", (company_id,))
    pros_cons = cursor.fetchall()

    conn.close()

    pros = [row[0] for row in pros_cons if row[0]]
    cons = [row[1] for row in pros_cons if row[1]]

    # Count processed companies
    try:
        processed_count = len([f for f in os.listdir(data_processed_path) if f.endswith('.json')])
    except Exception:
        processed_count = 0

    show_insights = processed_count >= 70

    return render_template("company.html", company=company, analysis=analysis, pros=pros, cons=cons, show_insights=show_insights, processed_count=processed_count)

@app.route("/companies")
def companies():
    """Full company listing page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get page parameter for pagination
    page = request.args.get('page', 1, type=int)
    per_page = 24  # 6x4 grid
    offset = (page - 1) * per_page
    
    # Get companies with pagination
    cursor.execute("""
        SELECT c.id, c.company_name, c.roe_percentage, 
               a.compounded_sales_growth, a.compounded_profit_growth,
               COUNT(pc.pros) as pros_count,
               COUNT(pc.cons) as cons_count
        FROM companies c
        LEFT JOIN analysis a ON c.id = a.company_id
        LEFT JOIN prosandcons pc ON c.id = pc.company_id
        GROUP BY c.id, c.company_name, c.roe_percentage, a.compounded_sales_growth, a.compounded_profit_growth
        ORDER BY c.company_name
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    
    companies = cursor.fetchall()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]
    
    # Calculate pagination info
    total_pages = (total_companies + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    conn.close()
    
    return render_template("companies.html", 
                         companies=companies,
                         total_companies=total_companies,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next)

if __name__ == "__main__":
    app.run(debug=True)
