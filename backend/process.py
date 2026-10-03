# File: preprocess.py

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import os

def identify_columns(df):
    """Identify numerical and categorical columns in a DataFrame"""
    numerical_cols = df.select_dtypes(include=['int64', 'float64', 'bool']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return numerical_cols, categorical_cols

def impute_missing(df, numerical_cols, categorical_cols):
    """Handle missing values safely"""
    if numerical_cols:
        try:
            num_imputer = SimpleImputer(strategy="mean")
            df[numerical_cols] = num_imputer.fit_transform(df[numerical_cols])
        except Exception as e:
            print(f"⚠️ Numerical imputation failed: {e}")

    if categorical_cols:
        try:
            cat_imputer = SimpleImputer(strategy="most_frequent")
            df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
        except Exception as e:
            print(f"⚠️ Categorical imputation failed: {e}")

    return df

def preprocess_chunk(df, numerical_cols, categorical_cols, encoder=None, scaler=None):
    """Scale numerical and encode categorical columns per chunk"""
    # Scale numerical columns
    if numerical_cols:
        try:
            if scaler is None:
                scaler = StandardScaler()
                df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
            else:
                df[numerical_cols] = scaler.transform(df[numerical_cols])
        except Exception as e:
            print(f"⚠️ Scaling failed: {e}")

    # Encode categorical columns
    if categorical_cols:
        try:
            if encoder is None:
                try:
                    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
                except TypeError:
                    encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
                encoded_array = encoder.fit_transform(df[categorical_cols])
            else:
                encoded_array = encoder.transform(df[categorical_cols])

            encoded_df = pd.DataFrame(
                encoded_array,
                columns=encoder.get_feature_names_out(categorical_cols),
                index=df.index
            )
            df = df.drop(columns=categorical_cols)
            df = pd.concat([df, encoded_df], axis=1)
        except Exception as e:
            print(f"⚠️ Encoding failed: {e}")

    return df, encoder, scaler

def process_file(file_path, output_folder="static/cleaned_files", chunk_size=50000):
    """
    Process CSV file in chunks (for big data), clean, and save.
    Returns path to cleaned CSV or None if failed.
    """
    os.makedirs(output_folder, exist_ok=True)
    cleaned_file_name = f"cleaned_{os.path.basename(file_path)}"
    cleaned_file_path = os.path.join(output_folder, cleaned_file_name)

    first_chunk = True
    encoder, scaler = None, None

    try:
        for chunk in pd.read_csv(file_path, encoding="utf-8", chunksize=chunk_size, on_bad_lines="skip"):
            if chunk.empty:
                continue

            numerical_cols, categorical_cols = identify_columns(chunk)
            chunk = impute_missing(chunk, numerical_cols, categorical_cols)
            chunk, encoder, scaler = preprocess_chunk(chunk, numerical_cols, categorical_cols, encoder, scaler)

            if first_chunk:
                chunk.to_csv(cleaned_file_path, index=False, mode='w')
                first_chunk = False
            else:
                chunk.to_csv(cleaned_file_path, index=False, mode='a', header=False)

        print(f"✅ File processed and saved at: {cleaned_file_path}")
        return cleaned_file_path

    except Exception as e:
        print(f"❌ Failed to process file {file_path}: {e}")
        return None
