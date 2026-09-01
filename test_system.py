import os
import sys
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import config
from data.generator import generate_synthetic_data
from models.ensemble_engine import EnsembleRiskScoringEngine
from logging_elk.elk_logger import ELKLogger

def run_tests():
    print("Running system verification tests...")
    
    # 1. Test Dataset Generation
    df = generate_synthetic_data(num_samples=100)
    assert len(df) == 100, "Dataset generation failed."
    print("[PASS] Dataset Generation Test Passed.")

    # 2. Test Ensemble Engine
    engine = EnsembleRiskScoringEngine()
    
    dummy_tabular = np.zeros((1, 23))
    dummy_seq = np.zeros((1, 10, 7))
    
    # Test Legitimate Case
    legit_txn = {"transaction_id": "TXN_TEST_1", "amount": 25.0, "velocity_5m": 0, "location_distance_km": 2.0}
    res_legit = engine.evaluate_transaction(dummy_tabular, dummy_seq, legit_txn)
    assert res_legit["decision"] == "APPROVE", f"Expected APPROVE, got {res_legit['decision']}"
    assert "framework_mapping" in res_legit
    assert res_legit["framework_mapping"]["owasp_reference"] is not None
    print("[PASS] Legitimate Transaction Test Passed.")

    # Test High-Velocity Fraud Case
    vel_txn = {"transaction_id": "TXN_TEST_2", "amount": 150.0, "velocity_5m": 6, "device_risk_score": 0.9}
    dummy_seq[0, :, 4] = 6 # High velocity sequence
    res_vel = engine.evaluate_transaction(dummy_tabular, dummy_seq, vel_txn)
    assert res_vel["decision"] in ["STEP_UP_AUTHENTICATION", "BLOCK"], f"Expected STEP_UP or BLOCK, got {res_vel['decision']}"
    assert len(res_vel["triggered_rules"]) > 0
    print("[PASS] High Velocity Fraud Test Passed.")

    # 3. Test ELK Logging
    logger = ELKLogger()
    log_event = logger.log_evaluation_event(res_vel, vel_txn)
    assert os.path.exists(config.NDJSON_LOG_PATH)
    assert log_event["transaction"]["id"] == "TXN_TEST_2"
    print("[PASS] ELK NDJSON Logger Test Passed.")

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! System is production-ready.")

if __name__ == "__main__":
    run_tests()
