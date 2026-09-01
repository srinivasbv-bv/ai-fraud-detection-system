import os
import json
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import joblib

import config
from models.ensemble_engine import EnsembleRiskScoringEngine
from logging_elk.elk_logger import ELKLogger

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Core Services
risk_engine = EnsembleRiskScoringEngine()
elk_logger = ELKLogger()

# In-Memory Transaction Store for Web UI Session
evaluated_transactions = []

def initialize_system():
    """
    Ensures dataset exists, pre-trains models if needed, and populates initial sample queue.
    """
    if not os.path.exists(config.SUPERVISED_MODEL_PATH) or not os.path.exists(config.METRICS_PATH):
        print("Pre-training ML models on Indian transaction benchmark dataset...")
        risk_engine.supervised_clf.train_and_evaluate()
        
    # Populate initial transaction list if empty
    if os.path.exists(config.TABULAR_DATASET_PATH) and len(evaluated_transactions) == 0:
        df = pd.read_csv(config.TABULAR_DATASET_PATH).head(30)
        for _, row in df.iterrows():
            txn_dict = row.to_dict()
            tabular_feats = np.zeros((1, 23))
            seq_feats = np.zeros((1, config.SEQUENCE_LENGTH, 7))
            
            res = risk_engine.evaluate_transaction(tabular_feats, seq_feats, txn_dict)
            res["status"] = "Pending Review" if res["decision"] != "APPROVE" else "Auto-Approved"
            evaluated_transactions.append(res)
            elk_logger.log_evaluation_event(res, txn_dict)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')

@app.route('/queue')
def queue():
    return render_template('analyst_queue.html')

@app.route('/metrics')
def metrics():
    return render_template('model_metrics.html')

@app.route('/framework')
def framework():
    return render_template('framework_mapping.html')

@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    data = request.json or {}
    
    # Extract transaction input fields in INR (₹)
    amount = float(data.get('amount', 450.00))
    merchant_cat = data.get('merchant_category', 'upi_kirana_retail')
    device_risk = float(data.get('device_risk_score', 0.15))
    location_dist = float(data.get('location_distance_km', 8.5))
    account_age = int(data.get('account_age_days', 365))
    card_age = int(data.get('card_age_days', 180))
    hour = int(data.get('hour_of_day', 14))
    is_weekend = int(data.get('is_weekend', 0))
    velocity_5m = int(data.get('velocity_5m', 1))
    
    num_feats = [amount, device_risk, location_dist, account_age, card_age, hour, is_weekend] + [0.0]*10
    
    scaler_dict = joblib.load(config.SCALER_PATH) if os.path.exists(config.SCALER_PATH) else None
    if scaler_dict:
        scaler = scaler_dict["scaler"]
        encoder = scaler_dict["encoder"]
        X_num = scaler.transform(np.array(num_feats).reshape(1, -1))
        
        # Handle one-hot encoding safely
        try:
            X_cat = encoder.transform([[merchant_cat]])
        except Exception:
            X_cat = np.zeros((1, 6))
            
        tabular_feats = np.hstack([X_num, X_cat])
    else:
        tabular_feats = np.random.normal(0, 1, size=(1, 23))
        
    seq_feats = np.random.normal(0, 1, size=(1, config.SEQUENCE_LENGTH, 7))
    if velocity_5m > 3:
        seq_feats[0, :, 4] = velocity_5m
        
    raw_txn = {
        "transaction_id": f"TXN_INR_{np.random.randint(100000, 999999)}",
        "account_id": data.get('account_id', f"ACC_IND_{np.random.randint(1000, 9999)}"),
        "amount": amount,
        "merchant_category": merchant_cat,
        "device_risk_score": device_risk,
        "location_distance_km": location_dist,
        "account_age_days": account_age,
        "card_age_days": card_age,
        "hour_of_day": hour,
        "is_weekend": is_weekend,
        "velocity_5m": velocity_5m,
        "ip_address": data.get('ip_address', '106.208.14.92'), # Indian IP
        "card_number": data.get('card_number', '459111******1234')
    }
    
    eval_result = risk_engine.evaluate_transaction(tabular_feats, seq_feats, raw_txn)
    eval_result["status"] = "Pending Review" if eval_result["decision"] != "APPROVE" else "Auto-Approved"
    eval_result["timestamp"] = pd.Timestamp.now().isoformat()
    
    evaluated_transactions.insert(0, eval_result)
    elk_logger.log_evaluation_event(eval_result, raw_txn)
    
    return jsonify(eval_result)

@app.route('/api/stats', methods=['GET'])
def api_stats():
    total = len(evaluated_transactions)
    approved = sum(1 for t in evaluated_transactions if t['decision'] == 'APPROVE')
    stepup = sum(1 for t in evaluated_transactions if t['decision'] == 'STEP_UP_AUTHENTICATION')
    blocked = sum(1 for t in evaluated_transactions if t['decision'] == 'BLOCK')
    
    category_counts = {}
    for t in evaluated_transactions:
        cat = t.get('fraud_category', 'LEGITIMATE')
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    return jsonify({
        "total_transactions": total,
        "decisions": {
            "approved": approved,
            "step_up": stepup,
            "blocked": blocked
        },
        "fraud_categories": category_counts,
        "average_risk_score": round(float(np.mean([t['risk_score'] for t in evaluated_transactions])) if total > 0 else 0.0, 2)
    })

@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    if os.path.exists(config.METRICS_PATH):
        with open(config.METRICS_PATH, 'r') as f:
            metrics_data = json.load(f)
        return jsonify(metrics_data)
    else:
        return jsonify({"error": "Metrics file not found. Please train models first."}), 404

@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    decision_filter = request.args.get('decision')
    limit = int(request.args.get('limit', 50))
    
    txns = evaluated_transactions
    if decision_filter:
        txns = [t for t in txns if t['decision'] == decision_filter]
        
    return jsonify(txns[:limit])

@app.route('/api/action', methods=['POST'])
def api_action():
    data = request.json or {}
    txn_id = data.get('transaction_id')
    action = data.get('action')
    
    for t in evaluated_transactions:
        if t['transaction_id'] == txn_id:
            if action == 'CONFIRM_FRAUD':
                t['status'] = 'Confirmed Fraud'
            elif action == 'MARK_LEGITIMATE':
                t['status'] = 'Marked Legitimate'
            elif action == 'DISMISS':
                t['status'] = 'Dismissed'
            return jsonify({"status": "success", "updated_transaction": t})
            
    return jsonify({"error": "Transaction not found"}), 404

if __name__ == '__main__':
    initialize_system()
    app.run(host='0.0.0.0', port=5000, debug=True)
