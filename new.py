import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import json
import os

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

def auto_detect_target(df):
    possible_targets = ['target', 'label', 'class', 'output', 'y']
    for col in df.columns:
        if col.lower() in possible_targets:
            return col
    # If none found, assume last column
    return df.columns[-1]

def preprocess_data(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Encode target if categorical
    if y.dtype == 'object':
        le = LabelEncoder()
        y = le.fit_transform(y)

    # Encode categorical features
    X = pd.get_dummies(X)

    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

def get_model(model_choice):
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "XGBoost": XGBClassifier(eval_metric='mlogloss', random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    return models.get(model_choice, RandomForestClassifier())

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    if len(np.unique(y_test)) > 2:
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        metrics = {"Accuracy": acc, "F1 Score": f1}
    else:
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        metrics = {"Accuracy": acc, "F1 Score": f1}
    return metrics

def run_training(file_path, model_choice):
    print(f"🚀 Loading dataset from: {file_path}")
    df = load_dataset(file_path)
    target_col = auto_detect_target(df)
    print(f"🎯 Target column detected: {target_col}")

    X, y = preprocess_data(df, target_col)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = get_model(model_choice)
    print(f"🧠 Training model: {model_choice}...")
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)
    print(f"✅ Model evaluation: {metrics}")

    # Save model and metrics
    os.makedirs("models", exist_ok=True)
    model_path = f"models/{model_choice.replace(' ', '_')}.pkl"
    joblib.dump(model, model_path)

    with open(f"models/{model_choice}_metrics.json", "w") as f:
        json.dump(metrics, f)

    print(f"📦 Model saved at {model_path}")
    print(f"📊 Metrics: {metrics}")

    return metrics

# Example usage (this part can be triggered by UI or CLI)
if __name__ == "__main__":
    dataset_path = "data/cleaned_data.csv"  # dynamic from UI
    user_choice = "Random Forest"  # dynamic input from dropdown or API
    run_training(dataset_path, user_choice)
