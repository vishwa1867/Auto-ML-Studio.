# services/data_io.py
import os, uuid, pandas as pd
from typing import Tuple

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_uploaded_csv(spooled_file, original_name: str) -> str:
    uid = uuid.uuid4().hex
    path = os.path.join(DATA_DIR, f"{uid}_{original_name}")
    with open(path, "wb") as f:
        f.write(spooled_file.read())
    return path

def load_tabular_csv(path: str, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found. Available: {list(df.columns)}")
    X = df.drop(columns=[target_col])
    y = df[target_col]
    # Basic encoding for categorical X; y kept as-is for classification/regression auto-handled in trainer
    X = pd.get_dummies(X, drop_first=False)
    return X, y
