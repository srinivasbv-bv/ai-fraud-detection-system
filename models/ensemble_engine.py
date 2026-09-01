import os
import numpy as np

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from models.supervised_model import SupervisedFraudClassifier
from models.sequence_model import DeepSequenceFraudDetector
from framework.mapping_engine import FrameworkMappingEngine

class BusinessRuleEngine:
    """
    Lightweight heuristic rule overlay for rapid velocity, blacklists, and geo-mismatches.
    """
    def __init__(self):
        self.blacklisted_ips = {'192.168.1.105', '10.0.0.99', '185.220.101.5'}
        self.blacklisted_cards = {'411111******1111', '550000******0000'}

    def evaluate_rules(self, txn_data):
        rule_score = 0.0
        triggered_rules = []

        # 1. Hard Velocity Cap Rule (> 5 txns in 5 mins)
        if txn_data.get('velocity_5m', 0) > 4:
            rule_score += 0.85
            triggered_rules.append("HIGH_VELOCITY_BURST (>5 txns in 5 min)")

        # 2. Extreme Geographic Mismatch (> 1000 km)
        if txn_data.get('location_distance_km', 0) > 1000:
            rule_score += 0.75
            triggered_rules.append("EXTREME_GEO_DISTANCE_JUMP (>1000 km)")

        # 3. High Device Risk & Nighttime Transaction
        if txn_data.get('device_risk_score', 0) > 0.80 and (txn_data.get('hour_of_day', 12) < 5 or txn_data.get('hour_of_day', 12) > 23):
            rule_score += 0.65
            triggered_rules.append("SUSPICIOUS_HIGH_RISK_DEVICE_NIGHTTIME")

        # 4. Blacklist Check
        if txn_data.get('ip_address') in self.blacklisted_ips:
            rule_score += 0.95
            triggered_rules.append("BLACKLISTED_IP_MATCH")
            
        if txn_data.get('card_number') in self.blacklisted_cards:
            rule_score += 0.95
            triggered_rules.append("BLACKLISTED_CARD_MATCH")

        return round(float(np.clip(rule_score, 0.0, 1.0)), 4), triggered_rules

class EnsembleRiskScoringEngine:
    def __init__(self):
        self.supervised_clf = SupervisedFraudClassifier()
        self.sequence_detector = DeepSequenceFraudDetector()
        self.rule_engine = BusinessRuleEngine()
        self.framework_mapper = FrameworkMappingEngine()

    def evaluate_transaction(self, tabular_feats, seq_vector, raw_txn_data):
        """
        Combines Supervised Probability, Sequence Anomaly Score, and Business Rules
        into a single calibrated Risk Score [0 - 100] and decision.
        """
        # 1. Supervised Score
        p_supervised = self.supervised_clf.predict_risk(tabular_feats)
        
        # 2. Sequence Score
        p_sequence = self.sequence_detector.predict_sequence_risk(seq_vector)
        
        # 3. Business Rule Overlay
        r_rules, triggered_rules = self.rule_engine.evaluate_rules(raw_txn_data)
        
        # If severe business rule triggered (e.g. hard velocity or blacklist), ensure rule weight contributes strongly
        if r_rules >= 0.8:
            weights = [0.30, 0.30, 0.40]
        else:
            weights = [config.WEIGHT_SUPERVISED, config.WEIGHT_SEQUENCE, config.WEIGHT_RULES]
            
        ensemble_prob = (weights[0] * p_supervised) + (weights[1] * p_sequence) + (weights[2] * r_rules)
        
        risk_score = round(float(ensemble_prob * 100.0), 2)
        
        # Decision Policy
        if risk_score < config.RISK_THRESHOLD_APPROVE:
            decision = "APPROVE"
            action = "Transaction Approved"
        elif risk_score < config.RISK_THRESHOLD_STEPUP:
            decision = "STEP_UP_AUTHENTICATION"
            action = "Trigger 2FA / OTP Verification"
        else:
            decision = "BLOCK"
            action = "Transaction Blocked & Flagged for Analyst Review"
            
        # Determine Primary Fraud Classification
        primary_fraud_type = self._classify_fraud_category(p_supervised, p_sequence, r_rules, raw_txn_data, risk_score)
        
        # Framework Mapping (OWASP API & PCI DSS)
        framework_context = self.framework_mapper.map_transaction(primary_fraud_type)

        return {
            "transaction_id": raw_txn_data.get("transaction_id", "TXN_UNKNOWN"),
            "account_id": raw_txn_data.get("account_id", "ACC_UNKNOWN"),
            "risk_score": risk_score,
            "decision": decision,
            "recommended_action": action,
            "fraud_category": primary_fraud_type,
            "components": {
                "supervised_score": round(p_supervised * 100, 1),
                "sequence_anomaly_score": round(p_sequence * 100, 1),
                "rule_overlay_score": round(r_rules * 100, 1)
            },
            "triggered_rules": triggered_rules,
            "framework_mapping": framework_context
        }

    def _classify_fraud_category(self, p_sup, p_seq, r_rules, txn, risk_score):
        if risk_score < config.RISK_THRESHOLD_APPROVE:
            return "LEGITIMATE"
            
        # Pattern heuristic for sub-categorization
        if txn.get('account_age_days', 100) < 7:
            return "SYNTHETIC_IDENTITY"
        elif txn.get('velocity_5m', 0) > 3 or any("VELOCITY" in r for r in self.rule_engine.evaluate_rules(txn)[1]):
            return "VELOCITY_ABUSE"
        elif p_seq > 0.65 or txn.get('location_distance_km', 0) > 500:
            return "ACCOUNT_TAKEOVER"
        elif txn.get('merchant_category') == 'digital_goods' and p_sup > 0.5:
            return "CHARGEBACK_FRAUD"
        else:
            return "CNP_FRAUD"
