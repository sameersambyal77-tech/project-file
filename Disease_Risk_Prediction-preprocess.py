# =============================================================================
# preprocess.py — Data Preprocessing Module
# Machine Learning-Based Disease Risk Prediction System
# =============================================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    A complete data preprocessing pipeline for healthcare datasets.
    Handles missing values, duplicates, outliers, encoding, and scaling.
    """

    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.target_column = 'Outcome'
        self.categorical_columns = ['Gender', 'SmokingStatus', 'FamilyHistory', 'ExerciseLevel']
        self.numerical_columns = [
            'Age', 'BMI', 'BloodPressure', 'Glucose',
            'Insulin', 'HeartRate', 'Cholesterol'
        ]

    # -------------------------------------------------------------------------
    # Step 1 — Load Dataset
    # -------------------------------------------------------------------------
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load dataset from CSV file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at: {filepath}")
        df = pd.read_csv(filepath)
        print(f"[INFO] Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        return df

    # -------------------------------------------------------------------------
    # Step 2 — Handle Missing Values
    # -------------------------------------------------------------------------
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values with median (numerical) or mode (categorical)."""
        before = df.isnull().sum().sum()
        for col in self.numerical_columns:
            if col in df.columns:
                df[col].fillna(df[col].median(), inplace=True)
        for col in self.categorical_columns:
            if col in df.columns:
                df[col].fillna(df[col].mode()[0], inplace=True)
        after = df.isnull().sum().sum()
        print(f"[INFO] Missing values: {before} → {after}")
        return df

    # -------------------------------------------------------------------------
    # Step 3 — Remove Duplicates
    # -------------------------------------------------------------------------
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop duplicate rows."""
        before = len(df)
        df.drop_duplicates(inplace=True)
        after = len(df)
        print(f"[INFO] Duplicates removed: {before - after}")
        return df

    # -------------------------------------------------------------------------
    # Step 4 — Detect and Cap Outliers (IQR method)
    # -------------------------------------------------------------------------
    def handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cap outliers using the IQR method for numerical columns."""
        for col in self.numerical_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                capped = ((df[col] < lower) | (df[col] > upper)).sum()
                df[col] = df[col].clip(lower=lower, upper=upper)
                if capped > 0:
                    print(f"[INFO] Outliers capped in '{col}': {capped} values")
        return df

    # -------------------------------------------------------------------------
    # Step 5 — Encode Categorical Variables
    # -------------------------------------------------------------------------
    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Label-encode categorical columns."""
        for col in self.categorical_columns:
            if col in df.columns:
                if fit:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    le = self.label_encoders.get(col)
                    if le:
                        df[col] = le.transform(df[col].astype(str))
        return df

    # -------------------------------------------------------------------------
    # Step 6 — Feature Scaling
    # -------------------------------------------------------------------------
    def scale_features(self, X: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Standardise feature matrix."""
        if fit:
            return self.scaler.fit_transform(X)
        return self.scaler.transform(X)

    # -------------------------------------------------------------------------
    # Step 7 — Full Pipeline
    # -------------------------------------------------------------------------
    def preprocess(self, df: pd.DataFrame, fit: bool = True):
        """Run the complete preprocessing pipeline and return X_train, X_test, y_train, y_test."""
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.handle_outliers(df)
        df = self.encode_categorical(df, fit=fit)

        self.feature_columns = [c for c in df.columns if c != self.target_column]
        X = df[self.feature_columns]
        y = df[self.target_column]

        X_scaled = self.scale_features(X, fit=fit)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"[INFO] Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train, X_test, y_train, y_test, X, y

    # -------------------------------------------------------------------------
    # Persist / Load Artefacts
    # -------------------------------------------------------------------------
    def save_artifacts(self, models_dir: str):
        """Save scaler and label encoders to disk."""
        os.makedirs(models_dir, exist_ok=True)
        joblib.dump(self.scaler, os.path.join(models_dir, 'scaler.pkl'))
        joblib.dump(self.label_encoders, os.path.join(models_dir, 'label_encoders.pkl'))
        joblib.dump(self.feature_columns, os.path.join(models_dir, 'feature_columns.pkl'))
        print(f"[INFO] Preprocessing artefacts saved to '{models_dir}'")

    def load_artifacts(self, models_dir: str):
        """Load scaler and label encoders from disk."""
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
        self.label_encoders = joblib.load(os.path.join(models_dir, 'label_encoders.pkl'))
        self.feature_columns = joblib.load(os.path.join(models_dir, 'feature_columns.pkl'))
        print(f"[INFO] Preprocessing artefacts loaded from '{models_dir}'")

    # -------------------------------------------------------------------------
    # Single-Row Inference Preprocessing
    # -------------------------------------------------------------------------
    def preprocess_single(self, data: dict) -> np.ndarray:
        """Preprocess a single patient record for inference."""
        df = pd.DataFrame([data])
        # Ensure all expected columns are present
        for col in self.numerical_columns:
            if col not in df.columns:
                df[col] = 0.0
        for col in self.categorical_columns:
            if col not in df.columns:
                df[col] = 'Unknown'
        df = self.encode_categorical(df, fit=False)
        # Keep only trained feature columns
        df = df[self.feature_columns]
        return self.scale_features(df, fit=False)
