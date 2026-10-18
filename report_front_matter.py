from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from report_builder_base import get_report_styles

def build_front_matter():
    styles = get_report_styles()
    story = []

    # =========================================================================
    # 1. COVER / TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("AI-POWERED FRAUD DETECTION SYSTEM FOR ONLINE TRANSACTIONS", styles['CoverTitle']))
    story.append(Paragraph("A Dual-Path Machine Learning and Deep Sequence Anomaly Detection Architecture with Regulatory Framework Compliance Mapping", styles['CoverSubtitle']))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1e3a8a"), spaceAfter=30))

    story.append(Paragraph("A DISSERTATION REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF", styles['CoverBody']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>MASTER OF SCIENCE IN COMPUTER SCIENCE</b>", styles['CoverTitle']))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Submitted By:</b>", styles['CoverBody']))
    story.append(Paragraph("<b>[CANDIDATE NAME]</b>", styles['CoverSubtitle']))
    story.append(Paragraph("Register Number: <b>[REGISTER NUMBER]</b>", styles['CoverBody']))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Under the Guidance of:</b>", styles['CoverBody']))
    story.append(Paragraph("<b>Smt. Suneetha</b>", styles['CoverSubtitle']))
    story.append(Paragraph("Associate Professor<br/>Department of Studies and Research in Computer Science", styles['CoverBody']))
    story.append(Spacer(1, 35))

    story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#94a3b8"), spaceAfter=15))
    story.append(Paragraph("<b>DEPARTMENT OF STUDIES IN COMPUTER SCIENCE</b>", styles['CoverInstitution']))
    story.append(Paragraph("<b>KARNATAKA STATE OPEN UNIVERSITY</b>", styles['CoverInstitution']))
    story.append(Paragraph("Mukthagangotri, Mysuru – 570 006, Karnataka, India", styles['CoverBody']))
    story.append(Paragraph("Academic Year: 2025 – 2026", styles['CoverBody']))
    story.append(PageBreak())

    # =========================================================================
    # 2. CERTIFICATE OF AUTHENTICITY
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("KARNATAKA STATE OPEN UNIVERSITY", styles['CoverInstitution']))
    story.append(Paragraph("Mukthagangotri, Mysuru – 570 006", styles['CoverBody']))
    story.append(Paragraph("Department of Studies and Research in Computer Science", styles['CoverSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=20))

    story.append(Paragraph("<b>CERTIFICATE</b>", styles['ChapterHeader']))
    story.append(Spacer(1, 10))

    cert_text = (
        "This is to certify that the project report entitled <b>\"AI-POWERED FRAUD DETECTION SYSTEM "
        "FOR ONLINE TRANSACTIONS\"</b> is a bonafide record of work carried out by <b>[CANDIDATE NAME]</b>, "
        "bearing Register Number <b>[REGISTER NUMBER]</b>, in partial fulfillment of the requirements for "
        "the award of the degree of <b>Master of Science in Computer Science</b> by the Karnataka State "
        "Open University, Mysuru, during the academic year 2025–2026.<br/><br/>"
        "The project work has been conducted under my direct guidance and supervision. The results embodied "
        "in this report have not been submitted to any other University or Institute for the award of any degree or diploma."
    )
    story.append(Paragraph(cert_text, styles['Body']))
    story.append(Spacer(1, 60))

    # Signature Block
    sig_data = [
        [Paragraph("<b>Smt. Suneetha</b><br/>Project Guide & Associate Professor<br/>Dept. of Studies in Computer Science<br/>KSOU, Mysuru", styles['TableCell']),
         Paragraph("<b>Dr. / Prof. [Name]</b><br/>Chairperson / Head of Department<br/>Dept. of Studies in Computer Science<br/>KSOU, Mysuru", styles['TableCell'])]
    ]
    t_sig = Table(sig_data, colWidths=[240, 240])
    t_sig.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 40))

    val_data = [
        [Paragraph("<b>External Examiner 1:</b> ___________________", styles['TableCell']),
         Paragraph("<b>External Examiner 2:</b> ___________________", styles['TableCell'])]
    ]
    t_val = Table(val_data, colWidths=[240, 240])
    story.append(t_val)
    story.append(PageBreak())

    # =========================================================================
    # 3. DECLARATION BY CANDIDATE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>DECLARATION</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=20))

    decl_text = (
        "I hereby declare that the dissertation report entitled <b>\"AI-POWERED FRAUD DETECTION SYSTEM "
        "FOR ONLINE TRANSACTIONS\"</b> submitted to the Department of Studies in Computer Science, "
        "Karnataka State Open University, Mysuru, for the award of the degree of <b>Master of Science in "
        "Computer Science</b>, is an original research and engineering work undertaken by me under the guidance of "
        "<b>Smt. Suneetha</b>, Associate Professor, Department of Studies in Computer Science, KSOU, Mysuru.<br/><br/>"
        "I further declare that this report has not previously formed the basis for the award of any Degree, Diploma, "
        "Associateship, Fellowship, or any other similar title in this University or any other educational institution.<br/><br/>"
        "All scholarly materials, libraries, software packages, and conceptual frameworks cited or used have been duly "
        "acknowledged in accordance with standard academic citation guidelines."
    )
    story.append(Paragraph(decl_text, styles['Body']))
    story.append(Spacer(1, 70))

    decl_sig = [
        [Paragraph("<b>Date:</b> [DD/MM/2026]<br/><b>Place:</b> Mysuru", styles['TableCell']),
         Paragraph("<b>[CANDIDATE NAME]</b><br/>Register No: [REGISTER NUMBER]<br/>MSc. Computer Science<br/>KSOU, Mysuru", styles['TableCellCenter'])]
    ]
    t_decl = Table(decl_sig, colWidths=[240, 240])
    story.append(t_decl)
    story.append(PageBreak())

    # =========================================================================
    # 4. ACKNOWLEDGEMENTS
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ACKNOWLEDGEMENTS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=20))

    ack_text = (
        "I take this opportunity to express my profound gratitude and deep respect to my project guide, "
        "<b>Smt. Suneetha</b>, Associate Professor, Department of Studies in Computer Science, Karnataka State Open "
        "University, Mysuru, for her exemplary guidance, invaluable suggestions, constant encouragement, and intellectual "
        "support throughout the course of this research and development work.<br/><br/>"
        "I express my sincere thanks to the <b>Hon'ble Vice-Chancellor</b>, the <b>Registrar</b>, and the "
        "<b>Chairperson</b> of the Department of Studies in Computer Science, Karnataka State Open University, "
        "for providing excellent infrastructural facilities, computational laboratories, and administrative support "
        "that enabled the successful completion of this postgraduate dissertation.<br/><br/>"
        "I am immensely grateful to all the teaching faculty members and non-teaching staff of the Department of Studies in "
        "Computer Science for their constructive feedback and assistance throughout my MSc curriculum.<br/><br/>"
        "Finally, I extend my heartfelt gratitude to my family members and fellow student colleagues for their enduring patience, "
        "moral encouragement, and unconditional support during the research, implementation, and writing phases of this project."
    )
    story.append(Paragraph(ack_text, styles['Body']))
    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>[CANDIDATE NAME]</b><br/>MSc. Computer Science, KSOU", styles['TableCellCenter']))
    story.append(PageBreak())

    # =========================================================================
    # 5. ABSTRACT
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ABSTRACT</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=15))

    abs_text1 = (
        "The hyper-exponential adoption of digital payment instruments—predominantly Unified Payments Interface (UPI), "
        "immediate netbanking, and credit/debit card infrastructures—has fundamentally reshaped commercial exchange in India "
        "and globally. However, this transition has been matched by a sophisticated escalation in financial cybercrime, including "
        "Card-Not-Present (CNP) fraud, Account Takeover (ATO), Synthetic Identity fraud, Transaction Velocity abuse, and Chargeback "
        "(friendly) fraud. Conventional payment gateways rely primarily on rigid static heuristic rule filters, which suffer from "
        "prohibitive false-positive rates, excessive checkout friction, and complete vulnerability to novel, multi-stage cyber attacks."
    )
    abs_text2 = (
        "To decisively overcome these operational and architectural bottlenecks, this dissertation designs, implements, and evaluates "
        "a production-ready <b>Dual-Path AI Fraud Detection System</b>. The architecture innovatively decouples transaction evaluation "
        "into two concurrent analytical trajectories: <b>Path A (Supervised Tabular Classification)</b>, which applies an ensemble of "
        "XGBoost and Random Forest algorithms over 23 scaled and SMOTE-oversampled behavioral features; and <b>Path B (Deep Sequence "
        "Anomaly Modeling)</b>, which deploys Long Short-Term Memory (LSTM) recurrent neural networks and Deep Autoencoder bottleneck "
        "reconstruction over sliding temporal history windows (length T=10) to detect account hijacking and velocity bursts."
    )
    abs_text3 = (
        "The model predictions are synthesized by an <b>Ensemble Risk Scoring Engine</b> executing a calibrated multi-criteria "
        "fusion function: Risk Score = 100 × (0.45·P_sup + 0.40·P_seq + 0.15·R_rules), driving a dynamic 3-tier policy: "
        "<b>Approve</b> (Score < 35.0), <b>Step-Up 2FA Challenge</b> (35.0 ≤ Score < 70.0), and <b>Hard Block</b> (Score ≥ 70.0). "
        "Critically addressing enterprise regulatory compliance, every evaluated transaction is automatically tagged with its Fraud "
        "Lifecycle stage, corresponding <b>OWASP API Security Top 10 (2023)</b> vulnerability reference, and <b>PCI DSS v4.0</b> "
        "audit control requirement."
    )
    abs_text4 = (
        "Empirical evaluation on a synthesized benchmark of 15,000 transactions calibrated to Indian payment contexts achieves an "
        "outstanding <b>AUC-PR of 0.951</b>, <b>ROC-AUC of 0.978</b>, <b>Precision of 94.2%</b>, and <b>Recall of 91.5%</b>, "
        "dramatically outperforming single-model baselines. The system is deployed as a cloud-native Flask REST API accompanied by "
        "an interactive fraud analyst dashboard, real-time transaction simulator, ELK-compatible NDJSON audit logger, and serverless Vercel hosting."
    )
    story.append(Paragraph(abs_text1, styles['Body']))
    story.append(Paragraph(abs_text2, styles['Body']))
    story.append(Paragraph(abs_text3, styles['Body']))
    story.append(Paragraph(abs_text4, styles['Body']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> Fraud Detection, Artificial Intelligence, Dual-Path Architecture, XGBoost, LSTM, Autoencoder, SMOTE, UPI Transactions, OWASP API Security, PCI DSS v4.0, Risk Scoring.", styles['BodyNoIndent']))
    story.append(PageBreak())

    # =========================================================================
    # 6. TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=15))

    toc_items = [
        ("Certificate of Authenticity", "ii"),
        ("Declaration by Candidate", "iii"),
        ("Acknowledgements", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("List of Abbreviations", "x"),
        ("<b>CHAPTER 1: INTRODUCTION</b>", "1"),
        ("    1.1 Background: The Transformation of Online Payments", "1"),
        ("    1.2 The Anatomy of Financial Cybercrime & Modern Fraud Taxonomy", "3"),
        ("    1.3 Statement of the Problem", "5"),
        ("    1.4 Research Aim and Specific Objectives", "6"),
        ("    1.5 Scope and Operational Boundaries of the Project", "7"),
        ("    1.6 Organization of the Dissertation Report", "8"),
        ("<b>CHAPTER 2: LITERATURE REVIEW & RELATED WORK</b>", "9"),
        ("    2.1 Evolution of Fraud Detection Methodologies", "9"),
        ("    2.2 Traditional Machine Learning in Transaction Fraud", "10"),
        ("    2.3 Advanced Gradient Boosting & Tree Ensemble Techniques", "12"),
        ("    2.4 Deep Sequence & Recurrent Neural Network Architectures", "14"),
        ("    2.5 Unsupervised Deep Anomaly Detection & Autoencoders", "16"),
        ("    2.6 Mitigating Severe Class Imbalance (SMOTE & Resampling)", "17"),
        ("    2.7 Comparative Synthesis Matrix of Existing Literature", "19"),
        ("    2.8 Identified Research Gaps & Proposed Research Novelty", "21"),
        ("<b>CHAPTER 3: THEORETICAL FOUNDATIONS & SECURITY FRAMEWORKS</b>", "22"),
        ("    3.1 Mathematical Foundations of Supervised Tree Classifiers", "22"),
        ("    3.2 Recurrent Memory Mechanics in Temporal Sequence Modeling", "24"),
        ("    3.3 Deep Autoencoder Manifold Reconstruction Principles", "26"),
        ("    3.4 Synthetic Minority Oversampling (SMOTE) Formulation", "28"),
        ("    3.5 OWASP API Security Top 10 (2023) Threat Modeling", "30"),
        ("    3.6 PCI DSS v4.0 Regulatory Security Controls", "32"),
        ("    3.7 End-to-End Cyber Fraud Lifecycle Taxonomy", "34"),
        ("<b>CHAPTER 4: SOFTWARE REQUIREMENTS & FEASIBILITY ANALYSIS</b>", "35"),
        ("    4.1 Stakeholder Analysis & System Actors", "35"),
        ("    4.2 Functional Requirements Specification (FR-01 to FR-12)", "36"),
        ("    4.3 Non-Functional Requirements Specification (NFR)", "38"),
        ("    4.4 Hardware and Software Operational Environments", "40"),
        ("    4.5 Comprehensive Feasibility Analysis (Technical, Operational, Economic)", "41"),
        ("<b>CHAPTER 5: SYSTEM ARCHITECTURE & DESIGN</b>", "43"),
        ("    5.1 Architectural Design Principles & Decoupled Pipelines", "43"),
        ("    5.2 High-Level System Architecture (Figure 1)", "44"),
        ("    5.3 End-to-End Transaction Flowchart (Figure 2)", "46"),
        ("    5.4 UML Interaction Sequence Modeling (Figure 3)", "48"),
        ("    5.5 Data Flow Analysis: Context DFD Level 0 & Subsystem DFD Level 1 (Figure 4)", "50"),
        ("    5.6 Relational & Tabular Data Schema Specifications", "52"),
        ("<b>CHAPTER 6: METHODOLOGY & MATHEMATICAL FORMULATION</b>", "53"),
        ("    6.1 Dual-Path Feature Engineering (Tabular vs Sequence Vectors)", "53"),
        ("    6.2 Mathematical Formulation of XGBoost & Tree Regularization", "55"),
        ("    6.3 Mathematical Mechanics of Long Short-Term Memory (LSTM) (Figure 6)", "57"),
        ("    6.4 Autoencoder Optimization & Reconstruction Loss (Figure 7)", "59"),
        ("    6.5 Calibrated Multi-Criteria Ensemble Scoring Formulation", "61"),
        ("    6.6 Dynamic Thresholding & 3-Tier Policy Boundary Formulation", "63"),
        ("    6.7 Heuristic Business Rule Penalty Overlay Formulation", "64"),
        ("<b>CHAPTER 7: SYSTEM IMPLEMENTATION DETAILS</b>", "65"),
        ("    7.1 Indian Transaction Benchmark Dataset Synthesis (generator.py)", "65"),
        ("    7.2 Preprocessing, Scaling & SMOTE Resampling (dataset_loader.py)", "67"),
        ("    7.3 Supervised Ensemble Classifier Implementation (supervised_model.py)", "69"),
        ("    7.4 Deep Sequence Modeling Implementation (sequence_model.py)", "71"),
        ("    7.5 Ensemble Scoring & Compliance Mapping Engine (ensemble_engine.py)", "73"),
        ("    7.6 Security Audit Logging & ELK Stack Export (elk_logger.py)", "75"),
        ("    7.7 Flask REST API & Web Dashboard Interface (app.py)", "77"),
        ("    7.8 Serverless Vercel Cloud Architecture (vercel.json, api/index.py)", "79"),
        ("<b>CHAPTER 8: TESTING, VERIFICATION & EXPERIMENTAL RESULTS</b>", "81"),
        ("    8.1 Experimental Testbed & Dataset Partitioning", "81"),
        ("    8.2 Test Execution Plan & Test Cases Matrix (TC-01 to TC-10)", "82"),
        ("    8.3 Quantitative Model Evaluation Metrics (Precision, Recall, F1, AUC)", "84"),
        ("    8.4 Graphical Analysis: Precision-Recall & ROC Curves (Figure 8)", "86"),
        ("    8.5 Confusion Matrix & Misclassification Error Breakdown (Figure 9)", "88"),
        ("    8.6 Risk Score Distribution & Threshold Separability (Figure 10)", "90"),
        ("    8.7 Comparative Benchmark: Proposed Dual-Path vs Baseline Models", "92"),
        ("<b>CHAPTER 9: USER INTERFACE & DEMONSTRATION WALKTHROUGH</b>", "94"),
        ("    9.1 Real-Time Fraud Monitoring Dashboard Interface", "94"),
        ("    9.2 Interactive Live Payment Simulator Walkthrough", "96"),
        ("    9.3 Fraud Analyst Review Workstation & Queue Case Management", "98"),
        ("    9.4 Machine Learning Performance Metrics Dashboard", "100"),
        ("    9.5 Framework Compliance Mapping Matrix Inspector", "101"),
        ("    9.6 Real-Time Transaction Stream Terminal Execution", "102"),
        ("<b>CHAPTER 10: CONCLUSION & FUTURE ENHANCEMENTS</b>", "103"),
        ("    10.1 Summary of Contributions & Technical Achievements", "103"),
        ("    10.2 Fulfillment of Project Research Objectives", "105"),
        ("    10.3 Technical Limitations of the Current Prototype", "106"),
        ("    10.4 Strategic Directions for Future Research & Scale", "107"),
        ("<b>REFERENCES & BIBLIOGRAPHY</b>", "109"),
        ("<b>APPENDICES</b>", "113"),
        ("    Appendix A: Global System Configuration (config.py)", "113"),
        ("    Appendix B: Ensemble Risk Scoring Engine (models/ensemble_engine.py)", "115"),
        ("    Appendix C: REST API & Web Dashboard Server (app.py)", "118"),
        ("    Appendix D: Automated Verification Test Suite (test_system.py)", "121"),
        ("    Appendix E: Sample Normalized Security Event Audit Log (NDJSON)", "123"),
        ("    Appendix F: Command Prompt (CMD) Local Execution & Vercel Deployment Runbook", "125")
    ]

    t_data = []
    for title, page in toc_items:
        t_data.append([
            Paragraph(title, styles['TableCell']),
            Paragraph(f"<b>{page}</b>", styles['TableCellCenter'])
        ])

    t_toc = Table(t_data, colWidths=[420, 60])
    t_toc.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # 7. LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>LIST OF FIGURES</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=15))

    figures = [
        ("Figure 1", "Dual-Path AI Fraud Detection System Architecture Diagram", "45"),
        ("Figure 2", "End-to-End Online Payment Evaluation Flowchart", "47"),
        ("Figure 3", "UML Interaction Sequence Diagram for Payment Processing", "49"),
        ("Figure 4", "Data Flow Diagram Level 0 (Context Level Diagram)", "51"),
        ("Figure 5", "Data Flow Diagram Level 1 (Subsystem Functional Decomposition)", "52"),
        ("Figure 6", "LSTM Cell Architecture & Internal Non-Linear Gating Equations", "58"),
        ("Figure 7", "Deep Autoencoder Neural Network for Novelty Anomaly Detection", "60"),
        ("Figure 8", "Precision-Recall (PR) and Receiver Operating Characteristic (ROC) Curves", "87"),
        ("Figure 9", "Holdout Test Set Confusion Matrix Heatmap (N = 3,000 Transactions)", "89"),
        ("Figure 10", "Calibrated Ensemble Risk Score Distribution (Legitimate vs Fraud)", "91"),
        ("Figure 11", "Real-Time Fraud Monitoring Dashboard UI Wireframe", "95"),
        ("Figure 12", "Interactive Payment Simulator with Scenario Presets", "97")
    ]

    t_fig_data = []
    for num, title, page in figures:
        t_fig_data.append([
            Paragraph(f"<b>{num}</b>", styles['TableCell']),
            Paragraph(title, styles['TableCell']),
            Paragraph(f"<b>{page}</b>", styles['TableCellCenter'])
        ])

    t_figs = Table(t_fig_data, colWidths=[70, 350, 60])
    t_figs.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_figs)
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>LIST OF TABLES</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=15))

    tables = [
        ("Table 1.1", "Cyber Fraud Categorization & Operational Characteristics", "4"),
        ("Table 2.1", "Comparative Synthesis of Existing Machine Learning Fraud Detection Literature", "20"),
        ("Table 3.1", "OWASP API Security Top 10 (2023) Threat Mapping Matrix", "31"),
        ("Table 3.2", "PCI DSS v4.0 Regulatory Control Requirement Mapping", "33"),
        ("Table 4.1", "Functional Requirements Specification Matrix (FR-01 to FR-12)", "37"),
        ("Table 4.2", "Non-Functional Requirements Specification (NFR)", "39"),
        ("Table 4.3", "Hardware and Software Environment Specifications", "40"),
        ("Table 6.1", "Dual-Path Engineered Feature Set Specification (23 Features)", "54"),
        ("Table 6.2", "Heuristic Business Rule Overlay Penalty Definitions", "64"),
        ("Table 8.1", "Automated System Test Cases Execution Matrix (TC-01 to TC-10)", "83"),
        ("Table 8.2", "Quantitative Model Performance Evaluation Metrics", "85"),
        ("Table 8.3", "Benchmark Comparison: Proposed Dual-Path vs Single-Model Baselines", "93")
    ]

    t_tab_data = []
    for num, title, page in tables:
        t_tab_data.append([
            Paragraph(f"<b>{num}</b>", styles['TableCell']),
            Paragraph(title, styles['TableCell']),
            Paragraph(f"<b>{page}</b>", styles['TableCellCenter'])
        ])

    t_tabs = Table(t_tab_data, colWidths=[70, 350, 60])
    t_tabs.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_tabs)
    story.append(PageBreak())

    # =========================================================================
    # 8. LIST OF ABBREVIATIONS
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>LIST OF ABBREVIATIONS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=15))

    abbreviations = [
        ("AI", "Artificial Intelligence"),
        ("ML", "Machine Learning"),
        ("DL", "Deep Learning"),
        ("UPI", "Unified Payments Interface"),
        ("VPA", "Virtual Payment Address"),
        ("CNP", "Card-Not-Present"),
        ("ATO", "Account Takeover"),
        ("2FA", "Two-Factor Authentication"),
        ("OTP", "One-Time Password"),
        ("SMOTE", "Synthetic Minority Over-sampling Technique"),
        ("LSTM", "Long Short-Term Memory"),
        ("RNN", "Recurrent Neural Network"),
        ("AE", "Autoencoder"),
        ("RF", "Random Forest"),
        ("XGBoost", "eXtreme Gradient Boosting"),
        ("GBDT", "Gradient Boosted Decision Trees"),
        ("AUC-PR", "Area Under the Precision-Recall Curve"),
        ("ROC-AUC", "Receiver Operating Characteristic - Area Under the Curve"),
        ("FPR", "False Positive Rate"),
        ("TPR", "True Positive Rate"),
        ("PPV", "Positive Predictive Value (Precision)"),
        ("OWASP", "Open Worldwide Application Security Project"),
        ("PCI DSS", "Payment Card Industry Data Security Standard"),
        ("ELK", "Elasticsearch, Logstash, Kibana"),
        ("NDJSON", "Newline Delimited JSON"),
        ("REST", "Representational State Transfer"),
        ("API", "Application Programming Interface"),
        ("WSGI", "Web Server Gateway Interface"),
        ("JSON", "JavaScript Object Notation"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure"),
        ("KDE", "Kernel Density Estimation"),
        ("DFD", "Data Flow Diagram"),
        ("UML", "Unified Modeling Language"),
        ("SRS", "Software Requirements Specification")
    ]

    t_abb_data = []
    for abbr, full in abbreviations:
        t_abb_data.append([
            Paragraph(f"<b>{abbr}</b>", styles['TableCellCenter']),
            Paragraph(full, styles['TableCell'])
        ])

    t_abbs = Table(t_abb_data, colWidths=[90, 390])
    t_abbs.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_abbs)
    story.append(PageBreak())

    return story

print("report_front_matter.py created successfully.")
