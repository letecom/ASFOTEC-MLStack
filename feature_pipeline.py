import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

CATEGORICAL_FEATURES = [
    'Contract', 'PaymentMethod', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
    'StreamingMovies', 'gender', 'PaperlessBilling', 'Partner', 'Dependents',
    'PhoneService', 'MultipleLines'
]
NUMERICAL_FEATURES = ['tenure', 'MonthlyCharges', 'TotalCharges']
TARGET = 'Churn'

def preprocess_pipeline():
    """Returns fitted preprocessor."""
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERICAL_FEATURES),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), CATEGORICAL_FEATURES)
        ]
    )
    return preprocessor

def load_and_split_data(data_path='data/telco_churn.csv', test_size=0.2, random_state=42):
    """Load CSV, drop customerID, encode target, split."""
    df = pd.read_csv(data_path)
    df = df.drop('customerID', axis=1)
    df[TARGET] = (df[TARGET] == 'Yes').astype(int)

    if len(df) < 1000:
        repeats = (1000 // len(df)) + 1
        df = pd.concat([df] * repeats, ignore_index=True)
    
    X = df.drop(TARGET, axis=1)
    y = df[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test
