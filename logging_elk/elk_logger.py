import os
import json
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class ELKLogger:
    """
    ELK Stack Log Formatting and Export Utility.
    Generates structured NDJSON log records compatible with Logstash ingestion
    and Elasticsearch indexing.
    """
    def __init__(self, log_filepath=config.NDJSON_LOG_PATH):
        self.log_filepath = log_filepath
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)

    def log_evaluation_event(self, eval_result, raw_txn):
        """
        Formats transaction decision event into Elasticsearch/Logstash standard document.
        """
        log_event = {
            "@timestamp": datetime.utcnow().isoformat() + "Z",
            "log": {"level": "WARN" if eval_result["decision"] != "APPROVE" else "INFO"},
            "transaction": {
                "id": eval_result["transaction_id"],
                "account_id": eval_result["account_id"],
                "amount": raw_txn.get("amount", 0.0),
                "merchant_category": raw_txn.get("merchant_category", "unknown"),
                "device_risk_score": raw_txn.get("device_risk_score", 0.0),
                "location_distance_km": raw_txn.get("location_distance_km", 0.0)
            },
            "fraud_detection": {
                "risk_score": eval_result["risk_score"],
                "decision": eval_result["decision"],
                "action": eval_result["recommended_action"],
                "fraud_category": eval_result["fraud_category"],
                "scores": eval_result["components"],
                "triggered_rules": eval_result["triggered_rules"]
            },
            "compliance_mapping": {
                "lifecycle_stage": eval_result["framework_mapping"]["lifecycle_stage"],
                "owasp_ref": eval_result["framework_mapping"]["owasp_reference"],
                "pci_dss_ref": eval_result["framework_mapping"]["pci_dss_reference"]
            }
        }
        
        # Append to NDJSON log file
        with open(self.log_filepath, 'a') as f:
            f.write(json.dumps(log_event) + '\n')
            
        return log_event

    def get_recent_logs(self, limit=50):
        if not os.path.exists(self.log_filepath):
            return []
        
        logs = []
        with open(self.log_filepath, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        logs.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        return logs[-limit:]
