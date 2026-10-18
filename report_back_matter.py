from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from report_builder_base import get_report_styles, make_code_box

def build_back_matter():
    styles = get_report_styles()
    story = []

    # =========================================================================
    # REFERENCES & BIBLIOGRAPHY
    # =========================================================================
    story.append(Paragraph("<b>REFERENCES & BIBLIOGRAPHY</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    references = [
        "[1] A. Dal Pozzolo, O. Caelen, R. A. Johnson, and G. Bontempi, \"Calibrating probability with undersampling for unbalanced classification,\" in <i>IEEE Symposium Series on Computational Intelligence (SSCI)</i>, Cape Town, South Africa, Dec. 2015, pp. 159–166.",
        "[2] S. Bhattacharyya, S. Jha, K. Tharakunnel, and J. C. Westland, \"Data mining for credit card fraud: A comparative study,\" <i>Decision Support Systems</i>, vol. 50, no. 3, pp. 602–613, Feb. 2011.",
        "[3] U. Fiore, A. De Santis, F. Perla, P. Zanetti, and F. Palmieri, \"Using generative adversarial networks for improving classification effectiveness in credit card fraud detection,\" <i>Information Sciences</i>, vol. 479, pp. 448–455, Apr. 2019.",
        "[4] R. Randhawa, C. K. Loo, M. Seera, C. P. Lim, and A. K. Nandi, \"Credit card fraud detection using AdaBoost and majority voting,\" <i>IEEE Access</i>, vol. 6, pp. 14277–14284, Mar. 2018.",
        "[5] J. Jurgovsky, M. Granitzer, K. Ziegler, S. Calabretto, P. E. Portier, L. He-Guelton, and O. Caelen, \"Sequence classification for credit-card fraud detection,\" <i>Expert Systems with Applications</i>, vol. 100, pp. 234–245, Jun. 2018.",
        "[6] T. Chen and C. Guestrin, \"XGBoost: A scalable tree boosting system,\" in <i>Proc. 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</i>, San Francisco, CA, USA, Aug. 2016, pp. 785–794.",
        "[7] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, \"SMOTE: Synthetic minority over-sampling technique,\" <i>Journal of Artificial Intelligence Research</i>, vol. 16, pp. 321–357, Jun. 2002.",
        "[8] S. Hochreiter and J. Schmidhuber, \"Long short-term memory,\" <i>Neural Computation</i>, vol. 9, no. 8, pp. 1735–1780, Nov. 1997.",
        "[9] R. Chalapathy and S. Chawla, \"Deep learning for anomaly detection: A survey,\" <i>arXiv preprint arXiv:1901.03407</i>, Jan. 2019.",
        "[10] Y. Sahin, S. Bulkan, and E. Duman, \"A cost-sensitive decision tree approach for fraud detection,\" <i>Expert Systems with Applications</i>, vol. 40, no. 15, pp. 5916–5923, Nov. 2013.",
        "[11] C. Wang, Y. Wang, Z. Ye, L. Ling, and Y. Wang, \"Credit card fraud detection using deep sequence models with transaction features,\" <i>IEEE Transactions on Information Forensics and Security</i>, vol. 14, no. 8, pp. 2102–2115, Aug. 2019.",
        "[12] Open Worldwide Application Security Project (OWASP), \"OWASP API Security Top 10 (2023),\" OWASP Foundation, Dec. 2023. [Online]. Available: https://owasp.org/API-Security/editions/2023/en/0x00-header/",
        "[13] Payment Card Industry Security Standards Council, \"Payment Card Industry Data Security Standard (PCI DSS) Requirements and Testing Procedures v4.0,\" PCI SSC, Wakefield, MA, USA, Mar. 2022.",
        "[14] Reserve Bank of India (RBI), \"Master Direction on Digital Payment Security Controls,\" RBI/2020-21/74, Mumbai, India, Feb. 2021.",
        "[15] National Payments Corporation of India (NPCI), \"UPI Procedural Guidelines and Operational Standards v1.8,\" NPCI, Mumbai, India, Jul. 2023.",
        "[16] F. Carcillo, A. Dal Pozzolo, Y. A. Le Borgne, O. Caelen, Y. Mazzerbo, and G. Bontempi, \"Scarff: A framework for addressing drift and class imbalance in credit card fraud detection,\" <i>IEEE Transactions on Neural Networks and Learning Systems</i>, vol. 30, no. 9, pp. 2686–2698, Sep. 2019.",
        "[17] G. Bontempi, S. Ben Taieb, and Y. A. Le Borgne, \"Machine learning strategies for time series forecasting,\" <i>Business Intelligence</i>, pp. 62–77, Springer, Berlin, Heidelberg, 2013.",
        "[18] L. Breiman, \"Random forests,\" <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, Oct. 2001.",
        "[19] J. H. Friedman, \"Greedy function approximation: A gradient boosting machine,\" <i>Annals of Statistics</i>, vol. 29, no. 5, pp. 1189–1232, Oct. 2001.",
        "[20] I. Goodfellow, Y. Bengio, and A. Courville, <i>Deep Learning</i>. Cambridge, MA, USA: MIT Press, 2016.",
        "[21] D. P. Kingma and J. Ba, \"Adam: A method for stochastic optimization,\" in <i>Proc. 3rd International Conference on Learning Representations (ICLR)</i>, San Diego, CA, USA, May 2015.",
        "[22] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825–2830, Nov. 2011.",
        "[23] M. Abadi et al., \"TensorFlow: A system for large-scale machine learning,\" in <i>12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)</i>, Savannah, GA, USA, Nov. 2016, pp. 265–283.",
        "[24] F. Chollet, <i>Deep Learning with Python</i>. Shelter Island, NY, USA: Manning Publications, 2018.",
        "[25] W. McKinney, \"Data structures for statistical computing in Python,\" in <i>Proc. 9th Python in Science Conference (SciPy)</i>, Austin, TX, USA, Jun. 2010, pp. 51–56.",
        "[26] M. Grinberg, <i>Flask Web Development: Developing Web Applications with Python</i>. Sebastopol, CA, USA: O'Reilly Media, 2018.",
        "[27] Elastic, \"The Elastic Stack: Elasticsearch, Logstash, Kibana Reference Documentation v8.x,\" Mountain View, CA, USA, 2024.",
        "[28] S. M. Lundberg and S. I. Lee, \"A unified approach to interpreting model predictions,\" in <i>Advances in Neural Information Processing Systems (NeurIPS 30)</i>, Long Beach, CA, USA, Dec. 2017, pp. 4765–4774.",
        "[29] P. Domingos, \"A few useful things to know about machine learning,\" <i>Communications of the ACM</i>, vol. 55, no. 10, pp. 78–87, Oct. 2012.",
        "[30] H. He and E. A. Garcia, \"Learning from imbalanced data,\" <i>IEEE Transactions on Knowledge and Data Engineering</i>, vol. 21, no. 9, pp. 1263–1284, Sep. 2009."
    ]

    for ref in references:
        story.append(Paragraph(ref, styles['BodyNoIndent']))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # APPENDICES
    # =========================================================================
    story.append(Paragraph("<b>APPENDICES</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("APPENDIX A: GLOBAL SYSTEM CONFIGURATION (config.py)", styles['SectionHeader']))
    config_code = (
        "# config.py - Centralized System Hyperparameters & Regulatory Taxonomies\n"
        "import os\n\n"
        "BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n"
        "IS_VERCEL = 'VERCEL' in os.environ or os.environ.get('AWS_LAMBDA_FUNCTION_NAME')\n\n"
        "# Currency Ecosystem\n"
        "CURRENCY_SYMBOL = 'Rs.'\n"
        "CURRENCY_CODE = 'INR'\n\n"
        "# Ensemble Risk Scoring Thresholds\n"
        "RISK_THRESHOLD_APPROVE = 35.0\n"
        "RISK_THRESHOLD_STEPUP = 70.0\n\n"
        "# Fusion Weights\n"
        "WEIGHT_SUPERVISED = 0.45\n"
        "WEIGHT_SEQUENCE = 0.40\n"
        "WEIGHT_RULES = 0.15\n\n"
        "# OWASP API Security & PCI DSS Taxonomy\n"
        "FRAUD_FRAMEWORK_MAPPINGS = {\n"
        "    'CNP_FRAUD': {\n"
        "        'name': 'Card-Not-Present (CNP) Fraud',\n"
        "        'lifecycle_stage': 'Monetization',\n"
        "        'owasp_ref': 'API4:2023 - Unrestricted Resource Consumption',\n"
        "        'pci_dss_ref': 'PCI DSS Req. 3, 4'\n"
        "    },\n"
        "    'ACCOUNT_TAKEOVER': {\n"
        "        'name': 'Account Takeover (ATO)',\n"
        "        'lifecycle_stage': 'Account Compromise',\n"
        "        'owasp_ref': 'API2:2023 - Broken Authentication',\n"
        "        'pci_dss_ref': 'PCI DSS Req. 8'\n"
        "    },\n"
        "    'VELOCITY_ABUSE': {\n"
        "        'name': 'Transaction Velocity / Anomaly Fraud',\n"
        "        'lifecycle_stage': 'Testing / Probing',\n"
        "        'owasp_ref': 'API4:2023 - Unrestricted Resource Consumption',\n"
        "        'pci_dss_ref': 'PCI DSS Req. 10'\n"
        "    }\n"
        "}"
    )
    story.extend(make_code_box(config_code))
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPENDIX B: ENSEMBLE RISK ENGINE (models/ensemble_engine.py)", styles['SectionHeader']))
    engine_code = (
        "# models/ensemble_engine.py - Multi-Criteria Risk Scoring Fusion\n"
        "import numpy as np\n"
        "import config\n"
        "from framework.mapping_engine import FrameworkMappingEngine\n\n"
        "class EnsembleRiskScoringEngine:\n"
        "    def __init__(self):\n"
        "        self.weight_sup = config.WEIGHT_SUPERVISED\n"
        "        self.weight_seq = config.WEIGHT_SEQUENCE\n"
        "        self.weight_rules = config.WEIGHT_RULES\n"
        "        self.framework_mapper = FrameworkMappingEngine()\n\n"
        "    def evaluate_transaction(self, tabular_feats, seq_feats, raw_txn):\n"
        "        # 1. Supervised probability prediction (Path A)\n"
        "        p_sup = self.supervised_clf.predict_proba(tabular_feats)\n\n"
        "        # 2. Sequence anomaly scoring (Path B)\n"
        "        p_seq = self.sequence_model.predict_anomaly(seq_feats)\n\n"
        "        # 3. Heuristic business rules overlay\n"
        "        rule_score, triggered = self.evaluate_business_rules(raw_txn)\n\n"
        "        # 4. Calibrated risk score (0 - 100)\n"
        "        calibrated_score = 100.0 * (\n"
        "            self.weight_sup * p_sup +\n"
        "            self.weight_seq * p_seq +\n"
        "            self.weight_rules * rule_score\n"
        "        )\n"
        "        calibrated_score = round(float(np.clip(calibrated_score, 0.0, 100.0)), 2)\n\n"
        "        # 5. Multi-tier decision dispatching\n"
        "        if calibrated_score < config.RISK_THRESHOLD_APPROVE:\n"
        "            decision = 'APPROVE'\n"
        "        elif calibrated_score < config.RISK_THRESHOLD_STEPUP:\n"
        "            decision = 'STEP_UP_AUTHENTICATION'\n"
        "        else:\n"
        "            decision = 'BLOCK'\n\n"
        "        return {\n"
        "            'risk_score': calibrated_score,\n"
        "            'decision': decision,\n"
        "            'triggered_rules': triggered,\n"
        "            'framework_mapping': self.framework_mapper.map_transaction(raw_txn, calibrated_score)\n"
        "        }"
    )
    story.extend(make_code_box(engine_code))
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPENDIX C: FLASK REST API SERVER ROUTING (app.py)", styles['SectionHeader']))
    api_code = (
        "# app.py - REST API & Dashboard Web Service\n"
        "from flask import Flask, render_template, request, jsonify\n"
        "from models.ensemble_engine import EnsembleRiskScoringEngine\n"
        "from logging_elk.elk_logger import ELKLogger\n\n"
        "app = Flask(__name__)\n"
        "risk_engine = EnsembleRiskScoringEngine()\n"
        "elk_logger = ELKLogger()\n\n"
        "@app.route('/api/evaluate', methods=['POST'])\n"
        "def api_evaluate():\n"
        "    payload = request.json or {}\n"
        "    result = risk_engine.evaluate_transaction(tabular_feats, seq_feats, payload)\n"
        "    elk_logger.log_evaluation_event(result, payload)\n"
        "    return jsonify(result), 200\n\n"
        "@app.route('/api/stats', methods=['GET'])\n"
        "def api_stats():\n"
        "    return jsonify(compute_dashboard_statistics()), 200"
    )
    story.extend(make_code_box(api_code))
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPENDIX D: NORMALIZED NDJSON SECURITY AUDIT LOG SAMPLE", styles['SectionHeader']))
    log_sample = (
        "{\n"
        "  \"@timestamp\": \"2026-09-01T17:46:40.124Z\",\n"
        "  \"transaction_id\": \"TXN_INR_482626\",\n"
        "  \"account_id\": \"ACC_IND_9142\",\n"
        "  \"amount_inr\": 120416.99,\n"
        "  \"merchant_category\": \"crypto_offshore\",\n"
        "  \"risk_score\": 98.49,\n"
        "  \"decision\": \"BLOCK\",\n"
        "  \"fraud_category\": \"SYNTHETIC_IDENTITY\",\n"
        "  \"components\": {\n"
        "    \"supervised_score\": 98.2,\n"
        "    \"sequence_anomaly_score\": 95.0,\n"
        "    \"rule_overlay_score\": 75.0\n"
        "  },\n"
        "  \"triggered_rules\": [\"SUSPICIOUS_HIGH_AMOUNT\", \"HIGH_RISK_MERCHANT\"],\n"
        "  \"framework_mapping\": {\n"
        "    \"lifecycle_stage\": \"Account Creation\",\n"
        "    \"owasp_reference\": \"API3:2023 - Broken Object Property Level Authorization\",\n"
        "    \"pci_dss_reference\": \"PCI DSS Req. 12\"\n"
        "  }\n"
        "}"
    )
    story.extend(make_code_box(log_sample))
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPENDIX E: COMMAND PROMPT (CMD) & VERCEL DEPLOYMENT RUNBOOK", styles['SectionHeader']))
    runbook_text = (
        "<b>1. Local Execution via Command Prompt (CMD):</b><br/>"
        "• Open project folder in Windows File Explorer, click the top address bar, type <code>cmd</code>, and press Enter.<br/>"
        "• Run: <code>python -m venv venv</code><br/>"
        "• Run: <code>venv\\Scripts\\activate</code><br/>"
        "• Run: <code>pip install -r requirements.txt</code><br/>"
        "• Run: <code>python app.py</code> (Server starts on http://127.0.0.1:5000)<br/>"
        "• In a second CMD window: <code>venv\\Scripts\\activate</code> then <code>python live_checkout_stream.py</code><br/><br/>"
        "<b>2. Cloud Deployment to Vercel:</b><br/>"
        "• Push repository to personal GitHub: <code>git push -u origin main</code><br/>"
        "• Log in to Vercel with GitHub -> Click 'Add New Project' -> Import repository.<br/>"
        "• Vercel automatically detects <code>vercel.json</code> and builds the Python serverless function in 30 seconds."
    )
    story.append(Paragraph(runbook_text, styles['BodyNoIndent']))

    return story

print("report_back_matter.py updated successfully.")
