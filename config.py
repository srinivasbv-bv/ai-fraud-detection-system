import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_VERCEL = "VERCEL" in os.environ or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")

DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = "/tmp" if IS_VERCEL else os.path.join(BASE_DIR, 'logs')

# File Paths
TABULAR_DATASET_PATH = os.path.join(DATA_DIR, 'tabular_transactions.csv')
SEQUENCE_DATASET_PATH = os.path.join(DATA_DIR, 'sequence_transactions.csv')
SUPERVISED_MODEL_PATH = os.path.join(MODELS_DIR, 'xgboost_fraud_model.pkl')
SEQUENCE_MODEL_PATH = os.path.join(MODELS_DIR, 'lstm_sequence_model.h5')
AUTOENCODER_MODEL_PATH = os.path.join(MODELS_DIR, 'autoencoder_model.h5')
SCALER_PATH = os.path.join(MODELS_DIR, 'feature_scaler.pkl')
METRICS_PATH = os.path.join(MODELS_DIR, 'model_evaluation_metrics.json')
NDJSON_LOG_PATH = os.path.join(LOGS_DIR, 'transactions.ndjson')

# Currency Setting
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

# Ensemble Risk Thresholds (0 to 100)
RISK_THRESHOLD_APPROVE = 35.0
RISK_THRESHOLD_STEPUP = 70.0

# Ensemble Scoring Weights
WEIGHT_SUPERVISED = 0.45
WEIGHT_SEQUENCE = 0.40
WEIGHT_RULES = 0.15

# Sequence Sliding Window Length
SEQUENCE_LENGTH = 10

# OWASP & PCI DSS Framework Mappings
FRAUD_FRAMEWORK_MAPPINGS = {
    "CNP_FRAUD": {
        "name": "Card-Not-Present (CNP) Fraud",
        "lifecycle_stage": "Monetization",
        "owasp_ref": "API4:2023 – Unrestricted Resource Consumption",
        "pci_dss_ref": "PCI DSS Req. 3, 4",
        "description": "Unauthorized online purchase using stolen credit/debit card details without OTP verification."
    },
    "ACCOUNT_TAKEOVER": {
        "name": "Account Takeover (ATO)",
        "lifecycle_stage": "Account Compromise",
        "owasp_ref": "API2:2023 – Broken Authentication",
        "pci_dss_ref": "PCI DSS Req. 8",
        "description": "Hacker gains unauthorized access to UPI app / Netbanking account and transfers funds."
    },
    "SYNTHETIC_IDENTITY": {
        "name": "Synthetic Identity Fraud",
        "lifecycle_stage": "Account Creation",
        "owasp_ref": "API3:2023 – Broken Object Property Level Authorization",
        "pci_dss_ref": "PCI DSS Req. 12",
        "description": "Mule account created using forged Aadhaar/PAN details for laundering."
    },
    "VELOCITY_ABUSE": {
        "name": "Transaction Velocity / Anomaly Fraud",
        "lifecycle_stage": "Testing / Probing",
        "owasp_ref": "API4:2023 – Unrestricted Resource Consumption",
        "pci_dss_ref": "PCI DSS Req. 10",
        "description": "Rapid repeated UPI / card payment attempts within short temporal windows."
    },
    "CHARGEBACK_FRAUD": {
        "name": "Chargeback (Friendly) Fraud",
        "lifecycle_stage": "Post-Transaction Dispute",
        "owasp_ref": "API9:2023 – Improper Inventory Management (logging gaps)",
        "pci_dss_ref": "PCI DSS Req. 10",
        "description": "Customer disputes valid digital goods / online gaming payment after consumption."
    },
    "LEGITIMATE": {
        "name": "Legitimate Transaction",
        "lifecycle_stage": "Normal Operation",
        "owasp_ref": "N/A - Standard Compliant API Flow",
        "pci_dss_ref": "PCI DSS Compliant",
        "description": "Transaction verified and consistent with normal Indian spending patterns."
    }
}
