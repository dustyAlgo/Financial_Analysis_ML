# Financial Analysis ML Project Documentation

## Project Overview

This project implements a comprehensive financial analysis system using Machine Learning to analyze public company financials. The system fetches financial data, applies ML algorithms to generate insights, stores results in MySQL, and displays them through a web interface.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Source   │    │   ML Pipeline   │    │   Web Interface │
│   (API/Excel)   │───▶│   (Python)      │───▶│   (Flask)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   MySQL DB      │
                       │   (Storage)     │
                       └─────────────────┘
```

## Project Structure

```
financial-analysis-ml/
├── main.py                 # Main orchestrator script
├── requirements.txt        # Python dependencies
├── config/
│   └── config.py          # Configuration settings
├── data/
│   ├── companies.xlsx  # Company list (your own or sample)
│   ├── raw/              # Raw API data
│   └── processed/        # ML-processed data
├── scripts/
│   ├── fetch_data.py     # Data fetching script
│   ├── train_ml_classifier.py  # ML model training
│   ├── analyze_data.py   # ML analysis script
│   └── store_results.py  # Database storage script
├── web/
│   ├── app.py           # Flask web application
│   └── templates/
│       ├── layout.html  # Base template
│       └── company.html # Company analysis page
└── models/              # Trained ML models
```

## Components Breakdown

### 1. Python Scripts: Fetch, ML, and Store

#### `main.py` - Main Orchestrator
- **Purpose**: Coordinates the entire ML pipeline
- **Features**: 
  - Runs data fetching, ML training, analysis, and storage
  - Starts web server after pipeline completion
  - Command-line options for different modes

#### `scripts/fetch_data.py` - Data Fetching
- **Purpose**: Retrieves financial data from API
- **Features**:
  - Reads company IDs from Excel file
  - Fetches data from financial API
  - Saves raw JSON data to `data/raw/`

#### `scripts/train_ml_classifier.py` - ML Training
- **Purpose**: Trains machine learning classifier
- **Features**:
  - Uses scikit-learn for classification
  - Trains on financial metrics (ROE, dividend payout, sales growth, debt ratio)
  - Saves trained model as `ml_pros_classifier.joblib`

#### `scripts/analyze_data.py` - ML Analysis
- **Purpose**: Applies ML to generate insights
- **Features**:
  - Extracts financial features from raw data
  - Applies trained ML model for predictions
  - Generates pros/cons analysis
  - Saves processed data to `data/processed/`

#### `scripts/store_results.py` - Database Storage
- **Purpose**: Stores analysis results in MySQL
- **Features**:
  - Connects to MySQL database
  - Inserts company data, analysis results, and pros/cons
  - Handles data updates and duplicates

### 2. Web Interface

#### `web/app.py` - Flask Application
- **Purpose**: Web server for displaying insights
- **Features**:
  - RESTful API endpoints
  - Database integration
  - Template rendering
  - Company-specific analysis pages

#### Templates
- **`layout.html`**: Base template with Bootstrap styling
- **`company.html`**: Company analysis page with ML insights

**Key Feature**: ML insights are only visible after analyzing 100+ companies, ensuring data quality and meaningful analysis.

### 3. Database Integration

#### MySQL Schema
```sql
-- Companies table
CREATE TABLE companies (
    id VARCHAR(50) PRIMARY KEY,
    company_logo TEXT,
    company_name VARCHAR(255),
    chart_link TEXT,
    about_company TEXT,
    website VARCHAR(255),
    nse_profile VARCHAR(255),
    bse_profile VARCHAR(255),
    face_value DECIMAL(10,2),
    book_value DECIMAL(10,2),
    roce_percentage DECIMAL(5,2),
    roe_percentage DECIMAL(5,2)
);

-- Analysis results
CREATE TABLE analysis (
    id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50),
    compounded_sales_growth VARCHAR(20),
    compounded_profit_growth VARCHAR(20),
    stock_price_cagr VARCHAR(20),
    roe VARCHAR(20),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- ML-generated pros and cons
CREATE TABLE prosandcons (
    id INT PRIMARY KEY,
    company_id VARCHAR(50),
    pros TEXT,
    cons TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

## Setup Instructions

### Prerequisites
1. Python 3.8+
2. MySQL Server
3. Virtual environment (recommended)

### Installation

1. **Clone and Setup Environment**
   ```bash
   git clone <repository-url>
   cd financial-analysis-ml
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```sql
   CREATE DATABASE ml;
   USE ml;
   -- Run the schema creation scripts above
   ```

3. **Configuration**
   - Edit `config/config.py` with your MySQL credentials
   - Update API key if required

4. **Run the Pipeline**
   ```bash
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
# Fetch data only
python scripts/fetch_data.py

# Train ML model
python scripts/train_ml_classifier.py

# Analyze data
python scripts/analyze_data.py

# Store in database
python scripts/store_results.py
```

### Web Interface
- Access at: `http://localhost:5000`
- Navigate to company pages: `http://localhost:5000/company/<company_id>`
- ML insights appear after 100+ companies analyzed

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

## API Integration

### Data Source
- **API Endpoint**: `https://api.example.com/company` (configure your own)
- **Authentication**: API key required
- **Data Format**: JSON response with financial metrics

### Rate Limiting
- Implemented delays between requests
- Error handling for API failures
- Retry mechanism for failed requests

## Error Handling

### Common Issues
1. **Database Connection**: Check MySQL credentials in config
2. **API Failures**: Verify API key and network connectivity
3. **Missing Dependencies**: Ensure all packages installed
4. **File Permissions**: Check write access to data directories

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

**Last Updated**: December 2024  
**Version**: 1.0  
**Owner**: Your Name