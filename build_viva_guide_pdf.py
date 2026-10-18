import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(46, letter[1] - 32, "M.Sc. Computer Science Viva Voce Defense Guide & Feature Presentation Manual")
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 46, letter[1] - 32, "AI-Powered Fraud Detection System")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(46, letter[1] - 38, letter[0] - 46, letter[1] - 38)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 46, 26, footer_text)
        self.drawString(46, 26, "Department of Studies in Computer Science | Karnataka State Open University (KSOU)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(46, 36, letter[0] - 46, 36)
        
        self.restoreState()

def create_qa_card(q_num, question, answer, styles, key_tip=None):
    """
    Renders an elegant two-tone card for Viva questions and answers.
    """
    q_para = Paragraph(f"<b>Q{q_num}: {question}</b>", styles["QAQuestion"])
    a_para = Paragraph(answer, styles["QAAnswer"])
    
    flowables = [q_para, Spacer(1, 4), a_para]
    if key_tip:
        tip_para = Paragraph(f"<b>Key Examiner Takeaway:</b> {key_tip}", styles["QATip"])
        flowables.extend([Spacer(1, 4), tip_para])
        
    t = Table([[flowables]], colWidths=[letter[0] - 92])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor("#CBD5E1")),
        ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor("#2563EB")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def create_feature_card(title, url_route, what_to_show, script_to_say, tech_concepts, expected_q, styles):
    """
    Renders a comprehensive feature presentation breakdown card for lectures.
    """
    content = []
    content.append(Paragraph(f"<b>FEATURE DEMONSTRATION: {title.upper()}</b> &nbsp;&nbsp;<font color='#2563EB'>[Route: {url_route}]</font>", styles["FeatureTitle"]))
    content.append(Spacer(1, 4))
    content.append(Paragraph(f"<b>1. What to Open & Show on Screen:</b><br/>{what_to_show}", styles["FeatureSection"]))
    content.append(Spacer(1, 5))
    
    script_box = Table([[Paragraph(f"<b>Exact Word-for-Word Script to Speak to Lecturers:</b><br/><i>\"{script_to_say}\"</i>", styles["FeatureScript"])]], colWidths=[letter[0] - 116])
    script_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(script_box)
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<b>2. Technical Concepts Behind this Screen:</b><br/>{tech_concepts}", styles["FeatureSection"]))
    content.append(Spacer(1, 4))
    content.append(Paragraph(f"<b>3. Anticipated Examiner Cross-Question & Quick Defense:</b><br/>{expected_q}", styles["FeatureSection"]))
    
    t = Table([[content]], colWidths=[letter[0] - 92])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#1E3A8A")),
        ('LINELEFT', (0,0), (-1,-1), 4.0, colors.HexColor("#1E3A8A")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def build_pdf(filename="Viva_Questions_and_Feature_Explanation_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=46,
        rightMargin=46,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle('DocHeaderBanner', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0F172A'), alignment=1))
    styles.add(ParagraphStyle('DocSubBanner', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#2563EB'), alignment=1))
    styles.add(ParagraphStyle('MetaBanner', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#475569'), alignment=1))
    styles.add(ParagraphStyle('SectionH1', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#1E3A8A'), spaceBefore=10, spaceAfter=4))
    styles.add(ParagraphStyle('SectionH2', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#0F172A'), spaceBefore=6, spaceAfter=2))
    styles.add(ParagraphStyle('BodyCustom', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#334155')))
    styles.add(ParagraphStyle('BodyCustomBold', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#0F172A')))
    
    styles.add(ParagraphStyle('QAQuestion', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#1E3A8A')))
    styles.add(ParagraphStyle('QAAnswer', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor('#1E293B')))
    styles.add(ParagraphStyle('QATip', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor('#047857')))
    
    styles.add(ParagraphStyle('FeatureTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#0F172A')))
    styles.add(ParagraphStyle('FeatureSection', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#334155')))
    styles.add(ParagraphStyle('FeatureScript', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor('#1E3A8A')))

    story = []

    # Title Banner Block
    banner_data = [
        [Paragraph("M.Sc. COMPUTER SCIENCE — PROJECT VIVA VOCE DEFENSE", styles["DocHeaderBanner"])],
        [Spacer(1, 2)],
        [Paragraph("ORAL EXAMINATION QUESTIONS, MODEL ANSWERS & LECTURER PRESENTATION SCRIPT", styles["DocSubBanner"])],
        [Spacer(1, 2)],
        [Paragraph("<b>Project Title:</b> AI-Powered Real-Time Fraud Detection System for Indian Banking Transactions<br/>"
                   "<b>University:</b> Karnataka State Open University (KSOU), Mukthagangothri, Mysuru &nbsp;|&nbsp; "
                   "<b>Project Guide:</b> Smt. Suneetha, Associate Professor, DoS in Computer Science<br/>"
                   "<b>Candidate Name:</b> [CANDIDATE NAME] &nbsp;|&nbsp; <b>Register Number:</b> [REGISTER NUMBER] &nbsp;|&nbsp; <b>Academic Year:</b> 2025–2026", styles["MetaBanner"])]
    ]
    banner_table = Table(banner_data, colWidths=[letter[0] - 92])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#CBD5E1")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 8))

    # Introduction summary
    intro_p = Paragraph(
        "<b>Executive Defense Strategy:</b> The M.Sc. viva examination tests three key pillars: "
        "(1) <b>Mathematical & Algorithmic Foundations</b> (why an ensemble of GBDT + LSTM + Rules is superior to a single model), "
        "(2) <b>Domain Grounding</b> (calibrating specifically for Indian payment rails like UPI, IMPS, RTGS, RuPay, and RBI 2021 Security Guidelines), and "
        "(3) <b>Engineering Execution</b> (achieving sub-25ms inference latency and providing a Human-in-the-Loop triage queue). "
        "Use this guide to master anticipated questions and deliver a structured, confident software demonstration.",
        styles["BodyCustom"]
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    # =========================================================================
    # PART 1: VIVA VOCE QUESTIONS & MODEL ANSWERS
    # =========================================================================
    story.append(Paragraph("PART 1: CORE VIVA VOCE QUESTIONS & HIGH-SCORING ANSWERS", styles["SectionH1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=1, spaceAfter=8))

    # Section 1.1
    story.append(Paragraph("Category A: Project Motivation, Scope & Problem Formulation", styles["SectionH2"]))
    
    story.append(create_qa_card(
        1,
        "What motivated you to select this project, and what specific problem does it solve?",
        "<b>Answer:</b> With over 13 billion monthly UPI transactions and massive expansion in IMPS, RTGS, and RuPay card payments in India, "
        "banking security teams face sophisticated threats including automated bot velocity bursts, credential-stuffing account takeovers (ATO), and card skimming. "
        "Legacy fraud systems rely on rigid, static threshold rules (e.g., flagging any transaction > ₹50,000). These rules yield over 80% false positives, "
        "annoying genuine customers, while failing completely against distributed micro-transaction probing. My project builds an intelligent, real-time "
        "hybrid risk-scoring engine that combines supervised learning, temporal sequence deep learning, and heuristic guardrails to score transactions within "
        "25 milliseconds, satisfying NPCI/RBI switch latency limits.",
        styles,
        key_tip="Highlight the failure of legacy threshold rules (80% false alarms) and the need for sub-25ms real-time intelligence."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        2,
        "What are the major objectives and deliverables of your system?",
        "<b>Answer:</b> The system achieves five major deliverables:<br/>"
        "1. <b>Multi-Model Ensemble Engine:</b> Integrates LightGBM/Gradient Boosting, Bi-directional LSTM for temporal sequences, and deterministic rules.<br/>"
        "2. <b>Three-Tier Decision Policy:</b> Auto-Approve (score &lt;30), Step-Up Authentication / OTP 2FA (score 30–70), and Outright Block (score &gt;70).<br/>"
        "3. <b>Indian Financial Customization:</b> Calibrated in INR (₹) across UPI (P2P/P2M), IMPS, RTGS, NEFT, and domestic RuPay debit/credit cards.<br/>"
        "4. <b>Explainable AI (XAI):</b> Provides human analysts with local feature contribution breakdown for every flagged event.<br/>"
        "5. <b>Regulatory Compliance:</b> Direct architectural mapping to RBI Digital Payment Security Guidelines (2021) and PCI-DSS v4.0.",
        styles,
        key_tip="Emphasize that the system outputs three actionable tiers (Approve, Step-Up 2FA, Block), not just a binary black-box output."
    ))
    story.append(Spacer(1, 8))

    # Section 1.2
    story.append(Paragraph("Category B: Machine Learning & Deep Learning Architecture", styles["SectionH2"]))

    story.append(create_qa_card(
        3,
        "Explain the mathematical formulation and justification of your Hybrid Ensemble. Why not use a single model?",
        "<b>Answer:</b> No single model architecture can simultaneously detect all fraud modalities:<br/>"
        "• <b>Supervised Classifier (Gradient Boosting / LightGBM):</b> Optimizes decision boundaries across static tabular feature interactions (amount, device risk, account age, merchant category).<br/>"
        "• <b>Deep Sequence Detector (Bi-directional LSTM):</b> Processes a sliding window of historical transactions ($N=10$) to capture temporal sequence dynamics (e.g., multiple rapid micro-probing transactions followed by a massive drain).<br/>"
        "• <b>Business Rule Engine:</b> Provides deterministic, zero-latency safety nets for impossible physical travel (>1000 km in 30 mins) and blacklisted credentials.<br/>"
        "The overall calibrated Risk Score [0–100] is calculated as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Risk Score = 100 × ( w₁ · P_supervised + w₂ · P_sequence + w₃ · R_rules )</b><br/>"
        "Default weights are set to <b>w₁=0.45, w₂=0.35, w₃=0.20</b>. If a critical blacklist or velocity cap rule triggers, dynamic re-weighting shifts the rule weight to <b>0.40</b>.",
        styles,
        key_tip="State the ensemble formula and weights clearly. Examiners love to see that you understand how individual outputs combine."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        4,
        "How do you address extreme class imbalance in banking fraud data?",
        "<b>Answer:</b> In commercial banking, fraudulent transactions represent less than 0.1% of all activity. Evaluating such data using standard Accuracy "
        "is fatal (a naive model predicting 'Legitimate' for every transaction achieves 99.9% accuracy while missing 100% of frauds). We resolved this via:<br/>"
        "1. <b>Cost-Sensitive Objective Weighting:</b> Tuned <i>scale_pos_weight</i> in Gradient Boosting to penalize False Negatives heavily.<br/>"
        "2. <b>Imbalance-Resilient Evaluation Metrics:</b> Evaluated performance strictly via <b>Precision-Recall AUC (PR-AUC)</b>, <b>ROC-AUC (0.978)</b>, and <b>F1-Score (0.928)</b>.<br/>"
        "3. <b>Threshold Tuning:</b> Optimized classification cutoffs based on cost-weighted financial risk matrices rather than standard 0.50.",
        styles,
        key_tip="Never say 'accuracy was 99%'. Always explain why PR-AUC and F1-score are the correct metrics for fraud imbalance."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        5,
        "What specific function does the Bi-directional LSTM serve over traditional models?",
        "<b>Answer:</b> Standard machine learning models treat each incoming transaction as an isolated, independent vector <i>X_t</i>. "
        "However, sophisticated fraudsters execute <i>card testing</i> or <i>account probing</i>—they initiate small test payments (₹10, ₹50) across online merchants "
        "to verify whether stolen credentials work before executing a catastrophic drain. The Bi-directional LSTM maintains an internal memory state across "
        "a sequence of $N=10$ prior transactions, tracking amount velocity ratios, inter-transaction time deltas ($\Delta t$), and channel transitions to identify "
        "temporal behavioral drift that static tabular models miss.",
        styles,
        key_tip="LSTMs model temporal dependencies across a sequence of transactions, catching card probing and velocity bursts."
    ))
    story.append(Spacer(1, 8))

    # Page Break for clean layout
    story.append(PageBreak())

    story.append(Paragraph("Category C: Indian Banking Domain & RBI Regulations", styles["SectionH2"]))

    story.append(create_qa_card(
        6,
        "How is your system customized specifically for Indian banking and payment channels?",
        "<b>Answer:</b> Unlike generic Western fraud systems based purely on credit card swipes, our engine is purpose-built for India:<br/>"
        "1. <b>Payment Rails:</b> Native modeling of <b>UPI (P2P & P2M)</b>, <b>IMPS</b>, <b>RTGS</b>, <b>NEFT</b>, and domestic <b>RuPay</b> debit/credit cards.<br/>"
        "2. <b>Currency Dynamics in INR (₹):</b> Calibrated for Indian ticket sizes (small high-frequency UPI Kirana payments vs. high-ticket RTGS corporate transfers).<br/>"
        "3. <b>Indian Geographic Matrix:</b> Evaluates physical travel impossibility across major Indian commercial hubs (e.g., Bengaluru to Delhi in 30 minutes).<br/>"
        "4. <b>Indian Merchant Categories:</b> Integrates domestic MCC categories such as <i>upi_kirana_retail</i>, <i>irctc_railway_booking</i>, <i>utility_bill_payment</i>, and <i>high_risk_crypto_gaming</i>.",
        styles,
        key_tip="Mention UPI, IMPS, RTGS, RuPay, and the Indian city geographic distance matrix."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        7,
        "What is Step-Up Authentication and why is it preferred over outright transaction blocking?",
        "<b>Answer:</b> Outright blocking a transaction causes acute customer friction, cart abandonment, and customer churn whenever a false positive occurs "
        "(e.g., a genuine user buying flight tickets late at night from a new hotel). Step-Up Authentication is a dynamic, risk-based friction mechanism mandated by RBI:<br/>"
        "• Transactions scoring <b>30 to 70</b> are not blocked; instead, the payment gateway demands secondary verification (OTP, mobile biometric fingerprint, or UPI PIN re-entry).<br/>"
        "• If verified, the transaction completes smoothly. If abandoned or failed, it is blocked and escalated to the Analyst Queue.<br/>"
        "This minimizes legitimate payment failures while neutralizing unauthorized account takeovers.",
        styles,
        key_tip="Explain how Step-Up 2FA balances security with customer friction in compliance with RBI directives."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Category D: Software Engineering, Implementation & Deployment", styles["SectionH2"]))

    story.append(create_qa_card(
        8,
        "Explain your software architecture and technology stack.",
        "<b>Answer:</b> The project is architected as a modular, three-tier enterprise microservices system:<br/>"
        "• <b>Inference Backend:</b> Built in Python using <b>Flask / FastAPI</b>. Python enables seamless model serving using PyTorch, Scikit-learn, Joblib, and NumPy.<br/>"
        "• <b>Presentation Layer:</b> Developed using responsive HTML5, modern Tailwind CSS, and interactive Chart.js widgets for live telemetry and risk meters.<br/>"
        "• <b>Production Hosting:</b> Deployed on <b>Vercel</b> with global Edge CDN caching and serverless execution.<br/>"
        "• <b>Audit & SIEM Logging:</b> Outputs structured JSON log events compatible with the ELK Stack (Elasticsearch, Logstash, Kibana) for non-repudiation.",
        styles,
        key_tip="State clearly: Flask/FastAPI backend, PyTorch/Scikit-learn ML core, Tailwind/Chart.js UI, Vercel cloud deployment."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        9,
        "What is the system's inference latency? Can it handle high-volume banking traffic?",
        "<b>Answer:</b> The end-to-end inference pipeline—including JSON payload parsing, feature vectorization, MinMax/Standard scaling, "
        "ensemble model scoring, and rule evaluation—benchmarks at <b>18 to 25 milliseconds per transaction</b> on standard commodity CPU cores. "
        "Because NPCI and major Indian banking switches allocate a 50–100ms processing window for third-party fraud scoring, our system operates well within "
        "real-time production SLAs. Furthermore, horizontal container scaling (via Docker/Kubernetes) allows scaling to thousands of transactions per second.",
        styles,
        key_tip="Latency is 18–25ms, well within the 50ms NPCI switch processing SLA."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Category E: Tough Defense & Examiner Trap Questions", styles["SectionH2"]))

    story.append(create_qa_card(
        10,
        "Examiner Trap Question: 'Your dataset is synthetically generated. How can we trust it works in a real bank?'",
        "<b>Answer (Master Defense):</b> 'Respected Examiner, real commercial banking transaction logs contain sensitive Customer PII and financial records, "
        "strictly protected under the <b>Digital Personal Data Protection (DPDP) Act 2023</b> and RBI confidentiality mandates. Banks are legally prohibited from "
        "releasing live transaction streams for academic research. Therefore, international financial research and benchmark competitions (e.g., Kaggle, IEEE-CIS) "
        "rely on calibrated stochastic synthetic generators. Our dataset generator strictly preserves mathematical statistical properties, Benford's law for currency amounts, "
        "and empirical fraud ratios. Crucially, our machine learning pipeline is completely schema-agnostic: in a commercial bank, the exact same code simply connects to "
        "the bank's Apache Kafka event topic without changing model architecture.'",
        styles,
        key_tip="Do not get defensive. Cite DPDP Act 2023 and explain that your ML pipeline is schema-agnostic and ready for Kafka event streams."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        11,
        "Examiner Trap Question: 'What if an attacker learns your velocity rule (>5 txns in 5 mins) and purposely slows down?'",
        "<b>Answer (Master Defense):</b> 'That is the exact limitation of legacy rule engines that our project directly resolves! If an attacker deliberately slows their attack "
        "to 4 transactions in 5 minutes to evade the rule engine, the rule score will be low. However, their transactions will still trigger high anomaly scores from the "
        "<b>Bi-directional LSTM sequence detector</b> (due to unusual inter-transaction intervals) and the <b>Supervised Classifier</b> (due to unfamiliar device fingerprints, "
        "atypical merchant categories, or geo-jumps). The multi-model ensemble ensures that evading one tier causes detection by the other two.'",
        styles,
        key_tip="Explain defense-in-depth: bypassing the rule engine still triggers the LSTM sequence model and the GBDT classifier."
    ))
    story.append(Spacer(1, 6))

    story.append(create_qa_card(
        12,
        "What are the limitations and future enhancements of your system?",
        "<b>Answer:</b> While the system excels at single-account real-time detection, its current limitations offer exciting research extensions:<br/>"
        "1. <b>Graph Neural Networks (GNN):</b> Modeling cross-account transaction graphs to identify coordinated mule account networks and money laundering rings.<br/>"
        "2. <b>Federated Learning:</b> Enabling multiple Indian banks (e.g., SBI, HDFC, ICICI) to collaboratively train fraud models without centralizing or sharing private customer financial data.<br/>"
        "3. <b>Reinforcement Learning:</b> Dynamically updating decision thresholds based on real-time feedback loops from fraud analyst review queues.",
        styles,
        key_tip="Highlight Graph Neural Networks (GNNs) for mule account rings and Federated Learning for multi-bank privacy."
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # PART 2: HOW TO EXPLAIN EACH FEATURE TO THE LECTURERS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("PART 2: STEP-BY-STEP FEATURE PRESENTATION SCRIPT FOR LECTURERS", styles["SectionH1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=1, spaceAfter=8))

    strategy_p = Paragraph(
        "<b>The 3 Golden Rules When Presenting to Lecturers:</b><br/>"
        "1. <b>Always state the Business Problem first:</b> Before clicking anything, tell the examiners *why* the screen exists in a real bank.<br/>"
        "2. <b>Show, Don't Just Tell:</b> Trigger a live simulation on screen, let the examiners see the risk meter move, and explain the output numbers.<br/>"
        "3. <b>Keep the Focus on Indian Banking:</b> Relate inputs to UPI, Kirana stores, RuPay cards, and RBI Step-Up authentication.",
        styles["BodyCustom"]
    )
    story.append(strategy_p)
    story.append(Spacer(1, 8))

    # Feature 1
    story.append(create_feature_card(
        "Central Command Dashboard & Live Transaction Stream",
        "/",
        "• Open the main landing page.<br/>"
        "• Point to the top KPI metric summary cards: <i>Total Processed</i>, <i>Approval Rate</i>, <i>Step-Up 2FA Rate</i>, <i>Blocked Count</i>, and <i>Average Risk Score</i>.<br/>"
        "• Scroll down to show the incoming live transaction stream table with INR amounts, Indian payment channels, and decision status badges.",
        "Respected Examiners, this is our Central Security Operations Dashboard, designed for banking fraud monitoring teams. In real time, transactions in Indian Rupees (₹) across UPI, IMPS, RTGS, and RuPay card networks are ingested and evaluated by our AI pipeline. For every payment, the system computes a risk score from 0 to 100 and applies our three-tier policy: Auto-Approved, Step-Up 2FA, or Blocked. Notice the fraud distribution chart on the right: it breaks down threats into Account Takeover, Velocity Spikes, and Card Skimming, providing instant situational awareness.",
        "Real-time stream aggregation, asynchronous UI polling, dynamic status classification, and RESTful telemetry synthesis.",
        "<b>Q: How often does this table refresh?</b><br/><b>Answer:</b> The dashboard polls the backend `/api/transactions` and `/api/stats` endpoints asynchronously every 3 seconds, visualizing real-time throughput without page reloads.",
        styles
    ))
    story.append(Spacer(1, 8))

    # Feature 2
    story.append(create_feature_card(
        "Interactive Real-Time Transaction Simulator & Explainable AI Sandbox",
        "/simulator",
        "• Navigate to `/simulator`. Show the interactive parameter sliders (Amount in ₹, Merchant Type, Device Risk, Distance, Velocity, Time).<br/>"
        "• Demonstrate <b>Test Case 1 (Legitimate)</b>: Click 'Simulate Legitimate UPI Payment' and evaluate.<br/>"
        "• Demonstrate <b>Test Case 2 (Attack)</b>: Click 'Simulate Rapid Bot Burst Attack' and evaluate. Show the Explainable AI feature breakdown.",
        "To prove how our machine learning models evaluate transactions in real time, we built this Interactive Simulator Sandbox. Examiners can input custom transaction parameters or test preset scenarios.<br/><br/>First, let's test a normal daily payment: ₹450 at a Kirana store with low device risk. Upon clicking 'Evaluate', the engine computes a Risk Score of 12.4 / 100, resulting in an AUTO-APPROVE decision in just 19 milliseconds.<br/><br/>Now, let's simulate a hostile attack: clicking 'Simulate Rapid Bot Burst Attack' sets velocity to 8 transactions in 5 minutes, amount to ₹48,000, and device risk to 0.85 at 3 AM. The Risk Score immediately jumps to 94.8 / 100, triggering an instant BLOCK & FLAG decision. Below the risk gauge, our Explainable AI breakdown shows exactly why: high velocity burst and untrusted device fingerprint were the primary contributing factors.",
        "Sub-25ms synchronous inference, MinMax scaling, categorical one-hot encoding, ensemble probability weighting, and Explainable AI local attribution.",
        "<b>Q: What does the Device Risk Score represent?</b><br/><b>Answer:</b> It represents client-side telemetry: rooted/jailbroken devices, emulator detection, VPN/Tor IP usage, and untrusted hardware fingerprints.",
        styles
    ))
    story.append(Spacer(1, 8))

    # Page Break for remaining features
    story.append(PageBreak())

    # Feature 3
    story.append(create_feature_card(
        "Fraud Analyst Review Queue & Human-in-the-Loop (HITL) Triage",
        "/queue",
        "• Navigate to `/queue`. Show the filtered list of flagged and Step-Up transactions.<br/>"
        "• Expand one transaction row to reveal forensic telemetry (IP, Device Risk, Account Age, Velocity).<br/>"
        "• Demonstrate the triage action buttons: 'Confirm Fraud', 'Mark False Positive / Release', and 'Trigger 2FA'.",
        "In enterprise banking, fully autonomous systems without human oversight can lead to severe customer friction. Hence, our architecture incorporates a Human-in-the-Loop Analyst Triage Queue. Transactions in the Step-Up zone (30–70) or Blocked zone (>70) are queued here for Level-2 investigation. A bank fraud analyst can inspect the full digital forensics. If customer verification proves genuine, clicking 'Mark False Positive' releases the funds. If confirmed malicious, clicking 'Confirm Fraud' immediately adds the credentials to the business blacklist and logs the event for model retraining.",
        "Human-in-the-Loop (HITL) design, operational workflow state transitions, forensic metadata inspection, and blacklist propagation.",
        "<b>Q: Does human review slow down real-time payments?</b><br/><b>Answer:</b> No. The transaction is instantly held or prompted for OTP at the gateway within 25ms; the analyst queue handles secondary verification and forensic escalation asynchronously.",
        styles
    ))
    story.append(Spacer(1, 8))

    # Feature 4
    story.append(create_feature_card(
        "Model Performance Benchmarks, ROC-AUC & Precision-Recall Curves",
        "/metrics",
        "• Navigate to `/metrics`. Show the interactive Precision-Recall Curve, ROC-AUC Curve (0.978), and Model Comparison Table.<br/>"
        "• Highlight the performance numbers across LightGBM, LSTM, Isolation Forest, and the Hybrid Ensemble.",
        "This section presents our empirical experimental evaluation. In banking fraud detection, accuracy is a misleading metric due to severe class imbalance. Therefore, we evaluate our system using Precision-Recall curves, ROC-AUC, and F1-score. Our Gradient Boosted model achieves an AUC-ROC of 0.978 and an F1-score of 0.928, with Precision at 94.2% and Recall at 91.5%. As shown in the benchmark table, while individual models suffer from either high false alarms or missed anomalies, our Hybrid Ensemble achieves the optimal balance between fraud capture and low customer friction.",
        "Precision-Recall trade-off, ROC-AUC calculation, Confusion Matrix cost weighting, and cross-model empirical benchmarking.",
        "<b>Q: What is the difference between Precision and Recall in fraud detection?</b><br/><b>Answer:</b> Precision is the percentage of flagged transactions that were truly fraud (minimizing false alarms). Recall is the percentage of all actual frauds that our system caught (minimizing financial loss).",
        styles
    ))
    story.append(Spacer(1, 8))

    # Feature 5
    story.append(create_feature_card(
        "Regulatory Compliance & Security Framework Mapping",
        "/framework",
        "• Navigate to `/framework`. Show the interactive cards mapping detected fraud typologies to RBI Guidelines, OWASP API Security, and PCI-DSS.<br/>"
        "• Point to the specific compliance clauses.",
        "To ensure that our project is ready for enterprise adoption rather than remaining a theoretical exercise, we engineered direct compliance mapping to industry standards: (1) The RBI Digital Payment Security Guidelines (2021) for mandatory velocity monitoring and risk-based authentication; (2) OWASP API Security Top 10 for defending payment APIs against credential stuffing and automated bot attacks; and (3) PCI-DSS v4.0 for non-repudiation and immutable audit logging.",
        "Cybersecurity frameworks, regulatory compliance mapping, risk governance, and audit trail architecture.",
        "<b>Q: Why is RBI compliance important for software engineers?</b><br/><b>Answer:</b> Indian banking licenses and payment aggregator approvals (from RBI and NPCI) mandate strict compliance with the 2021 guidelines before any AI system is permitted in production.",
        styles
    ))
    story.append(Spacer(1, 10))

    # Quick Reference Table & Checklist
    story.append(Paragraph("PART 3: QUICK METRIC CHEAT-SHEET & EXAM DAY CHECKLIST", styles["SectionH1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=1, spaceAfter=8))

    cheat_data = [
        [Paragraph("<b>Metric / Parameter</b>", styles["BodyCustomBold"]), Paragraph("<b>Achieved Value</b>", styles["BodyCustomBold"]), Paragraph("<b>Significance for Viva Defense</b>", styles["BodyCustomBold"])],
        [Paragraph("ROC-AUC Score", styles["BodyCustom"]), Paragraph("<b>0.978</b>", styles["BodyCustom"]), Paragraph("Demonstrates near-perfect discrimination between genuine and fraudulent transactions.", styles["BodyCustom"])],
        [Paragraph("Precision-Recall AUC", styles["BodyCustom"]), Paragraph("<b>0.951</b>", styles["BodyCustom"]), Paragraph("Proves strong reliability under extreme class imbalance (low false positives).", styles["BodyCustom"])],
        [Paragraph("F1-Score", styles["BodyCustom"]), Paragraph("<b>0.928</b>", styles["BodyCustom"]), Paragraph("Harmonic mean of precision (94.2%) and recall (91.5%).", styles["BodyCustom"])],
        [Paragraph("Inference Latency", styles["BodyCustom"]), Paragraph("<b>18 – 25 ms</b>", styles["BodyCustom"]), Paragraph("Well below the 50ms NPCI switch real-time processing SLA.", styles["BodyCustom"])],
        [Paragraph("Decision Thresholds", styles["BodyCustom"]), Paragraph("<b>&lt;30 / 30-70 / &gt;70</b>", styles["BodyCustom"]), Paragraph("Auto-Approve / Step-Up OTP 2FA / Block & Analyst Review.", styles["BodyCustom"])],
        [Paragraph("Ensemble Weights", styles["BodyCustom"]), Paragraph("<b>0.45 / 0.35 / 0.20</b>", styles["BodyCustom"]), Paragraph("GBDT Supervised (0.45), LSTM Sequence (0.35), Heuristic Rules (0.20).", styles["BodyCustom"])]
    ]
    cheat_table = Table(cheat_data, colWidths=[130, 90, letter[0] - 92 - 220])
    cheat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F8FAFC"), colors.HexColor("#FFFFFF")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(cheat_table)
    story.append(Spacer(1, 8))

    checklist_p = Paragraph(
        "<b>Exam Day Final Preparation Checklist:</b><br/>"
        "1. <b>Live Deployment URL:</b> Verify `https://ai-fraud-detection-system-five.vercel.app` is reachable on your phone or laptop browser.<br/>"
        "2. <b>Local Offline Backup:</b> Run `python app.py` on your laptop CMD and keep `http://127.0.0.1:5000` open in a backup browser tab.<br/>"
        "3. <b>Project Documentation:</b> Have both the PDF and DOCX copies of your 60–70 page dissertation ready on your desktop.<br/>"
        "4. <b>Confidence & Delivery:</b> Speak clearly, keep answers structured, and always ground your explanations in the Indian digital payment context!",
        styles["BodyCustom"]
    )
    story.append(checklist_p)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Viva Voce PDF successfully created: {filename}")

if __name__ == "__main__":
    build_pdf()
