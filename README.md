# Financial Analysis ML Project

A comprehensive financial analysis system using Machine Learning to analyze public company financials. The system processes existing financial data, applies ML algorithms, stores results in MySQL, and displays insights through a user-friendly web interface.

**🚀 New Features**: Enhanced web interface with company browsing, pagination, and responsive design!

##  Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- Virtual environment (recommended)
- Existing raw JSON data in `data/raw/` directory

### Installation

1. **Setup Environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   pip install flask  # For web interface
   ```

2. **Database Setup**
   ```sql
   CREATE DATABASE ml;
   USE ml;
   ```
   Run the schema from `PROJECT_DOCUMENTATION.md`

3. **Configuration**
   - Edit `config/config.py` with your MySQL credentials
   - Ensure raw JSON data files are in `data/raw/` directory
   - Ensure `ml_training_data.csv` exists for ML training

4. **Run the System**
   ```bash
   python main.py
   ```

## Project Structure

```
financial-analysis-ml/
├── main.py                 # Main orchestrator (updated)
├── scripts/               # Python scripts (ML, analyze, store)
├── web/                   # Enhanced Flask web interface
├── config/               # Configuration files
├── data/                 # Raw and processed data
├── ml_pros_classifier.joblib  # Trained ML model
├── ml_training_data.csv       # ML training data
└── database_schema.sql        # Database schema
```

##  Usage

### Complete Pipeline
```bash
python main.py  # Runs everything + starts web server
```

### Individual Components
```bash
python main.py --pipeline-only  # ML pipeline only
python main.py --web-only       # Web server only
```

### Web Interface (Enhanced)
- **Homepage**: `http://localhost:5000` - Company grid with dashboard stats
- **All Companies**: `http://localhost:5000/companies` - Full listing with pagination
- **Company Details**: `http://localhost:5000/company/<company_id>` - Detailed analysis
- **Features**: Responsive design, breadcrumb navigation, professional dashboard
- **ML insights** visible after analyzing 70+ companies

## Features

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

## 🛠️ Troubleshooting

- Check MySQL connection in `config/config.py`
- Ensure raw JSON data files exist in `data/raw/`
- Verify `ml_training_data.csv` exists for ML training
- Install Flask: `pip install flask`
- Ensure all dependencies installed
- Check console output for error messages
