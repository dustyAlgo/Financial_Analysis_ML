import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def main():
    """Train ML classifier for financial analysis"""
    print("Training ML classifier...")
    
    # Load data
    csv_path = "ml_training_data.csv"
    df = pd.read_csv(csv_path)
    print(f"Loaded training data: {len(df)} records")

    # Features and labels
    feature_cols = ["roe", "dividend_payout", "sales_growth", "debt_ratio"]
    label_cols = ["pro_roe", "pro_dividend", "pro_sales", "pro_debt"]

    X = df[feature_cols]
    y = df[label_cols]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model with regularization to prevent overfitting
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,              # Limit tree depth - prevents overfitting
        min_samples_split=8,       # Minimum samples required to split a node
        min_samples_leaf=3,        # Minimum samples required in a leaf node
        max_features=0.8,          # Use 80% of features per split - increases diversity
        max_samples=0.8,           # Use 80% of samples per tree - increases robustness
        bootstrap=True,            # Bootstrap sampling
        random_state=42,           # Reproducibility
        n_jobs=-1                  # Use all available CPU cores
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("Classification report (per label):")
    print(classification_report(y_test, y_pred, target_names=label_cols))

    # Save model
    joblib.dump(clf, "ml_pros_classifier.joblib")
    print("Model trained and saved as ml_pros_classifier.joblib")

if __name__ == "__main__":
    main() 