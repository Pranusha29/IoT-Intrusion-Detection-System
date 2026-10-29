import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def load_and_preprocess(csv_path):
    """
    Load CICIoT2023 CSV and perform basic preprocessing.
    """

    # Load dataset
    df = pd.read_csv(csv_path)

    # Separate features and target
    X = df.drop(columns=["Label"])
    y = df["Label"]

    # Handle infinite values
    X = X.replace([np.inf, -np.inf], np.nan)

    # Handle missing values using feature-wise median
    X = X.fillna(X.median())

    # Encode attack labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder


def ordered_train_test_split(X, y, train_ratio=0.8):
    """
    Split data while preserving the original row order.
    """

    split_point = int(len(X) * train_ratio)

    X_train = X.iloc[:split_point]
    X_test = X.iloc[split_point:]

    y_train = y[:split_point]
    y_test = y[split_point:]

    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    """
    Fit scaler only on training data and transform both sets.
    """

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler