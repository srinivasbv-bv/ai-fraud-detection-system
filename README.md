# AI-POWERED FRAUD DETECTION SYSTEM FOR ONLINE TRANSACTIONS

**Synopsis & Complete Implementation of MSc. CS Project**  
*Submitted in partial fulfillment of requirement for the award of the degree of Master of Science in Computer Science*  
**Karnataka State Open University, Mysore**

---

## 1. ABSTRACT & PROJECT OVERVIEW

The rapid growth of online payments and digital banking has been matched by a corresponding rise in transaction fraud, including Card-Not-Present (CNP) fraud, Account Takeover (ATO), Synthetic Identity fraud, Transaction Velocity abuse, and Chargeback (friendly) fraud. Traditional rule-based engines generate high false-positive rates and fail to adapt to evolving fraud patterns.

This project implements an **AI-Powered Fraud Detection System** combining:
1. A **Supervised Classifier** (XGBoost & Random Forest via Scikit-Learn) trained on transaction-level tabular features with **SMOTE** class-imbalance correction.
2. A **Deep Sequence Model** (LSTM & Autoencoders via TensorFlow/Keras) that models per-account temporal behavior to flag account takeover and velocity anomalies.
3. A **Business Rule Engine Overlay** enforcing hard velocity caps, geo-distance mismatches, and blacklists.
4. An **Ensemble Risk Scoring Engine** producing a calibrated risk score (0-100) and a 3-tier decision (*Approve*, *Step-Up Authentication*, *Block*).
5. A **Framework Mapping Engine** tagging every evaluated transaction with its stage in the Fraud Lifecycle, relevant **OWASP API Security Top 10 (2023)** category, and **PCI DSS v4.0** control reference.
6. An **ELK Stack Integration** writing normalized NDJSON log events for Logstash and Elasticsearch indexing.
7. A **Fraud Analyst Web Dashboard & Real-Time Simulator** built with Flask, Bootstrap 5, and Chart.js.

---

## 2. FRAUD FRAMEWORK MAPPING MATRIX

Because online transaction fraud operates over payment and banking APIs, standard infrastructure kill-chain models do not apply cleanly. This system maps each classified fraud type to standard compliance taxonomies:

| Fraud Category | Fraud Lifecycle Stage | OWASP API Security Top 10 (2023) Reference | Primary PCI DSS v4.0 Control Reference |
| :--- | :--- | :--- | :--- |
| **Card-Not-Present (CNP) Fraud** | Monetization | `API4:2023 – Unrestricted Resource Consumption` | PCI DSS Req. 3, 4 |
| **Account Takeover (ATO)** | Account Compromise | `API2:2023 – Broken Authentication` | PCI DSS Req. 8 |
| **Synthetic Identity Fraud** | Account Creation | `API3:2023 – Broken Object Property Level Authorization` | PCI DSS Req. 12 |
| **Transaction Velocity / Anomaly Fraud** | Testing / Probing | `API4:2023 – Unrestricted Resource Consumption` | PCI DSS Req. 10 |
| **Chargeback (Friendly) Fraud** | Post-Transaction Dispute | `API9:2023 – Improper Inventory Management (logging gaps)` | PCI DSS Req. 10 |

---

## 3. SYSTEM ARCHITECTURE

```
                                +-----------------------------------+
                                |     Incoming Online Transaction   |
                                +-----------------------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | Dual-Path Feature Engineering     |
                                +-----------------------------------+
                                  /                               \
                                 /                                 \
  +-------------------------------------+           +-------------------------------------+
  | Path A: Tabular Transaction Features|           | Path B: Per-Account Temporal Seq.  |
  +-------------------------------------+           +-------------------------------------+
                    |                                                  |
                    v                                                  v
  +-------------------------------------+           +-------------------------------------+
  | Supervised Model (XGBoost / RF)    |           | Deep Sequence Model (LSTM / AE)     |
  +-------------------------------------+           +-------------------------------------+
                    \                                                  /
                     \                                                /
                      +----------------------------------------------+
                                             |
                                             v
                              +------------------------------+
                              | Heuristic Business Rule      |
                              | Overlay (Caps, Blacklist)    |
                              +------------------------------+
                                             |
                                             v
                              +------------------------------+
                              | Ensemble Risk Scoring Engine |
                              | Score = 100 * (w1*P1+w2*P2)  |
                              +------------------------------+
                                             |
                                             v
                              +------------------------------+
                              | 3-Tier Decision Engine       |
                              | Score < 35: Approve          |
                              | 35 <= Score < 70: Step-Up 2FA|
                              | Score >= 70: Block           |
                              +------------------------------+
                                             |
                                             v
                              +------------------------------+
                              | OWASP & PCI DSS Tagging      |
                              +------------------------------+
                                  /                      \
                                 v                        v
                  +-----------------------+     +------------------------+
                  | Logstash / Elastic    |     | Fraud Analyst Web UI   |
                  | NDJSON Logs           |     | & Live Simulator       |
                  +-----------------------+     +------------------------+
```

---

## 4. PROJECT STRUCTURE

```
ai_fraud_detection_system/
├── app.py                      # Flask Web Dashboard & Real-Time REST API server
├── train_all.py                # End-to-end model training script
├── test_system.py              # Automated unit and integration verification test suite
├── requirements.txt            # Python package dependencies
├── config.py                   # Global system thresholds, OWASP/PCI mappings, & model hyperparams
├── README.md                   # Academic project documentation
├── data/
│   ├── generator.py            # Synthetic benchmark dataset generator (ULB & IEEE-CIS style)
│   └── dataset_loader.py       # Feature scaling, SMOTE resampling, and sliding window generator
├── models/
│   ├── supervised_model.py     # Random Forest & XGBoost classifiers (CNP, Synthetic ID, Chargeback)
│   ├── sequence_model.py       # TensorFlow/Keras LSTM & Autoencoder models (ATO & Velocity)
│   └── ensemble_engine.py      # Ensemble Risk Scoring Engine & Heuristic Business Rules
├── framework/
│   └── mapping_engine.py       # Fraud Lifecycle, OWASP API Top 10 (2023), & PCI DSS v4.0 tagging
├── logging_elk/
│   ├── elk_logger.py           # Logstash/Elasticsearch NDJSON event formatter & logger
│   └── logstash.conf           # Logstash pipeline configuration snippet
├── templates/
│   ├── layout.html             # Base Bootstrap 5 layout & sidebar
│   ├── index.html              # Main Monitoring Dashboard
│   ├── simulator.html          # Live Interactive Transaction Simulator
│   ├── analyst_queue.html      # Analyst Review Queue & Case Management
│   ├── model_metrics.html      # Machine Learning Model Evaluation (AUC-PR, ROC, F1)
│   └── framework_mapping.html  # OWASP API & PCI DSS Security Audit Matrix
└── static/
    ├── css/style.css           # Custom dark dashboard theme styling
    └── js/main.js              # Chart.js visualization & AJAX client logic
```

---

## 5. QUICK START GUIDE

### Prerequisites
- Python 3.8+
- Operating System: Windows 10/11 or Ubuntu Linux

### Installation

1. Navigate to the project directory:
   ```bash
   cd C:\Users\Srinivas\.gemini\antigravity\scratch\ai_fraud_detection_system
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Model Training
To generate synthetic benchmark datasets and train all ML/DL models (XGBoost, Random Forest, LSTM, Autoencoder):
```bash
python train_all.py
```

### Running Automated Verification Tests
```bash
python test_system.py
```

### Launching the Web Application & Analyst Workstation
Start the Flask web server:
```bash
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

- **Dashboard**: `http://127.0.0.1:5000/`
- **Live Simulator**: `http://127.0.0.1:5000/simulator`
- **Analyst Queue**: `http://127.0.0.1:5000/queue`
- **Model Metrics**: `http://127.0.0.1:5000/metrics`
- **Security Framework Matrix**: `http://127.0.0.1:5000/framework`

---

## 6. REFERENCES

1. Dal Pozzolo et al. (2015), *"Calibrating Probability with Undersampling for Unbalanced Classification"*, IEEE SSCI.
2. Bhattacharyya et al. (2011), *"Data Mining for Credit Card Fraud: A Comparative Study"*, Decision Support Systems.
3. Fiore et al. (2019), *"Using Generative Adversarial Networks for Improving Classification Effectiveness in Credit Card Fraud Detection"*, Information Sciences.
4. Randhawa et al. (2018), *"Credit Card Fraud Detection Using AdaBoost and Majority Voting"*, IEEE Access.
5. Jurgovsky et al. (2018), *"Sequence Classification for Credit-Card Fraud Detection"*, Expert Systems with Applications.
6. OWASP Foundation, *"OWASP API Security Top 10 (2023)"*.
7. PCI Security Standards Council, *"Payment Card Industry Data Security Standard (PCI DSS) v4.0"*.
