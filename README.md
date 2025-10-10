# Financial Analysis ML Project

A comprehensive financial analysis system using Machine Learning to analyze public company financials. The system fetches financial data, applies ML algorithms, stores results in MySQL, and displays insights through a web interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- Virtual environment (recommended)

### Installation

1. **Setup Environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```sql
   CREATE DATABASE ml;
   USE ml;
   ```
   Run the schema from `PROJECT_DOCUMENTATION.md`

3. **Configuration**
   - Edit `config/config.py` with your MySQL credentials
   - Set `API_BASE_URL` to your data provider and add your `API_KEY`
   - Set `COMPANY_LIST_PATH` (defaults to `data/companies.xlsx`)

5. **Create Companies Template (optional)**
   ```bash
   python scripts/create_companies_template.py
   ```
   Then fill the `company_id` column with your IDs.

4. **Run the System**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
financial-analysis-ml/
├── main.py                 # Main orchestrator
├── scripts/               # Python scripts (fetch, ML, store)
├── web/                   # Flask web interface
├── config/               # Configuration files
├── data/                 # Data storage
└── models/               # ML models
```

## 🔧 Usage

### Complete Pipeline
```bash
python main.py  # Runs everything + starts web server
```

### Individual Components
```bash
python main.py --pipeline-only  # ML pipeline only
python main.py --web-only       # Web server only
```

### Web Interface
- Access: `http://localhost:5000`
- ML insights visible after analyzing 70+ companies

## 📊 Features

- **Data Fetching**: Automated API data retrieval
- **ML Analysis**: Financial metrics classification
- **Database Storage**: MySQL integration
- **Web Interface**: Bootstrap-styled dashboard
- **Insights**: Pros/cons analysis with ML

## 📚 Documentation

For detailed documentation, see `PROJECT_DOCUMENTATION.md`

## 🛠️ Troubleshooting

- Check MySQL connection in `config/config.py`
- Verify API key and network connectivity
- Ensure all dependencies installed
- Check console output for error messages

## 🤝 Team Collaboration

- Use feature branches for development
- Update documentation with changes
- Test components individually
- Review code before merging

---

**Version**: 1.0 | **Last Updated**: December 2024 