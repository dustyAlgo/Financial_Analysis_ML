from flask import Flask, render_template, request
import mysql.connector
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

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
    
    # Count processed companies (those with pros/cons data) for ML insights
    cursor.execute("SELECT COUNT(DISTINCT company_id) FROM prosandcons")
    processed_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template("home.html", 
                         companies=companies, 
                         total_companies=total_companies,
                         processed_count=processed_count,
                         show_insights=processed_count >= 70)

@app.route("/company/<company_id>")
def company(company_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
        company = cursor.fetchone()
        
        if not company:
            cursor.close()
            conn.close()
            return f"Company '{company_id}' not found", 404

        cursor.execute("SELECT * FROM analysis WHERE company_id = %s", (company_id,))
        analysis = cursor.fetchone()

        cursor.execute("SELECT pros, cons FROM prosandcons WHERE company_id = %s", (company_id,))
        pros_cons = cursor.fetchall()

        # Count processed companies (those with pros/cons data) for ML insights
        cursor.execute("SELECT COUNT(DISTINCT company_id) as count FROM prosandcons")
        processed_count = cursor.fetchone()['count']

        cursor.close()
        conn.close()

        # Extract pros and cons from database results
        pros = []
        cons = []
        for row in pros_cons:
            if row.get('pros'):
                pros.append(row['pros'])
            if row.get('cons'):
                cons.append(row['cons'])

        show_insights = processed_count >= 70

        return render_template("company.html", 
                             company=company, 
                             analysis=analysis, 
                             pros=pros, 
                             cons=cons, 
                             show_insights=show_insights, 
                             processed_count=processed_count)
    except Exception as e:
        try:
            cursor.close()
        except:
            pass
        conn.close()
        return f"Error loading company data: {str(e)}", 500

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

@app.route("/search")
def search():
    """Search companies by name"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template("search.html", query=None, companies=None)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Search for companies matching the query
    cursor.execute("""
        SELECT c.id, c.company_name, c.roe_percentage, 
               a.compounded_sales_growth, a.compounded_profit_growth,
               COUNT(pc.pros) as pros_count,
               COUNT(pc.cons) as cons_count
        FROM companies c
        LEFT JOIN analysis a ON c.id = a.company_id
        LEFT JOIN prosandcons pc ON c.id = pc.company_id
        WHERE c.company_name LIKE %s
        GROUP BY c.id, c.company_name, c.roe_percentage, a.compounded_sales_growth, a.compounded_profit_growth
        ORDER BY c.company_name
    """, (f"%{query}%",))
    
    companies = cursor.fetchall()
    conn.close()
    
    return render_template("search.html", query=query, companies=companies)

if __name__ == "__main__":
    app.run(debug=True)
