-- Financial Analysis ML Database Schema
-- Run this file to set up the MySQL database

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS ml;
USE ml;

-- Companies table - stores basic company information
CREATE TABLE IF NOT EXISTS companies (
    id VARCHAR(50) PRIMARY KEY,
    company_logo TEXT,
    company_name VARCHAR(255) NOT NULL,
    chart_link TEXT,
    about_company TEXT,
    website VARCHAR(255),
    nse_profile VARCHAR(255),
    bse_profile VARCHAR(255),
    face_value DECIMAL(10,2),
    book_value DECIMAL(10,2),
    roce_percentage DECIMAL(5,2),
    roe_percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Analysis table - stores ML-generated analysis results
CREATE TABLE IF NOT EXISTS analysis (
    id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    compounded_sales_growth VARCHAR(20),
    compounded_profit_growth VARCHAR(20),
    stock_price_cagr VARCHAR(20),
    roe VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Pros and Cons table - stores ML-generated insights
CREATE TABLE IF NOT EXISTS prosandcons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    pros TEXT,
    cons TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_companies_name ON companies(company_name);
CREATE INDEX idx_analysis_company ON analysis(company_id);
CREATE INDEX idx_proscons_company ON prosandcons(company_id);

-- Cashflow statements for each company/year
CREATE TABLE IF NOT EXISTS cashflow (
    id INT PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    year VARCHAR(20) NOT NULL,
    operating_activity DECIMAL(20,2),
    investing_activity DECIMAL(20,2),
    financing_activity DECIMAL(20,2),
    net_cash_flow DECIMAL(20,2),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_cashflow_company (company_id),
    INDEX idx_cashflow_year (year)
);

-- Balance sheets for each company/year
CREATE TABLE IF NOT EXISTS balancesheet (
    id INT PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    year VARCHAR(20) NOT NULL,
    equity_capital DECIMAL(20,2),
    reserves DECIMAL(20,2),
    borrowings DECIMAL(20,2),
    other_liabilities DECIMAL(20,2),
    total_liabilities DECIMAL(20,2),
    fixed_assets DECIMAL(20,2),
    cwip DECIMAL(20,2),
    investments DECIMAL(20,2),
    other_asset DECIMAL(20,2),
    total_assets DECIMAL(20,2),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_balancesheet_company (company_id),
    INDEX idx_balancesheet_year (year)
);

-- Profit and loss for each company/year
CREATE TABLE IF NOT EXISTS profitandloss (
    id INT PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    year VARCHAR(20) NOT NULL,
    sales DECIMAL(20,2),
    expenses DECIMAL(20,2),
    operating_profit DECIMAL(20,2),
    opm_percentage DECIMAL(10,4),
    other_income DECIMAL(20,2),
    interest DECIMAL(20,2),
    depreciation DECIMAL(20,2),
    profit_before_tax DECIMAL(20,2),
    tax_percentage VARCHAR(10),
    net_profit DECIMAL(20,2),
    eps DECIMAL(20,2),
    dividend_payout VARCHAR(20),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_profitandloss_company (company_id),
    INDEX idx_profitandloss_year (year)
);

-- Insert sample data (optional)
-- INSERT INTO companies (id, company_name) VALUES ('SAMPLE', 'Sample Company');

-- Show table structure
DESCRIBE companies;
DESCRIBE analysis;
DESCRIBE prosandcons;

-- Show indexes
SHOW INDEX FROM companies;
SHOW INDEX FROM analysis;
SHOW INDEX FROM prosandcons; 