import time
import random
import requests

API_URL = "http://127.0.0.1:5000/api/evaluate"

print("=========================================================")
print(" LIVE INDIAN TRANSACTION STREAM SIMULATOR (UPI / CARDS INR)")
print(" Streaming live incoming Indian payment requests (in Rs. INR)...")
print(" Press CTRL+C to stop.")
print("=========================================================\n")

categories = [
    'upi_kirana_retail', 'food_zomato_swiggy', 'ecommerce_amazon_flipkart',
    'digital_gaming_rummy', 'travel_irctc_airlines', 'crypto_offshore'
]

try:
    while True:
        is_suspicious = random.random() < 0.35
        
        # Amounts in Indian Rupees (Rs.)
        amount_inr = round(
            random.uniform(45000.0, 350000.0) if is_suspicious else random.uniform(50.0, 2500.0), 2
        )
        
        payload = {
            "account_id": f"ACC_IND_{random.randint(1000, 9999)}",
            "amount": amount_inr,
            "merchant_category": random.choice(['crypto_offshore', 'digital_gaming_rummy']) if is_suspicious else random.choice(categories),
            "device_risk_score": round(random.uniform(0.7, 0.99) if is_suspicious else random.uniform(0.05, 0.3), 2),
            "location_distance_km": round(random.uniform(300, 2500) if is_suspicious else random.uniform(1, 20), 1),
            "account_age_days": random.randint(1, 5) if is_suspicious else random.randint(60, 1000),
            "card_age_days": random.randint(1, 3) if is_suspicious else random.randint(30, 500),
            "hour_of_day": random.choice([2, 3, 4]) if is_suspicious else random.choice([10, 12, 14, 16, 18]),
            "is_weekend": random.choice([0, 1]),
            "velocity_5m": random.randint(4, 10) if is_suspicious else 1
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=3.0)
            if response.status_code == 200:
                res = response.json()
                score = res['risk_score']
                decision = res['decision']
                cat = res['framework_mapping']['category_name']
                
                tag = "[APPROVE]" if decision == "APPROVE" else ("  [STEP-UP 2FA]" if decision == "STEP_UP_AUTHENTICATION" else "    [BLOCK]")
                print(f"{tag} Txn: {res['transaction_id']} | Acc: {res['account_id']} | Amt: Rs.{amount_inr:,.2f} | Risk Score: {score}/100 | Category: {cat}")
            else:
                print(f"Server returned status code: {response.status_code}")
        except Exception as e:
            print(f"Request error: {e}")
            
        time.sleep(2.5)

except KeyboardInterrupt:
    print("\nLive transaction stream stopped.")
