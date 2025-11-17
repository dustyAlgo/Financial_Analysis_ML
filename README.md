# Financial Analysis ML Project

A comprehensive financial analysis system using Machine Learning to analyze public company financials. The system uses a **fully database-driven architecture** - all company and financial data is stored in MySQL, processed through ML algorithms, and displayed through a user-friendly web interface.

**🚀 Key Features**: 
- **Database-Driven Architecture**: All data stored in normalized MySQL tables
- **Enhanced Web Interface**: Company browsing, pagination, and responsive design
- **ML-Powered Analysis**: Automated pros/cons generation using Random Forest

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server (running and accessible)
- Virtual environment (recommended)
- Raw JSON data files (for initial migration)

### Installation

1. **Setup Environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   pip install flask mysql-connector-python  # For web interface and database
   ```

2. **Database Setup**
   ```bash
   # Create database and tables
   mysql -u root -p < database_schema.sql
   
   # Or manually:
   # CREATE DATABASE ml; (or ml_test for testing)
   # USE ml;
   # Run all CREATE TABLE statements from database_schema.sql
   ```

3. **Configuration**
   - Edit `config/config.py` with your MySQL credentials:
     ```python
     DB_CONFIG = {
         "host": "localhost",
         "port": 3306,
         "user": "root",
         "password": "your_password",
         "database": "ml"  # or "ml_test" for testing
     }
     ```

4. **Migrate Data to Database (One-Time)**
   ```bash
   # Import all JSON files from data/raw/ into MySQL
   python scripts/migrate_json_to_mysql.py
   ```

5. **Run the System**
   ```bash
   # Complete pipeline + web server
   python main.py
   ```

## 📁 Project Structure

```
financial-analysis-ml/
├── main.py                      # Main orchestrator (database-driven)
├── scripts/                      # Python scripts
│   ├── migrate_json_to_mysql.py # One-time JSON to DB migration
│   ├── train_ml_classifier.py   # ML model training
│   ├── analyze_data.py          # ML analysis (reads from DB)
│   └── store_results.py         # Store results (reads/writes DB)
├── web/                         # Enhanced Flask web interface
│   ├── app.py                   # Web server (database-driven)
│   └── templates/                # HTML templates
├── config/                      # Configuration files
│   └── config.py                # MySQL connection settings
├── data/                        # Data directories
│   ├── raw/                     # Original JSON files (for migration)
│   └── processed/               # ML-processed results (optional)
├── database_schema.sql          # MySQL database schema
├── ml_pros_classifier.joblib    # Trained ML model
└── ml_training_data.csv         # ML training data
```

## 🔧 Usage

### First-Time Setup
```bash
# 1. Migrate JSON data to database (one-time)
python scripts/migrate_json_to_mysql.py

# 2. Run complete pipeline
python main.py
```

### Complete Pipeline
```bash
python main.py  # Runs ML pipeline + starts web server
```

### Individual Components
```bash
# Run only ML pipeline (no web server)
python main.py --pipeline-only

# Start only web server (skip pipeline)
python main.py --web-only

# Run individual scripts
python scripts/analyze_data.py      # Analyze companies from DB
python scripts/store_results.py      # Store results to DB
python scripts/train_ml_classifier.py  # Train ML model
```

### Web Interface (Enhanced)
- **Homepage**: `http://localhost:5000` - Company grid with dashboard stats
- **All Companies**: `http://localhost:5000/companies` - Full listing with pagination
- **Company Details**: `http://localhost:5000/company/<company_id>` - Detailed analysis
- **Features**: Responsive design, breadcrumb navigation, professional dashboard
- **ML insights** visible after analyzing 70+ companies

## 📊 Features

- **ML Analysis**: Financial metrics classification with Random Forest
- **Database Storage**: MySQL integration with optimized queries
- **Web Interface**: Enhanced Bootstrap 5 dashboard with responsive design
- **Company Browsing**: Grid layout with pagination and search-ready structure
- **Insights**: ML-generated pros/cons analysis
- **Navigation**: Breadcrumb trails and user-friendly navigation
- **Mobile Support**: Responsive design for all devices

## 🌐 Enhanced Web Interface

### New User Experience
- **🏠 Homepage**: Company grid with key metrics and dashboard stats
- **📋 All Companies**: Paginated listing with enhanced company cards
- **🔍 Company Details**: Detailed analysis with breadcrumb navigation
- **📱 Responsive**: Works perfectly on desktop, tablet, and mobile
- **🧭 Navigation**: Easy browsing with breadcrumbs and back buttons

### Key Improvements
- **Professional Design**: Bootstrap 5 with modern styling
- **User-Friendly**: No need to know company IDs - browse visually
- **Performance**: Optimized database queries with pagination
- **Accessibility**: Proper navigation and mobile support

## 📚 Documentation

For detailed documentation, see `PROJECT_DOCUMENTATION.md`

## 🛠️ Troubleshooting

### Database Issues
- **"No companies found in database"**: Run migration first: `python scripts/migrate_json_to_mysql.py`
- **"Error connecting to database"**: 
  - Check MySQL is running: `mysql -u root -p`
  - Verify credentials in `config/config.py`
  - Test connection manually

### Missing Files
- **"ml_training_data.csv not found"**: Script will auto-generate or train model if missing
- **"ml_pros_classifier.joblib not found"**: Model will be auto-trained on first run

### Dependencies
- Install missing packages: `pip install flask mysql-connector-python`
- Activate virtual environment before running scripts

### General
- Check console output for detailed error messages
- Verify database schema is created: `SHOW TABLES;` in MySQL
- See `RUN_INSTRUCTIONS.md` for detailed setup guide

## 🤝 Team Collaboration

- Use feature branches for development
- Update documentation with changes
- Test components individually
- Review code before merging

---

## 🗄️ Database Architecture

This project uses a **fully normalized MySQL database** as the single source of truth:

- **Input Data**: All company and financial data stored in normalized tables
- **Processing**: ML pipeline reads directly from database
- **Output**: Results stored back in database
- **Web Interface**: Displays data directly from database

**Key Tables:**
- `companies` - Company metadata
- `cashflow` - Cash flow statements (by year)
- `balancesheet` - Balance sheets (by year)
- `profitandloss` - P&L statements (by year)
- `analysis` - ML-generated analysis results
- `prosandcons` - ML-generated pros/cons

See `database_schema.sql` for complete schema.

---

**Version**: 2.0 (Database-Driven) | **Last Updated**: December 2024 