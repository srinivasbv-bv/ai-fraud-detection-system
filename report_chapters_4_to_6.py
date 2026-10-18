import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from report_builder_base import get_report_styles, make_callout_box

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(PROJECT_DIR, 'assets', 'report_figures')

def build_chapters_4_to_6():
    styles = get_report_styles()
    story = []

    # =========================================================================
    # CHAPTER 4: SOFTWARE REQUIREMENTS & FEASIBILITY ANALYSIS
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 4</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>SOFTWARE REQUIREMENTS & FEASIBILITY ANALYSIS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("4.1 Stakeholder Analysis & System Actors", styles['SectionHeader']))
    story.append(Paragraph(
        "A rigorous Software Requirements Specification (SRS) requires defining the primary human and automated actors "
        "interacting with the AI Fraud Detection System:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>Primary Actor 1: Cardholder / UPI Consumer:</b> Initiates legitimate checkout transactions across e-commerce, food delivery, utility, or peer-to-peer (P2P) portals. Requires sub-100ms frictionless payment authorization without intrusive challenges when risk scores are low.", styles['Bullet']))
    story.append(Paragraph("• <b>Primary Actor 2: Fraud Operations Analyst:</b> Inspects transactions flagged by the system, reviews component risk score attributions, examines triggered heuristic rules, and manually confirms fraud or marks transactions legitimate.", styles['Bullet']))
    story.append(Paragraph("• <b>Primary Actor 3: Payment Gateway / Core Banking API:</b> Automated upstream client (e.g. Razorpay, Paytm, Cashfree, or Core Banking Server) that transmits JSON transaction payloads to the <code>/api/evaluate</code> endpoint and consumes decision directives.", styles['Bullet']))
    story.append(Paragraph("• <b>Secondary Actor 4: Security Compliance Auditor:</b> Evaluates system logs against PCI DSS v4.0 and OWASP API Security requirements during regulatory compliance audits.", styles['Bullet']))

    story.append(Paragraph("4.2 Functional Requirements Specification (FR-01 to FR-12)", styles['SectionHeader']))
    story.append(Paragraph(
        "The functional capabilities of the system are categorized into twelve mandatory technical requirements:",
        styles['Body']
    ))

    fr_data = [
        [Paragraph("<b>Req ID</b>", styles['TableHead']),
         Paragraph("<b>Requirement Title</b>", styles['TableHead']),
         Paragraph("<b>Technical Description & Acceptance Criteria</b>", styles['TableHead']),
         Paragraph("<b>Priority</b>", styles['TableHead'])],
        [Paragraph("<b>FR-01</b>", styles['TableCellCenter']),
         Paragraph("JSON Ingestion", styles['TableCell']),
         Paragraph("Ingest and sanitize standard payment transaction payloads via HTTP POST.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-02</b>", styles['TableCellCenter']),
         Paragraph("Dual-Path Splitting", styles['TableCell']),
         Paragraph("Deconstruct payload into 23 tabular features and 7-metric temporal sequences.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-03</b>", styles['TableCellCenter']),
         Paragraph("Supervised Inference", styles['TableCell']),
         Paragraph("Execute XGBoost / Random Forest model to compute probability scalar P_sup.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-04</b>", styles['TableCellCenter']),
         Paragraph("Sequence Modeling", styles['TableCell']),
         Paragraph("Process sliding window (T=10) via LSTM and Autoencoder to compute P_seq.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-05</b>", styles['TableCellCenter']),
         Paragraph("Heuristic Rule Overlay", styles['TableCell']),
         Paragraph("Evaluate velocity caps, geo-distance speed limits, and blacklist matching.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-06</b>", styles['TableCellCenter']),
         Paragraph("Calibrated Risk Score", styles['TableCell']),
         Paragraph("Compute fused risk score: Score = 100 × (0.45·P_sup + 0.40·P_seq + 0.15·R_rules).", styles['TableCell']),
         Paragraph("Critical", styles['TableCellCenter'])],
        [Paragraph("<b>FR-07</b>", styles['TableCellCenter']),
         Paragraph("3-Tier Action Policy", styles['TableCell']),
         Paragraph("Route decisions to APPROVE (<35), STEP_UP_AUTHENTICATION (35-70), or BLOCK (≥70).", styles['TableCell']),
         Paragraph("Critical", styles['TableCellCenter'])],
        [Paragraph("<b>FR-08</b>", styles['TableCellCenter']),
         Paragraph("OWASP API Tagging", styles['TableCell']),
         Paragraph("Automatically map flagged incidents to OWASP API Security Top 10 (2023).", styles['TableCell']),
         Paragraph("Medium", styles['TableCellCenter'])],
        [Paragraph("<b>FR-09</b>", styles['TableCellCenter']),
         Paragraph("PCI DSS Tagging", styles['TableCell']),
         Paragraph("Tag compliance requirements (Req 3, 4, 8, 10, 12) to each transaction.", styles['TableCell']),
         Paragraph("Medium", styles['TableCellCenter'])],
        [Paragraph("<b>FR-10</b>", styles['TableCellCenter']),
         Paragraph("ELK Stack Logging", styles['TableCell']),
         Paragraph("Emit normalized, ISO-8601 timestamped NDJSON security audit event logs.", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-11</b>", styles['TableCellCenter']),
         Paragraph("Interactive Simulator", styles['TableCell']),
         Paragraph("Provide web UI form with 4 scenario presets (UPI, Card, ATO, Velocity).", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])],
        [Paragraph("<b>FR-12</b>", styles['TableCellCenter']),
         Paragraph("Analyst Resolution", styles['TableCell']),
         Paragraph("Support 1-click manual analyst overrides (Mark Legitimate / Confirm Fraud).", styles['TableCell']),
         Paragraph("High", styles['TableCellCenter'])]
    ]
    t_fr = Table(fr_data, colWidths=[55, 115, 250, 60])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_fr)
    story.append(Paragraph("Table 4.1: Functional Requirements Specification Matrix (FR-01 to FR-12)", styles['Caption']))

    story.append(Paragraph("4.3 Non-Functional Requirements Specification (NFR)", styles['SectionHeader']))
    story.append(Paragraph(
        "Non-functional requirements govern the architectural quality attributes of the system:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>NFR-01 (Inference Latency):</b> End-to-end evaluation latency across dual-path models and rule overlays must execute in under 100 milliseconds for 99% of requests (p99 < 100ms).", styles['Bullet']))
    story.append(Paragraph("• <b>NFR-02 (High Availability & Fault Tolerance):</b> The system must achieve 99.9% availability. If deep sequence neural weights fail to load, the engine must gracefully fallback to mathematical heuristic sequence anomaly scoring without dropping transactions.", styles['Bullet']))
    story.append(Paragraph("• <b>NFR-03 (Data Security & Masking):</b> Payment Card Industry (PCI DSS) rules mandate masking: full 16-digit card numbers must never be displayed or persisted (e.g. stored as <code>459111******1234</code>).", styles['Bullet']))
    story.append(Paragraph("• <b>NFR-04 (Scalability):</b> The stateless REST API architecture must be horizontally scalable across multi-worker clusters and serverless container platforms (Vercel / AWS Lambda).", styles['Bullet']))
    story.append(Paragraph("• <b>NFR-05 (Interpretability):</b> Every risk score must return component breakdown percentages (supervised score, sequence score, rule penalties, triggered heuristic rules) to ensure full algorithmic explainability.", styles['Bullet']))

    story.append(Paragraph("4.4 Hardware and Software Operational Environments", styles['SectionHeader']))
    story.append(Paragraph(
        "Table 4.2 outlines the minimal and recommended hardware/software specifications for development, training, and production hosting:",
        styles['Body']
    ))

    hw_data = [
        [Paragraph("<b>Component</b>", styles['TableHead']),
         Paragraph("<b>Minimum Specification</b>", styles['TableHead']),
         Paragraph("<b>Recommended Production Specification</b>", styles['TableHead'])],
        [Paragraph("Processor (CPU)", styles['TableCell']),
         Paragraph("Dual-Core Intel Core i3 / AMD Ryzen 3 (2.0 GHz)", styles['TableCell']),
         Paragraph("Octa-Core Intel Core i7 / AMD Ryzen 7 (3.6+ GHz)", styles['TableCell'])],
        [Paragraph("System Memory (RAM)", styles['TableCell']),
         Paragraph("8 GB DDR4", styles['TableCell']),
         Paragraph("16 GB – 32 GB DDR4 / DDR5", styles['TableCell'])],
        [Paragraph("Disk Storage", styles['TableCell']),
         Paragraph("5 GB available SSD storage", styles['TableCell']),
         Paragraph("50 GB NVMe PCIe SSD (for ELK logs)", styles['TableCell'])],
        [Paragraph("Operating System", styles['TableCell']),
         Paragraph("Windows 10/11 (64-bit) or Ubuntu Linux 20.04+", styles['TableCell']),
         Paragraph("Ubuntu Linux 22.04 LTS Server / Debian 12", styles['TableCell'])],
        [Paragraph("Python Runtime", styles['TableCell']),
         Paragraph("Python 3.10.x (64-bit)", styles['TableCell']),
         Paragraph("Python 3.11.x / 3.12.x in isolated venv", styles['TableCell'])],
        [Paragraph("Core Libraries", styles['TableCell']),
         Paragraph("NumPy, Pandas, Scikit-Learn, Flask, Joblib", styles['TableCell']),
         Paragraph("XGBoost, TensorFlow/Keras, Imbalanced-Learn, ReportLab", styles['TableCell'])],
        [Paragraph("Cloud Platform", styles['TableCell']),
         Paragraph("Localhost (127.0.0.1:5000)", styles['TableCell']),
         Paragraph("Vercel Serverless Functions / AWS Elastic Beanstalk", styles['TableCell'])]
    ]
    t_hw = Table(hw_data, colWidths=[110, 185, 185])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_hw)
    story.append(Paragraph("Table 4.2: Hardware and Software System Environmental Specifications", styles['Caption']))

    story.append(Paragraph("4.5 Comprehensive Feasibility Analysis", styles['SectionHeader']))
    story.append(Paragraph(
        "A formal three-dimensional feasibility assessment confirms the project's viability:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>Technical Feasibility:</b> High. Python provides an unparalleled ecosystem for scientific computing (Scikit-Learn, XGBoost, TensorFlow, Pandas). Modern standard laptops easily handle training 15,000 records in under 30 seconds. REST API serving with Flask and serverless deployment via Vercel ensure seamless operational accessibility.", styles['Bullet']))
    story.append(Paragraph("• <b>Operational Feasibility:</b> Excellent. The system is designed with a frictionless 3-tier action policy that requires zero human intervention for 90%+ of transactions (auto-approval). Fraud analysts are empowered by an intuitive web dashboard with 1-click review queues, while automated compliance tagging satisfies external auditors.", styles['Bullet']))
    story.append(Paragraph("• <b>Economic Feasibility:</b> Outstanding. Built entirely on open-source, non-proprietary frameworks (Python, Flask, Bootstrap 5, Chart.js, scikit-learn). Free-tier cloud serverless hosting on Vercel enables production deployment with ₹0 infrastructure procurement costs.", styles['Bullet']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: SYSTEM ARCHITECTURE & DESIGN
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 5</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>SYSTEM ARCHITECTURE & DESIGN</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("5.1 Architectural Design Principles & Decoupled Pipelines", styles['SectionHeader']))
    story.append(Paragraph(
        "The AI Fraud Detection System is architected according to principles of <b>Decoupled Analytical Concurrency</b>, "
        "<b>Fail-Safe Graceful Degradation</b>, and <b>Layered Defense-in-Depth</b>. Instead of forcing complex heterogeneous data "
        "into a single unwieldy classifier, the architecture bifurcates the incoming payment payload into two specialized, parallel "
        "analytical pipelines: Path A for static tabular feature interaction, and Path B for sequential temporal behavior.",
        styles['Body']
    ))

    story.append(Paragraph("5.2 High-Level System Architecture Diagram", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 1 illustrates the comprehensive structural architecture of the system, depicting the flow of data from ingestion "
        "through the Dual-Path models, rule overlay, ensemble fusion, and multi-tier decision dispatching:",
        styles['Body']
    ))

    # Embed Figure 1
    fig1_path = os.path.join(FIG_DIR, 'fig1_system_architecture.png')
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=460, height=299))
        story.append(Paragraph("Figure 1: Dual-Path AI Fraud Detection System Architecture Diagram", styles['Caption']))
    else:
        story.append(Paragraph("[Figure 1: System Architecture Diagram]", styles['Caption']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("5.3 End-to-End Transaction Flowchart", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 2 outlines the rigorous sequential logic executed for every transaction request evaluated by the engine:",
        styles['Body']
    ))

    # Embed Figure 2
    fig2_path = os.path.join(FIG_DIR, 'fig2_transaction_flowchart.png')
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=400, height=518))
        story.append(Paragraph("Figure 2: End-to-End Online Payment Evaluation Flowchart", styles['Caption']))
    else:
        story.append(Paragraph("[Figure 2: Transaction Evaluation Flowchart]", styles['Caption']))

    story.append(PageBreak())

    story.append(Paragraph("5.4 UML Interaction Sequence Modeling", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 3 presents the UML Sequence Diagram modeling message exchange protocols between the client, API gateway, "
        "dual-path machine learning engine, compliance mapper, audit logger, and analyst dashboard:",
        styles['Body']
    ))

    # Embed Figure 3
    fig3_path = os.path.join(FIG_DIR, 'fig3_sequence_diagram.png')
    if os.path.exists(fig3_path):
        story.append(Image(fig3_path, width=460, height=307))
        story.append(Paragraph("Figure 3: UML Interaction Sequence Diagram for Payment Processing", styles['Caption']))
    else:
        story.append(Paragraph("[Figure 3: UML Sequence Diagram]", styles['Caption']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("5.5 Data Flow Analysis: Context DFD Level 0", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 4 provides the Context-Level Data Flow Diagram (DFD Level 0), illustrating the boundaries of the system with "
        "external entities (Cardholder/UPI Consumer, Fraud Operations Analyst) and data stores:",
        styles['Body']
    ))

    # Embed Figure 4
    fig4_path = os.path.join(FIG_DIR, 'fig4_dfd_level0.png')
    if os.path.exists(fig4_path):
        story.append(Image(fig4_path, width=460, height=244))
        story.append(Paragraph("Figure 4: Data Flow Diagram Level 0 (Context Level Diagram)", styles['Caption']))
    else:
        story.append(Paragraph("[Figure 4: DFD Level 0]", styles['Caption']))

    story.append(Paragraph("5.6 Relational & Tabular Data Schema Specifications", styles['SectionHeader']))
    story.append(Paragraph(
        "The system processes structured tabular transaction records defined by the following fundamental schema: "
        "<code>transaction_id</code> (String, Primary Key), <code>account_id</code> (String, Foreign Key), "
        "<code>timestamp</code> (ISO-8601 DateTime), <code>amount</code> (Float, INR ₹), "
        "<code>merchant_category</code> (Categorical String, e.g. upi_kirana_retail, food_zomato_swiggy), "
        "<code>device_risk_score</code> (Float, 0.0 - 1.0), <code>location_distance_km</code> (Float, jump distance), "
        "<code>velocity_5m</code> (Integer, count of transactions in last 5 minutes), "
        "<code>account_age_days</code> (Integer), <code>card_age_days</code> (Integer), "
        "<code>hour_of_day</code> (Integer, 0-23), <code>is_weekend</code> (Binary, 0/1), and <code>is_fraud</code> (Binary Label).",
        styles['Body']
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: METHODOLOGY & MATHEMATICAL FORMULATION
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 6</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>METHODOLOGY & MATHEMATICAL FORMULATION</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("6.1 Dual-Path Feature Engineering", styles['SectionHeader']))
    story.append(Paragraph(
        "Feature engineering transforms raw transactional attributes into mathematical vectors optimized for model ingestion. "
        "Table 6.1 delineates the complete 23-feature space synthesized for Path A and Path B:",
        styles['Body']
    ))

    feat_data = [
        [Paragraph("<b>Index Range</b>", styles['TableHead']),
         Paragraph("<b>Feature Name / Group</b>", styles['TableHead']),
         Paragraph("<b>Data Type & Scaling</b>", styles['TableHead']),
         Paragraph("<b>Target Behavioral Signal</b>", styles['TableHead'])],
        [Paragraph("0", styles['TableCellCenter']), Paragraph("amount (INR ₹)", styles['TableCell']), Paragraph("Float, StandardScaler", styles['TableCell']), Paragraph("Monetary size deviation from account mean", styles['TableCell'])],
        [Paragraph("1", styles['TableCellCenter']), Paragraph("device_risk_score", styles['TableCell']), Paragraph("Float [0.0, 1.0]", styles['TableCell']), Paragraph("Emulator detection, root/jailbreak signal", styles['TableCell'])],
        [Paragraph("2", styles['TableCellCenter']), Paragraph("location_distance_km", styles['TableCell']), Paragraph("Float, StandardScaler", styles['TableCell']), Paragraph("Geographical jump distance from prior login", styles['TableCell'])],
        [Paragraph("3", styles['TableCellCenter']), Paragraph("account_age_days", styles['TableCell']), Paragraph("Integer, StandardScaler", styles['TableCell']), Paragraph("Synthetic identity / new account risk", styles['TableCell'])],
        [Paragraph("4", styles['TableCellCenter']), Paragraph("card_age_days", styles['TableCell']), Paragraph("Integer, StandardScaler", styles['TableCell']), Paragraph("Freshly linked stolen VPA / card risk", styles['TableCell'])],
        [Paragraph("5", styles['TableCellCenter']), Paragraph("hour_of_day", styles['TableCell']), Paragraph("Integer [0 - 23]", styles['TableCell']), Paragraph("Nocturnal botnet attack timing", styles['TableCell'])],
        [Paragraph("6", styles['TableCellCenter']), Paragraph("is_weekend", styles['TableCell']), Paragraph("Binary [0, 1]", styles['TableCell']), Paragraph("Weekend dispute & chargeback spikes", styles['TableCell'])],
        [Paragraph("7 – 16", styles['TableCellCenter']), Paragraph("10 PCA/Rolling Latents", styles['TableCell']), Paragraph("Float, StandardScaler", styles['TableCell']), Paragraph("Rolling mean spend, velocity variance", styles['TableCell'])],
        [Paragraph("17 – 22", styles['TableCellCenter']), Paragraph("6 Merchant One-Hot Bits", styles['TableCell']), Paragraph("OneHotEncoder (6 categories)", styles['TableCell']), Paragraph("Kirana, Food, Ecom, Gaming, Travel, Crypto", styles['TableCell'])]
    ]
    t_feat = Table(feat_data, colWidths=[70, 130, 140, 140])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_feat)
    story.append(Paragraph("Table 6.1: Dual-Path Engineered Feature Space Specification (23 Input Dimensions)", styles['Caption']))

    story.append(Paragraph("6.2 Mathematical Formulation of XGBoost & Tree Regularization", styles['SectionHeader']))
    story.append(Paragraph(
        "For an ensemble of $K$ additive trees $\hat{y}_i = \sum_{k=1}^K f_k(x_i)$, the objective function minimized at iteration $t$ is: "
        "$$\text{obj}^{(t)} = \sum_{i=1}^n \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$$ "
        "where $g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ and $h_i = \partial^2_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ are the "
        "first and second-order gradient statistics of the binary cross-entropy loss function. For a fixed tree structure with instance set $I_j$ "
        "at leaf $j$, the optimal leaf weight $w_j^*$ is derived by setting the partial derivative to zero:",
        styles['Body']
    ))
    story.append(Paragraph(
        "$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}, \quad \text{Gain} = \frac{1}{2} \left[ \frac{(\sum_{i \in I_L} g_i)^2}{\sum_{i \in I_L} h_i + \lambda} + \frac{(\sum_{i \in I_R} g_i)^2}{\sum_{i \in I_R} h_i + \lambda} - \frac{(\sum_{i \in I} g_i)^2}{\sum_{i \in I} h_i + \lambda} \right] - \gamma$$",
        styles['Formula']
    ))

    story.append(Paragraph("6.3 Mathematical Mechanics of Long Short-Term Memory (LSTM)", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 6 illustrates the internal gating mechanics of the LSTM recurrent unit deployed in Path B:",
        styles['Body']
    ))

    # Embed Figure 6
    fig6_path = os.path.join(FIG_DIR, 'fig6_lstm_cell.png')
    if os.path.exists(fig6_path):
        story.append(Image(fig6_path, width=440, height=285))
        story.append(Paragraph("Figure 6: LSTM Cell Architecture & Internal Non-Linear Gating Equations", styles['Caption']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("6.4 Autoencoder Mathematical Loss Formulation", styles['SectionHeader']))
    story.append(Paragraph(
        "Figure 7 depicts the Deep Autoencoder compression and reconstruction manifold utilized for unsupervised novelty detection:",
        styles['Body']
    ))

    # Embed Figure 7
    fig7_path = os.path.join(FIG_DIR, 'fig7_autoencoder.png')
    if os.path.exists(fig7_path):
        story.append(Image(fig7_path, width=440, height=233))
        story.append(Paragraph("Figure 7: Deep Autoencoder Neural Network for Novelty Anomaly Detection", styles['Caption']))

    story.append(Paragraph("6.5 Calibrated Multi-Criteria Ensemble Scoring Formulation", styles['SectionHeader']))
    story.append(Paragraph(
        "The central innovation of our decision architecture is the calibrated multi-criteria fusion function. Let $P_{sup} \in [0, 1]$ "
        "be the supervised probability, $P_{seq} \in [0, 1]$ be the sequential anomaly probability, and $R_{rules} \in [0, 1]$ be the "
        "normalized heuristic rule penalty. The global calibrated risk score $S \in [0, 100]$ is computed as:",
        styles['Body']
    ))
    story.append(Paragraph(
        "$$S = 100 \times \left( w_1 P_{sup} + w_2 P_{seq} + w_3 R_{rules} \right), \quad \text{where } w_1=0.45, \; w_2=0.40, \; w_3=0.15$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "The weights reflect optimal risk attribution: supervised classification carries 45% weight for known fraud patterns; "
        "deep sequence modeling carries 40% weight to catch behavioral shifts and ATO hijacking; and heuristic business rules contribute "
        "15% to enforce immediate deterministic safety overrides.",
        styles['Body']
    ))

    story.append(Paragraph("6.6 Dynamic Thresholding & 3-Tier Policy Boundary Formulation", styles['SectionHeader']))
    story.append(Paragraph(
        "The system evaluates the calibrated score $S$ against two global decision thresholds $(\theta_1 = 35.0, \; \theta_2 = 70.0)$:",
        styles['Body']
    ))
    story.append(Paragraph(
        "$$\text{Decision}(S) = \\begin{cases} \text{APPROVE} & \\text{if } 0.0 \\le S < 35.0 \\\\ \\text{STEP\\_UP\\_AUTHENTICATION (2FA)} & \\text{if } 35.0 \\le S < 70.0 \\\\ \\text{BLOCK} & \\text{if } 70.0 \\le S \\le 100.0 \\end{cases}$$",
        styles['Formula']
    ))

    story.append(Paragraph("6.7 Heuristic Business Rule Penalty Overlay Formulation", styles['SectionHeader']))
    story.append(Paragraph(
        "Table 6.2 formalizes the specific heuristic business rules overlaid onto the machine learning predictions:",
        styles['Body']
    ))

    rule_data = [
        [Paragraph("<b>Rule Identifier</b>", styles['TableHead']),
         Paragraph("<b>Condition Predicate</b>", styles['TableHead']),
         Paragraph("<b>Penalty</b>", styles['TableHead']),
         Paragraph("<b>Targeted Attack Threat</b>", styles['TableHead'])],
        [Paragraph("HIGH_VELOCITY_BURST", styles['TableCell']), Paragraph("velocity_5m > 5 transactions", styles['TableCell']), Paragraph("+0.40", styles['TableCellCenter']), Paragraph("Automated botnet card probing", styles['TableCell'])],
        [Paragraph("IMPOSSIBLE_GEO_SPEED", styles['TableCell']), Paragraph("location_distance_km > 500 km", styles['TableCell']), Paragraph("+0.30", styles['TableCellCenter']), Paragraph("Cross-border credential reuse", styles['TableCell'])],
        [Paragraph("SUSPICIOUS_HIGH_AMOUNT", styles['TableCell']), Paragraph("amount > ₹1,50,000 INR", styles['TableCell']), Paragraph("+0.25", styles['TableCellCenter']), Paragraph("Catastrophic fund drain attempt", styles['TableCell'])],
        [Paragraph("HIGH_RISK_MERCHANT", styles['TableCell']), Paragraph("category == 'crypto_offshore'", styles['TableCell']), Paragraph("+0.35", styles['TableCellCenter']), Paragraph("Offshore money laundering", styles['TableCell'])],
        [Paragraph("NEW_ACCOUNT_SURGE", styles['TableCell']), Paragraph("account_age < 7 & amount > ₹50,000", styles['TableCell']), Paragraph("+0.30", styles['TableCellCenter']), Paragraph("Synthetic identity bust-out", styles['TableCell'])]
    ]
    t_rule = Table(rule_data, colWidths=[120, 150, 60, 150])
    t_rule.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rule)
    story.append(Paragraph("Table 6.2: Heuristic Business Rule Penalty Overlay Mathematical Definitions", styles['Caption']))
    story.append(PageBreak())

    return story

print("report_chapters_4_to_6.py created successfully.")
