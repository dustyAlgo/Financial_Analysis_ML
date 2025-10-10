#!/usr/bin/env python3
"""
Financial Analysis ML Pipeline - Main Orchestrator
==================================================

This script orchestrates the complete ML pipeline:
1. Fetch financial data for Nifty 100 companies
2. Apply machine learning analysis
3. Store results in MySQL database
4. Display insights via web interface

Usage:
    python main.py

Requirements:
    - MySQL database running with 'ml' database created
    - Required Python packages installed (see requirements.txt)
    - API access configured in config/config.py
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def run_pipeline():
    """Execute the complete ML pipeline"""
    print("🚀 Starting Financial Analysis ML Pipeline")
    print("=" * 50)
    
    # Step 1: Fetch Data
    print("\n📡 Step 1: Fetching financial data...")
    try:
        from scripts.fetch_data import main as fetch_main
        fetch_main()
        print("✅ Data fetching completed")
    except Exception as e:
        print(f"❌ Error in data fetching: {e}")
        return False
    
    # Step 2: Train ML Model (if needed)
    print("\n🤖 Step 2: Training ML classifier...")
    try:
        from scripts.train_ml_classifier import main as train_main
        train_main()
        print("✅ ML model training completed")
    except Exception as e:
        print(f"❌ Error in ML training: {e}")
        return False
    
    # Step 3: Analyze Data with ML
    print("\n🔍 Step 3: Analyzing data with ML...")
    try:
        from scripts.analyze_data import main as analyze_main
        analyze_main()
        print("✅ ML analysis completed")
    except Exception as e:
        print(f"❌ Error in ML analysis: {e}")
        return False
    
    # Step 4: Store Results in MySQL
    print("\n💾 Step 4: Storing results in MySQL...")
    try:
        from scripts.store_results import main as store_main
        store_main()
        print("✅ Results stored in MySQL")
    except Exception as e:
        print(f"❌ Error storing results: {e}")
        return False
    
    print("\n🎉 Pipeline completed successfully!")
    print("=" * 50)
    print("📊 You can now view insights at: http://localhost:5000")
    print("💡 ML insights will be visible after analyzing 100+ companies")
    
    return True

def start_web_server():
    """Start the Flask web server"""
    print("\n🌐 Starting web server...")
    try:
        from web.app import app
        print("✅ Web server started at http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting web server: {e}")

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
            print("\n⏳ Starting web server in 3 seconds...")
            time.sleep(3)
            start_web_server()
