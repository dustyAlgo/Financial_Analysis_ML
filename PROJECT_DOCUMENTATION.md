# Financial Analysis ML Project Documentation

## Project Overview

This project implements a comprehensive financial analysis system using Machine Learning to analyze public company financials. The system uses a **fully database-driven architecture** - all company and financial data is stored in normalized MySQL tables, processed through ML algorithms, and displayed through a user-friendly web interface.

**Key Architecture Change**: This version has been refactored to use MySQL as the single source of truth. All data input, processing, and output operations are database-driven, eliminating dependency on JSON file reading during normal operations.

## System Architecture

```
┌─────────────────────────────────────────────────┐
│            MySQL Database                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │companies │  │cashflow  │  │balances  │     │
│  │balances  │  │profitloss│  │analysis  │     │
│  │proscons  │  └──────────┘  └──────────┘     │
└────────┬────────────────────────────────────────┘
         │
         ├─────────────────┬─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
│  ML Pipeline    │ │ Store Results│ │ Web Interface│
│  (analyze_data) │ │ (store_results)│ │  (app.py)   │
│  Reads from DB  │ │ Writes to DB │ │ Reads from DB│
└─────────────────┘ └──────────────┘ └──────────────┘
```

**Data Flow:**
1. **Initial Setup**: JSON files → Migration script → MySQL database
2. **Training Data**: MySQL database → Training data generation → ml_training_data.csv
3. **ML Training**: ml_training_data.csv → ML training → ml_pros_classifier.joblib
4. **Analysis**: MySQL database + ML model → ML analysis → Processed data
5. **Web Display**: MySQL database → Web Interface → User

## Project Structure

```
financial-analysis-ml/
├── main.py                 # Main orchestrator script (updated)
├── requirements.txt        # Python dependencies
├── config/
│   └── config.py          # Configuration settings
├── data/
│   ├── raw/              # Raw JSON data files
│   └── processed/        # ML-processed data
├── scripts/
│   ├── train_ml_classifier.py  # ML model training
│   ├── generate_training_data.py  # NEW: Training data generation from database
│   ├── analyze_data.py   # ML analysis script
│   └── store_results.py  # Database storage script
├── web/
│   ├── app.py           # Flask web application (enhanced)
│   └── templates/
│       ├── layout.html  # Base template (updated)
│       ├── home.html    # Homepage with company grid
│       ├── companies.html # All companies listing
│       └── company.html # Company analysis page (enhanced)
├── ml_pros_classifier.joblib  # Trained ML model
├── ml_training_data.csv       # ML training data
└── database_schema.sql        # Database schema
```

## Components Breakdown

### 1. Python Scripts: ML Pipeline (Updated)

#### `main.py` - Main Orchestrator
- **Purpose**: Coordinates the ML pipeline with database-driven data
- **Features**: 
  - Checks database for company data availability
  - Generates training data if needed (new feature)
  - Runs ML training, analysis, and storage
  - Starts web server after pipeline completion
  - Command-line options for different modes (`--pipeline-only`, `--web-only`)
  - Validates database connection and data before processing

#### `scripts/train_ml_classifier.py` - ML Training
- **Purpose**: Trains machine learning classifier
- **Features**:
  - Uses scikit-learn RandomForestClassifier
  - Trains on financial metrics (ROE, dividend payout, sales growth, debt ratio)
  - Loads training data from `ml_training_data.csv`
  - Saves trained model as `ml_pros_classifier.joblib`
  - Provides classification performance metrics

#### `scripts/migrate_json_to_mysql.py` - Data Migration
- **Purpose**: One-time migration of JSON files to MySQL database
- **Features**:
  - Reads all JSON files from `data/raw/` directory
  - Parses and normalizes company, financial, and analysis data
  - Inserts data into normalized MySQL tables
  - Handles errors gracefully with detailed logging
  - Supports resuming if migration fails partway

#### `scripts/analyze_data.py` - ML Analysis (Database-Driven)
- **Purpose**: Applies ML to generate insights from database data
- **Features**:
  - **Reads company and financial data directly from MySQL**
  - Extracts financial features from database records
  - Applies trained ML model for predictions
  - Generates pros/cons analysis using ML predictions
  - Saves processed data to `data/processed/` (optional, for compatibility)
  - Supports feature extraction for training data generation
  - Queries all companies from database instead of file system

#### `scripts/store_results.py` - Database Storage (Database-Driven)
- **Purpose**: Stores analysis results in MySQL using database data
- **Features**:
  - **Reads company and financial data from MySQL** (not JSON files)
  - Reads processed pros/cons from `data/processed/` files
  - Inserts/updates company data, analysis results, and pros/cons
  - Handles AUTO_INCREMENT primary keys properly
  - Supports data updates and duplicates
  - Calculates growth metrics from database historical data
  - Uses efficient database queries for data retrieval

#### `scripts/generate_training_data.py` - Training Data Generation
- **Purpose**: Extracts features and labels from database for ML training
- **Features**:
  - Reads company financial data directly from MySQL
  - Extracts ROE, dividend payout, sales growth, and debt ratio features
  - Generates labels from existing pros/cons data
  - Creates comprehensive training dataset
  - Saves to `ml_training_data.csv` for model training

### 2. Web Interface (Enhanced)

#### `web/app.py` - Flask Application (Database-Driven)
- **Purpose**: User-friendly web server for displaying insights from database
- **Features**:
  - **All data fetched directly from MySQL database**
  - Multiple routes for different pages (home, companies, company details, **search**)
  - Database integration with optimized queries and JOINs
  - **Search functionality with company name matching**
  - Pagination support for large datasets
  - Responsive design with Bootstrap 5
  - Company listing with database-driven counts
  - No dependency on file system for data display

#### Templates (Updated)
- **`layout.html`**: Base template with responsive navigation
- **`home.html`**: Homepage with company grid and dashboard stats
- **`companies.html`**: Full company listing with pagination
- **`company.html`**: Enhanced company analysis page with navigation
- **`search.html`**: **New search interface with results display**

**Key Features**: 
- ML insights are visible after analyzing 70+ companies
- User-friendly navigation with breadcrumbs
- **Search functionality for finding specific companies**
- Responsive design for mobile and desktop
- Professional dashboard appearance

### 3. Database Integration

#### MySQL Schema (Normalized)

The database uses a fully normalized schema with the following tables:

**Core Tables:**
- `companies` - Company metadata and basic information
- `cashflow` - Cash flow statements (one row per company per year)
- `balancesheet` - Balance sheets (one row per company per year)
- `profitandloss` - Profit & Loss statements (one row per company per year)
- `analysis` - ML-generated analysis results
- `prosandcons` - ML-generated pros and cons

**Key Features:**
- Normalized structure eliminates data redundancy
- Foreign key relationships ensure data integrity
- Indexed for optimal query performance
- Supports historical data tracking (multiple years per company)

**Complete Schema:**
See `database_schema.sql` for the full CREATE TABLE statements with all fields, indexes, and constraints.

## Setup Instructions

### Prerequisites
1. Python 3.8+
2. MySQL Server (running and accessible)
3. Virtual environment (recommended)
4. Raw JSON data files in `data/raw/` directory (for initial migration)

### Installation

1. **Clone and Setup Environment**
   ```bash
   git clone <repository-url>
   cd financial-analysis-ml
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   pip install flask mysql-connector-python  # Web interface and database
   ```

2. **Database Setup**
   ```bash
   # Option 1: Using command line
   mysql -u root -p < database_schema.sql
   
   # Option 2: Using MySQL Workbench
   # Open database_schema.sql and execute all statements
   
   # Option 3: Manual setup
   # CREATE DATABASE ml; (or ml_test for testing)
   # USE ml;
   # Copy and run all CREATE TABLE statements from database_schema.sql
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

5. **Generate Training Data** (Optional - if ml_training_data.csv doesn't exist)
   ```bash
   python scripts/generate_training_data.py
   ```

6. **Run the Pipeline**
   ```bash
   # Complete pipeline + web server
   python main.py
   ```

## Usage Guide

### Running the Complete System
```bash
# Run entire pipeline + web server
python main.py

# Run only ML pipeline
python main.py --pipeline-only

# Start only web server
python main.py --web-only
```

### Individual Scripts
```bash
# Generate training data from database
python scripts/generate_training_data.py

# Train ML model
python scripts/train_ml_classifier.py

# Analyze data
python scripts/analyze_data.py

# Store in database
python scripts/store_results.py
```

### Web Interface (Enhanced)
- **Homepage**: `http://localhost:5000` - Company grid with dashboard stats
- **All Companies**: `http://localhost:5000/companies` - Full company listing with pagination
- **Company Details**: `http://localhost:5000/company/<company_id>` - Detailed analysis
- **Search**: `http://localhost:5000/search` - **Search companies by name**
- **Features**: Responsive design, breadcrumb navigation, professional dashboard, **search functionality**
- **ML insights** appear after 70+ companies analyzed

### 4. Search Functionality (New)

#### Search Implementation
- **Route**: `/search` - Handles search queries and results
- **Features**:
  - **Company name search** using SQL LIKE operator for partial matching
  - **Empty search state** shows clean search interface
  - **No results messaging** when no matches found
  - **Consistent styling** with rest of application
  - **Database-driven** results from MySQL queries

#### Technical Details
- Uses parameterized queries for security
- Implements case-insensitive search through database collation
- Returns same company card format as homepage for consistency
- Supports search from navigation and quick actions

## ML Algorithm Details

### Features Used
1. **ROE (Return on Equity)**: 3-year average
2. **Dividend Payout**: Latest non-zero value
3. **Sales Growth**: 5-year compounded growth
4. **Debt Ratio**: Borrowings to total liabilities ratio

### Classification Output
- **Pros**: Positive financial indicators
- **Cons**: Areas of concern
- **Confidence**: Based on historical performance patterns

### Model Performance
- Uses Random Forest Classifier
- Trained on historical financial data
- Provides interpretable results

## Data Processing

### Data Source
- **Raw Data**: JSON files in `data/raw/` directory
- **Format**: Structured JSON with company information and financial data
- **Processing**: ML analysis applied to generate insights

### Data Flow
- Raw JSON files → ML Analysis → Processed insights → MySQL storage → Web display
- No external API dependencies
- Focus on ML processing and user-friendly presentation

## Error Handling

### Common Issues
1. **Database Connection**: Check MySQL credentials in config
2. **Missing Data Files**: Ensure raw JSON files exist in `data/raw/`
3. **Missing Dependencies**: Ensure all packages installed (including Flask)
4. **ML Training Data**: Verify `ml_training_data.csv` exists
5. **File Permissions**: Check write access to data directories

### Debugging
- Enable debug mode in Flask: `app.run(debug=True)`
- Check logs in console output
- Verify data files in `data/` directories

## Performance Considerations

### Optimization
- Batch processing for large datasets
- Database indexing for faster queries
- Caching for frequently accessed data
- Connection pooling for database

### Scalability
- Modular design allows component scaling
- Separate web and processing servers
- Database optimization for large datasets

## Security Considerations

### Data Protection
- API keys stored in configuration
- Database credentials secured
- Input validation on web forms
- SQL injection prevention

### Access Control
- Web interface for read-only access
- Database access limited to application
- No sensitive data in client-side code

## Future Enhancements

### Planned Features
1. **Real-time Updates**: Live data streaming
2. **Advanced Analytics**: More ML models
3. **User Authentication**: Multi-user support
4. **API Endpoints**: RESTful API for external access
5. **Dashboard**: Interactive charts and graphs
6. **Advanced Search**: **Filter by financial metrics, industry, etc.**

### Technical Improvements
1. **Microservices**: Separate services for different components
2. **Containerization**: Docker deployment
3. **Cloud Integration**: AWS/Azure deployment
4. **Monitoring**: Application performance monitoring

## Team Collaboration

### Development Workflow
1. **Feature Branches**: Create for new features
2. **Code Review**: Peer review before merging
3. **Testing**: Unit tests for critical functions
4. **Documentation**: Update docs with changes

### Communication
- Use issue tracking for bugs/features
- Regular team meetings for progress updates
- Code comments for complex logic
- README updates for setup changes

## Troubleshooting

### Quick Fixes
1. **Reset Database**: Drop and recreate tables
2. **Clear Cache**: Remove processed data files
3. **Restart Services**: Restart MySQL and Flask
4. **Check Logs**: Review console output for errors

### Support
- Check documentation first
- Review error messages carefully
- Test individual components
- Contact team lead for complex issues

---

**Last Updated**: December 2025  
**Version**: 1.2  **# Updated from 1.0 to reflect new feature**
**Owner**: Mrityunjay Bhagat