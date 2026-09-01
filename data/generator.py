import os
import numpy as np
import pandas as pd

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def generate_synthetic_data(num_samples=15000, seed=42):
    """
    Generates synthetic transaction benchmark datasets tailored to Indian Payment Systems (UPI, Netbanking, Cards):
    1. Tabular features (amount in INR Rs., Indian merchant categories, PCA V-features).
    2. Per-account sequence logs (rolling velocity, IP changes).
    """
    np.random.seed(seed)
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    print(f"Generating synthetic Indian transaction dataset (in Rs. INR) with {num_samples} records...")
    
    # Generate Account IDs and Timestamps
    account_ids = [f"ACC_IND_{np.random.randint(1000, 9999)}" for _ in range(num_samples)]
    timestamps = pd.date_range(start='2026-01-01', periods=num_samples, freq='2min')
    
    # Normal feature distributions in INR (Rs.)
    amounts = np.round(np.random.exponential(scale=1800.0, size=num_samples) + 49.0, 2)
    merchant_cats = np.random.choice([
        'upi_kirana_retail', 'food_zomato_swiggy', 'ecommerce_amazon_flipkart',
        'digital_gaming_rummy', 'travel_irctc_airlines', 'crypto_offshore'
    ], size=num_samples, p=[0.40, 0.20, 0.20, 0.10, 0.07, 0.03])
    
    device_risk = np.random.beta(a=1.5, b=8.0, size=num_samples)
    location_dist = np.random.exponential(scale=15.0, size=num_samples)
    account_age = np.random.randint(1, 1500, size=num_samples)
    card_age = np.random.randint(1, 1000, size=num_samples)
    hour_of_day = timestamps.hour.values
    is_weekend = (timestamps.dayofweek >= 5).astype(int)
    
    V_features = {f"V{i}": np.random.normal(0, 1.0, size=num_samples) for i in range(1, 11)}
    
    fraud_labels = np.zeros(num_samples, dtype=int)
    fraud_types = ["LEGITIMATE"] * num_samples
    
    num_fraud = int(num_samples * 0.012)
    fraud_indices = np.random.choice(num_samples, size=num_fraud, replace=False)
    
    fraud_categories = ["CNP_FRAUD", "ACCOUNT_TAKEOVER", "SYNTHETIC_IDENTITY", "VELOCITY_ABUSE", "CHARGEBACK_FRAUD"]
    
    for idx in fraud_indices:
        f_type = np.random.choice(fraud_categories)
        fraud_labels[idx] = 1
        fraud_types[idx] = f_type
        
        if f_type == "CNP_FRAUD":
            amounts[idx] = np.random.uniform(45000.0, 250000.0)
            merchant_cats[idx] = np.random.choice(['crypto_offshore', 'ecommerce_amazon_flipkart', 'digital_gaming_rummy'])
            device_risk[idx] = np.random.uniform(0.7, 0.99)
            V_features["V1"][idx] = np.random.uniform(-4.5, -2.5)
            V_features["V2"][idx] = np.random.uniform(3.0, 6.0)
            
        elif f_type == "ACCOUNT_TAKEOVER":
            amounts[idx] = np.random.uniform(50000.0, 500000.0)
            location_dist[idx] += np.random.uniform(500, 3000)
            device_risk[idx] = np.random.uniform(0.8, 1.0)
            V_features["V3"][idx] = np.random.uniform(-6.0, -3.0)
            V_features["V4"][idx] = np.random.uniform(4.0, 7.0)
            
        elif f_type == "SYNTHETIC_IDENTITY":
            amounts[idx] = np.random.uniform(20000.0, 150000.0)
            account_age[idx] = np.random.randint(1, 7)
            card_age[idx] = np.random.randint(1, 3)
            device_risk[idx] = np.random.uniform(0.6, 0.95)
            V_features["V5"][idx] = np.random.uniform(-3.5, -1.5)
            
        elif f_type == "VELOCITY_ABUSE":
            amounts[idx] = np.random.uniform(2000.0, 15000.0)
            device_risk[idx] = np.random.uniform(0.75, 0.98)
            V_features["V6"][idx] = np.random.uniform(2.5, 5.5)
            
        elif f_type == "CHARGEBACK_FRAUD":
            merchant_cats[idx] = 'digital_gaming_rummy'
            amounts[idx] = np.random.uniform(10000.0, 80000.0)
            V_features["V7"][idx] = np.random.uniform(-2.5, -1.0)

    data_dict = {
        'transaction_id': [f"TXN_INR_{100000+i}" for i in range(num_samples)],
        'account_id': account_ids,
        'timestamp': timestamps,
        'amount': amounts,
        'merchant_category': merchant_cats,
        'device_risk_score': device_risk,
        'location_distance_km': location_dist,
        'account_age_days': account_age,
        'card_age_days': card_age,
        'hour_of_day': hour_of_day,
        'is_weekend': is_weekend,
        **V_features,
        'is_fraud': fraud_labels,
        'fraud_type': fraud_types
    }
    
    df_tabular = pd.DataFrame(data_dict)
    df_tabular.to_csv(config.TABULAR_DATASET_PATH, index=False)
    print(f"Saved Tabular Dataset to {config.TABULAR_DATASET_PATH} ({len(df_tabular)} rows, {df_tabular['is_fraud'].sum()} frauds)")

    df_tabular.sort_values(by=['account_id', 'timestamp'], inplace=True)
    df_tabular.reset_index(drop=True, inplace=True)
    
    df_tabular['time_delta_sec'] = df_tabular.groupby('account_id')['timestamp'].diff().dt.total_seconds().fillna(3600)
    
    df_temp = df_tabular.set_index('timestamp')
    df_tabular['velocity_5m'] = df_temp.groupby('account_id')['amount'].rolling('5min').count().values - 1
    df_tabular['amount_sum_1h'] = df_temp.groupby('account_id')['amount'].rolling('1h').sum().values
    df_tabular['ip_change_flag'] = (df_tabular['location_distance_km'] > 100).astype(int)
    
    df_tabular.to_csv(config.SEQUENCE_DATASET_PATH, index=False)
    print(f"Saved Sequence Dataset to {config.SEQUENCE_DATASET_PATH}")
    
    return df_tabular

if __name__ == "__main__":
    generate_synthetic_data()
