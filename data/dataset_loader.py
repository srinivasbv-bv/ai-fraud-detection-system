import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib

try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False
    print("Notice: imbalanced-learn not installed. Using random minority oversampling fallback for class imbalance correction.")

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from data.generator import generate_synthetic_data

FEATURE_COLS_NUMERICAL = [
    'amount', 'device_risk_score', 'location_distance_km', 'account_age_days',
    'card_age_days', 'hour_of_day', 'is_weekend',
    'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10'
]

FEATURE_COLS_CATEGORICAL = ['merchant_category']

SEQUENCE_FEATURE_COLS = [
    'amount', 'device_risk_score', 'location_distance_km',
    'time_delta_sec', 'velocity_5m', 'amount_sum_1h', 'ip_change_flag'
]

def load_and_preprocess_tabular(apply_smote=True):
    """
    Loads tabular dataset, performs scaling/encoding, and applies SMOTE resampling for supervised ML models.
    """
    if not os.path.exists(config.TABULAR_DATASET_PATH):
        generate_synthetic_data()
        
    df = pd.read_csv(config.TABULAR_DATASET_PATH)
    
    X_num = df[FEATURE_COLS_NUMERICAL].values
    y = df['is_fraud'].values
    
    # One-hot encode merchant_category
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_cat = encoder.fit_transform(df[FEATURE_COLS_CATEGORICAL])
    
    # Train-test split
    X_num_train, X_num_test, X_cat_train, X_cat_test, y_train, y_test = train_test_split(
        X_num, X_cat, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scaling ONLY numerical features (17 features)
    scaler = StandardScaler()
    X_num_train_scaled = scaler.fit_transform(X_num_train)
    X_num_test_scaled = scaler.transform(X_num_test)
    
    X_train_scaled = np.hstack([X_num_train_scaled, X_cat_train])
    X_test_scaled = np.hstack([X_num_test_scaled, X_cat_test])
    
    # Save Scaler and Encoder
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    joblib.dump({"scaler": scaler, "encoder": encoder, "num_cols": FEATURE_COLS_NUMERICAL}, config.SCALER_PATH)
    
    if apply_smote:
        if SMOTE_AVAILABLE:
            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
            print(f"SMOTE applied: Training set expanded from {len(y_train)} to {len(y_train_res)} (Frauds: {sum(y_train_res)})")
        else:
            # Fallback random oversampling
            fraud_idx = np.where(y_train == 1)[0]
            legit_idx = np.where(y_train == 0)[0]
            over_fraud_idx = np.random.choice(fraud_idx, size=len(legit_idx), replace=True)
            res_idx = np.concatenate([legit_idx, over_fraud_idx])
            np.random.shuffle(res_idx)
            X_train_res = X_train_scaled[res_idx]
            y_train_res = y_train[res_idx]
            print(f"Oversampling applied: Training set expanded to {len(y_train_res)} (Frauds: {sum(y_train_res)})")
            
        return X_train_res, X_test_scaled, y_train_res, y_test, df
        
    return X_train_scaled, X_test_scaled, y_train, y_test, df

def prepare_sequence_data(seq_length=config.SEQUENCE_LENGTH):
    if not os.path.exists(config.SEQUENCE_DATASET_PATH):
        generate_synthetic_data()
        
    df = pd.read_csv(config.SEQUENCE_DATASET_PATH)
    
    scaler = StandardScaler()
    scaled_feats = scaler.fit_transform(df[SEQUENCE_FEATURE_COLS].values)
    
    sequences = []
    labels = []
    
    for account_id, group in df.groupby('account_id'):
        group_feats = scaled_feats[group.index]
        group_labels = group['is_fraud'].values
        
        if len(group_feats) >= seq_length:
            for i in range(len(group_feats) - seq_length + 1):
                seq = group_feats[i:i+seq_length]
                label = group_labels[i+seq_length-1]
                sequences.append(seq)
                labels.append(label)
        else:
            pad_len = seq_length - len(group_feats)
            padded = np.pad(group_feats, ((pad_len, 0), (0, 0)), mode='edge')
            sequences.append(padded)
            labels.append(group_labels[-1])
            
    X_seq = np.array(sequences)
    y_seq = np.array(labels)
    
    X_train_seq, X_test_seq, y_train_seq, y_test_seq = train_test_split(
        X_seq, y_seq, test_size=0.2, random_state=42, stratify=y_seq
    )
    
    return X_train_seq, X_test_seq, y_train_seq, y_test_seq, scaler
