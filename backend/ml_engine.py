import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score

def train_model(file_path, model_choice):
    df = pd.read_csv(file_path)
    df = df.dropna(axis=1, how='all')

    if df.shape[1] < 2:
        raise ValueError("Dataset must have at least one feature and one target column.")

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Convert categorical features to numeric
    X = pd.get_dummies(X)

    # Encode target if categorical
    if y.dtype == 'object':
        y = pd.factorize(y)[0]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Select model
    if model_choice == "Random Forest":
        model = RandomForestClassifier()
    elif model_choice == "Decision Tree":
        model = DecisionTreeClassifier()
    elif model_choice == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)
    elif model_choice == "SVM":
        model = SVC()
    elif model_choice == "XGBoost":
        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    else:
        raise ValueError("Invalid model choice")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "Model": model_choice,
        "Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "F1 Score": round(f1_score(y_test, y_pred, average='weighted'), 4)
    }
    return metrics
