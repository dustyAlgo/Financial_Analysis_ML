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
    return render_template("layout.html")

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

    show_insights = processed_count >= 100

    return render_template("company.html", company=company, analysis=analysis, pros=pros, cons=cons, show_insights=show_insights, processed_count=processed_count)

if __name__ == "__main__":
    app.run(debug=True)
