#!/usr/bin/env python3
"""
Financial Analysis ML Pipeline - Main Orchestrator
==================================================

This script orchestrates the ML pipeline using existing data:
1. Train ML classifier (if needed)
2. Analyze existing data with ML
3. Store results in MySQL database
4. Display insights via web interface

Usage:
    python main.py

Requirements:
    - MySQL database running with 'ml' database created
    - Raw JSON data in data/raw/ directory
    - ML training data CSV file
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def check_data_availability():
    """Check if required data files are available"""
    print("Checking data availability...")
    
    # Check raw data
    raw_data_path = Path("data/raw")
    if not raw_data_path.exists():
        print("Error: data/raw directory not found!")
        return False
    
    raw_files = list(raw_data_path.glob("*.json"))
    if not raw_files:
        print("Error: No JSON files found in data/raw/")
        return False
    
    print(f"Found {len(raw_files)} raw data files")
    
    # Check ML training data
    if not Path("ml_training_data.csv").exists():
        print("Warning: ml_training_data.csv not found - ML training may fail")
    
    # Check ML model
    if not Path("ml_pros_classifier.joblib").exists():
        print("Warning: ml_pros_classifier.joblib not found - will train new model")
    
    return True

def run_pipeline():
    """Execute the ML pipeline without data fetching"""
    print("Starting Financial Analysis ML Pipeline")
    print("=" * 50)
    
    # Check data availability
    if not check_data_availability():
        print("Pipeline cannot proceed - missing required data files")
        return False
    
    # Step 1: Train ML Model (if needed)
    print("\nStep 1: Training ML classifier...")
    try:
        from scripts.train_ml_classifier import main as train_main
        train_main()
        print("ML model training completed")
    except Exception as e:
        print(f"Error in ML training: {e}")
        return False
    
    # Step 2: Analyze Data with ML
    print("\nStep 2: Analyzing data with ML...")
    try:
        from scripts.analyze_data import main as analyze_main
        analyze_main()
        print("ML analysis completed")
    except Exception as e:
        print(f"Error in ML analysis: {e}")
        return False
    
    # Step 3: Store Results in MySQL
    print("\nStep 3: Storing results in MySQL...")
    try:
        from scripts.store_results import main as store_main
        store_main()
        print("Results stored in MySQL")
    except Exception as e:
        print(f"Error storing results: {e}")
        return False
    
    print("\nPipeline completed successfully!")
    print("=" * 50)
    print("You can now view insights at: http://localhost:5000")
    print("ML insights will be visible after analyzing 100+ companies")
    
    return True

def start_web_server():
    """Start the Flask web server"""
    print("\nStarting web server...")
    try:
        from web.app import app
        print("Web server started at http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting web server: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Financial Analysis ML Pipeline")
    parser.add_argument("--web-only", action="store_true", 
                       help="Start only the web server without running the pipeline")
    parser.add_argument("--pipeline-only", action="store_true",
                       help="Run only the ML pipeline without starting the web server")
    
    args = parser.parse_args()
    
    if args.web_only:
        start_web_server()
    elif args.pipeline_only:
        run_pipeline()
    else:
        # Run pipeline first, then start web server
        if run_pipeline():
            print("\nStarting web server in 3 seconds...")
            time.sleep(3)
            start_web_server()