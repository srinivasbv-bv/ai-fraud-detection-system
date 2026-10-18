from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from report_builder_base import get_report_styles, make_callout_box

def build_chapters_1_to_3():
    styles = get_report_styles()
    story = []

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 1</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>INTRODUCTION</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("1.1 Background: The Transformation of Online Payments", styles['SectionHeader']))
    story.append(Paragraph(
        "Over the past decade, the global financial technology (FinTech) landscape has undergone a profound structural shift "
        "from physical cash and legacy magnetic-stripe card payments to instant, cloud-native digital transactions. In India, "
        "this revolution has been spearheaded by the Unified Payments Interface (UPI) developed by the National Payments "
        "Corporation of India (NPCI), alongside ubiquitous mobile wallets, Immediate Payment Service (IMPS), and tokenized "
        "e-commerce checkout gateways (Amazon India, Flipkart, Zomato, Swiggy, IRCTC). The volume of instantaneous digital "
        "payments has surged exponentially, processing tens of billions of transactions monthly totaling trillions of Indian Rupees (₹).",
        styles['Body']
    ))
    story.append(Paragraph(
        "While this digital transformation has unlocked unprecedented economic velocity, commercial convenience, and financial "
        "inclusion across urban and rural demographics, it has simultaneously opened expansive attack surfaces for sophisticated "
        "cybercrime syndicates. Because transactions are cleared and settled in sub-second intervals—often without requiring "
        "physical card presentation or face-to-face biometric authentication—fraudulent actors can orchestrate large-scale "
        "automated exploits that drain consumer accounts, exhaust merchant processing limits, and compromise banking institutions "
        "before defensive perimeters can react.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Historically, commercial banking fraud defense relied almost exclusively on static, deterministic rule engines. These "
        "legacy rule systems apply hardcoded threshold conditions—such as flagging any single transaction exceeding ₹50,000, "
        "blocking payments originating from foreign IP subnets, or declining cards with three consecutive incorrect PIN entries. "
        "However, modern cybercriminals easily circumvent static thresholds through automated credential stuffing, distributed proxy "
        "networks, low-and-slow transaction probing, and social engineering attacks.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Furthermore, rigid rules create an untenable operational dilemma: tightening rule thresholds to catch stealthy fraud "
        "triggers unacceptable false-positive rates that decline legitimate customers (known as 'merchant friction' or false declines), "
        "whereas loosening rules leads to catastrophic chargeback liabilities and regulatory sanctions under the Reserve Bank of India (RBI) "
        "and international payment networks (Visa, Mastercard, RuPay). Consequently, there is an urgent and critical imperative "
        "for intelligent, adaptive, multi-layered Artificial Intelligence (AI) and Machine Learning (ML) architectures capable of "
        "evaluating payment risk in real time with high precision and low operational latency.",
        styles['Body']
    ))

    story.append(Paragraph("1.2 The Anatomy of Financial Cybercrime & Modern Fraud Taxonomy", styles['SectionHeader']))
    story.append(Paragraph(
        "To formulate an effective computational defense, it is essential to rigorously deconstruct the primary fraud modalities "
        "observed across modern digital payment networks. Unlike generic network intrusion attempts, payment fraud operates "
        "at the application layer and exploits vulnerabilities in authentication workflows, identity validation pipelines, and "
        "temporal behavioral consistency. This dissertation targets the five most prevalent and destructive fraud categories:",
        styles['Body']
    ))

    fraud_types = [
        ("1. Card-Not-Present (CNP) Fraud:", 
         "Occurs when an unauthorized adversary obtains compromised credit or debit card credentials (PAN, expiration date, CVV) "
         "via phishing, dark web dumps, or database breaches, and executes online e-commerce or offshore purchases without physical "
         "card possession. Adversaries frequently bypass OTPs through SIM-swapping or social engineering vishing calls."),
        ("2. Account Takeover (ATO):", 
         "Involves an unauthorized perpetrator gaining full control of an existing, legitimate customer's mobile banking app, "
         "UPI Virtual Payment Address (VPA), or netbanking portal through credential stuffing, malware keyloggers, or session hijacking. "
         "Once inside, the attacker alters security settings and rapidly transfers funds to offshore crypto exchanges or mule accounts."),
        ("3. Synthetic Identity Fraud:", 
         "One of the fastest-growing financial crimes, wherein criminals combine authentic and fabricated personal identifying "
         "information (such as stolen PAN cards, forged Aadhaar documents, and fake utility bills) to establish brand-new credit profiles. "
         "These accounts are systematically nurtured over months until high credit limits are granted, after which perpetrators execute "
         "maximum cash-out transactions and permanently abandon the identity ('bust-out fraud')."),
        ("4. Transaction Velocity Abuse & Probing:", 
         "Characterized by rapid-fire, high-frequency payment attempts launched by automated botnets against payment APIs within extremely "
         "short temporal windows (<5 minutes). Attackers use velocity bursts to brute-force card details, test active limits on compromised "
         "cards, or exploit inventory reservation locks on flash sales and digital gaming platforms (Dream11, MPL)."),
        ("5. Chargeback (Friendly) Fraud:", 
         "Occurs when a legitimate consumer makes an authentic online purchase—predominantly for consumed digital goods, food delivery, "
         "or online gaming tokens—and subsequently files a false dispute or chargeback with their issuing bank claiming they never "
         "authorized the purchase or never received the items, thereby defrauding the merchant of both goods and capital.")
    ]

    for title, desc in fraud_types:
        story.append(Paragraph(f"<b>{title}</b> {desc}", styles['Bullet']))

    story.append(Spacer(1, 8))

    # Table 1.1: Fraud Operational Characteristics
    t1_data = [
        [Paragraph("<b>Fraud Category</b>", styles['TableHead']),
         Paragraph("<b>Primary Vector</b>", styles['TableHead']),
         Paragraph("<b>Key Behavioral Signals</b>", styles['TableHead']),
         Paragraph("<b>Financial Impact</b>", styles['TableHead'])],
        [Paragraph("<b>CNP Fraud</b>", styles['TableCell']),
         Paragraph("Stolen card credentials, phishing, data breaches", styles['TableCell']),
         Paragraph("Unusual amount, foreign IP, mismatch billing address", styles['TableCell']),
         Paragraph("Direct chargeback liabilities, merchant fines", styles['TableCell'])],
        [Paragraph("<b>Account Takeover (ATO)</b>", styles['TableCell']),
         Paragraph("Credential stuffing, SIM swap, session hijack", styles['TableCell']),
         Paragraph("Abrupt device change, impossible geo-speed jump, nocturnal hour", styles['TableCell']),
         Paragraph("Total account drain, severe reputational loss", styles['TableCell'])],
        [Paragraph("<b>Synthetic Identity</b>", styles['TableCell']),
         Paragraph("Fabricated PII, mule account creation", styles['TableCell']),
         Paragraph("Zero credit history, recent account age, maximum limit drain", styles['TableCell']),
         Paragraph("Unrecoverable bad debt, systemic banking write-offs", styles['TableCell'])],
        [Paragraph("<b>Velocity Abuse</b>", styles['TableCell']),
         Paragraph("Automated botnets, script fuzzing, carding runs", styles['TableCell']),
         Paragraph("High frequency (>5 txns in 5 min), rapid successive failures", styles['TableCell']),
         Paragraph("Gateway interchange fees, inventory lockouts", styles['TableCell'])],
        [Paragraph("<b>Chargeback Fraud</b>", styles['TableCell']),
         Paragraph("Consumer abuse, false non-receipt disputes", styles['TableCell']),
         Paragraph("Digital goods consumption, repeat dispute history", styles['TableCell']),
         Paragraph("Processor penalty fees, revenue depletion", styles['TableCell'])]
    ]
    t1 = Table(t1_data, colWidths=[100, 120, 160, 100])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Paragraph("Table 1.1: Cyber Fraud Categorization, Attack Vectors & Behavioral Indicators", styles['Caption']))

    story.append(Paragraph("1.3 Statement of the Problem", styles['SectionHeader']))
    story.append(Paragraph(
        "Modern digital payment ecosystems operate under extreme performance constraints. In commercial payment gateways, "
        "authorization decisions must be rendered in fewer than 100 milliseconds to preserve user experience. Within this ultra-low "
        "latency envelope, traditional fraud mitigation systems suffer from four foundational deficiencies:",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>1. Static Inflexibility and High False-Positive Ratios:</b> Rule-based filters lack the capacity to discern contextual "
        "nuance. When rules are calibrated strictly to prevent fraud, they inadvertently decline legitimate high-value customers, "
        "eroding consumer trust and inflicting severe commercial revenue losses.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "<b>2. Blindness to Temporal Sequence and Behavioral Drift:</b> Traditional tabular machine learning models treat each "
        "transaction as an isolated, independent and identically distributed (i.i.d.) event. Consequently, they fail to detect "
        "Account Takeover attacks that manifest across sequential time steps—such as an attacker silently probing small transactions "
        "over two days before executing a catastrophic fund drain.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "<b>3. The Curse of Severe Class Imbalance:</b> In real-world payment networks, fraudulent transactions typically constitute "
        "less than 0.5% to 1.0% of total payment volume. Standard objective loss functions cause machine learning models to converge "
        "toward trivial majority-class classifiers, yielding 99% accuracy while missing virtually all fraudulent intrusions.",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "<b>4. Complete Absence of Regulatory and Audit Compliance Mapping:</b> Prevailing machine learning systems operate as "
        "uninterpretable 'black boxes', outputting raw probability scalars without correlating flagged events to industry security "
        "standards such as the <b>OWASP API Security Top 10 (2023)</b> or <b>PCI DSS v4.0</b>. Security operations analysts are left "
        "without actionable remediation context during forensic audits.",
        styles['Bullet']
    ))

    story.append(Paragraph("1.4 Research Aim and Specific Objectives", styles['SectionHeader']))
    story.append(Paragraph(
        "The overarching aim of this postgraduate research is to conceptualize, engineer, evaluate, and deploy an enterprise-grade "
        "<b>AI-Powered Fraud Detection System for Online Transactions</b> that simultaneously resolves the dual challenges of "
        "accurate pattern recognition on isolated transactions and temporal anomaly detection across behavioral sequences, "
        "while providing automated compliance mapping under international cybersecurity frameworks.",
        styles['Body']
    ))
    story.append(Paragraph("To fulfill this primary aim, the following specific technical objectives are formulated:", styles['BodyNoIndent']))

    objectives = [
        ("Objective 1 (Data Synthesis & Resampling Pipeline):", 
         "To engineer a comprehensive synthetic benchmark dataset modeling 15,000 online transactions calibrated to Indian payment contexts "
         "(UPI QR, Food Delivery, E-Commerce, Online Gaming, IRCTC) and apply Synthetic Minority Over-sampling Technique (SMOTE) to overcome severe class imbalance."),
        ("Objective 2 (Dual-Path ML Architecture Engineering):", 
         "To design and implement a decoupled Dual-Path detection architecture: Path A deploying tree-based supervised ensembles "
         "(XGBoost and Random Forest) over tabular features; and Path B deploying Long Short-Term Memory (LSTM) recurrent networks and Deep "
         "Autoencoders over sliding temporal sequence windows (T=10) to detect temporal ATO anomalies."),
        ("Objective 3 (Calibrated Multi-Criteria Risk Engine):", 
         "To develop a unified Ensemble Risk Scoring Engine that fuses supervised classification probabilities, deep sequence anomaly "
         "reconstruction errors, and heuristic rule penalties into a calibrated risk score (0–100) driving a dynamic 3-tier action policy: "
         "Approve (Score < 35), Step-Up 2FA Challenge (35 ≤ Score < 70), and Hard Block (Score ≥ 70)."),
        ("Objective 4 (Enterprise Regulatory Mapping Engine):", 
         "To establish an automated compliance mapping engine that programmatically correlates every evaluated transaction with its "
         "specific Fraud Lifecycle stage, OWASP API Security Top 10 (2023) vulnerability taxonomy, and PCI DSS v4.0 audit requirements."),
        ("Objective 5 (Full-Stack Deployment & Analyst Workstation):", 
         "To implement a production-ready Flask REST API server integrated with an interactive Bootstrap 5 fraud analyst dashboard, "
         "real-time payment stream simulator, Logstash/Elasticsearch NDJSON logging service, and serverless Vercel cloud deployment.")
    ]

    for title, desc in objectives:
        story.append(Paragraph(f"<b>{title}</b> {desc}", styles['Bullet']))

    story.append(Paragraph("1.5 Scope and Operational Boundaries of the Project", styles['SectionHeader']))
    story.append(Paragraph(
        "The scope of this project encompasses the complete end-to-end lifecycle of an online payment security engine: "
        "from transactional data synthesis and feature transformation, through model training, cross-validation, and ensemble scoring, "
        "to REST API serving and interactive analyst visualization. The experimental evaluation is grounded in Indian financial "
        "instruments (UPI VPAs, Netbanking IDs, Indian Rupee amounts).",
        styles['Body']
    ))
    story.append(Paragraph(
        "Operational boundaries: The system is designed as an application-layer analytical engine that interfaces with payment gateways "
        "via JSON payloads. It does not replace low-level network firewalls or TLS encryption pipelines, but operates at the API layer "
        "to inspect transactional integrity, customer velocity, and behavioral consistency before payment authorization is finalized.",
        styles['Body']
    ))

    story.append(Paragraph("1.6 Organization of the Dissertation Report", styles['SectionHeader']))
    story.append(Paragraph(
        "The remainder of this dissertation report is systematically structured into ten comprehensive chapters:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>Chapter 2 (Literature Review):</b> Surveys scholarly and industrial literature on machine learning, deep learning, and rule engines in financial cybercrime defense, highlighting existing research gaps.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 3 (Theoretical Foundations & Frameworks):</b> Explores the mathematical underpinnings of tree ensembles, LSTM gating mechanics, autoencoder manifold learning, SMOTE, and OWASP/PCI DSS standards.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 4 (Requirements Specification & Feasibility):</b> Details stakeholder roles, functional (FR-01 to FR-12) and non-functional requirements, and technical/economic feasibility.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 5 (System Architecture & Design):</b> Presents high-level architectural block diagrams, end-to-end flowcharts, UML sequence diagrams, and Data Flow Diagrams (DFD Level 0 and 1).", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 6 (Methodology & Mathematical Formulation):</b> Rigorously defines the dual-path feature engineering formulas, XGBoost loss regularization, LSTM equations, ensemble scoring functions, and rule penalties.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 7 (Detailed Implementation Details):</b> Explains the technical code implementation across all modular components (generator, loader, supervised model, sequence model, ensemble engine, ELK logging, and API server).", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 8 (Testing, Verification & Experimental Results):</b> Documents the verification testbed, automated test execution matrix, confusion matrices, ROC/PR curves, and comparative benchmark evaluations.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 9 (User Interface & Demonstration Walkthrough):</b> Provides visual walkthroughs of the monitoring dashboard, live simulator, analyst review workstation, and streaming execution.", styles['Bullet']))
    story.append(Paragraph("• <b>Chapter 10 (Conclusion & Future Work):</b> Summarizes research contributions, reviews objective fulfillment, discusses prototype limitations, and outlines future scalability directions.", styles['Bullet']))
    story.append(Paragraph("• <b>References & Appendices:</b> Provides full bibliographic citations in IEEE format and core source code listings.", styles['Bullet']))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW & RELATED WORK
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 2</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>LITERATURE REVIEW & RELATED WORK</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("2.1 Evolution of Fraud Detection Methodologies", styles['SectionHeader']))
    story.append(Paragraph(
        "The science of financial fraud detection has evolved through three distinct paradigms over the past four decades: "
        "first, deterministic expert rule systems; second, shallow statistical and supervised machine learning classifiers; and third, "
        "modern deep learning, sequence modeling, and hybrid ensemble architectures.",
        styles['Body']
    ))
    story.append(Paragraph(
        "In early electronic payment implementations (1980s–1990s), fraud mitigation relied on expert systems comprising collections "
        "of Boolean rules created manually by human risk analysts. While deterministic rules provided instant execution latency and "
        "100% interpretability, they suffered from catastrophic maintenance overhead: as fraudsters modified their tactics, analysts "
        "continually appended new rules, resulting in unwieldy rule sets that contradicted one another and generated intolerable false alarms.",
        styles['Body']
    ))
    story.append(Paragraph(
        "The advent of statistical machine learning in the early 2000s marked a pivotal shift toward inductive pattern recognition. "
        "Algorithms were trained on historical labeled datasets to automatically infer non-linear boundary manifolds distinguishing "
        "legitimate transactions from fraudulent exploits. However, as transactional volumes scaled and cybercriminals adopted "
        "distributed, multi-stage attack strategies, conventional shallow models proved insufficient, precipitating the need for "
        "deep neural sequence modeling and hybrid ensemble architectures.",
        styles['Body']
    ))

    story.append(Paragraph("2.2 Traditional Machine Learning in Transaction Fraud", styles['SectionHeader']))
    story.append(Paragraph(
        "Extensive scholarly inquiry has evaluated standard statistical learning techniques for credit card fraud detection. "
        "Early benchmark studies by Bhattacharyya et al. (2011) conducted comprehensive comparative analyses between Logistic "
        "Regression, Support Vector Machines (SVM), and Random Forests on real-world retail banking datasets. Their empirical findings "
        "demonstrated that while Logistic Regression offered computational speed, its linear decision boundary failed to capture "
        "intricate feature interactions—such as the non-linear relationship between transaction amount, account age, and nocturnal timing.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Support Vector Machines (SVM) with Radial Basis Function (RBF) kernels demonstrated superior non-linear classification capabilities, "
        "as highlighted by Sahin et al. (2013). Nevertheless, SVM models exhibited severe scalability bottlenecks: the quadratic time complexity "
        "$O(N^2)$ with respect to dataset size rendered SVM training and real-time inference impractical for streaming e-commerce platforms "
        "processing millions of daily transactions. Furthermore, SVM decision hyperplanes proved highly vulnerable to noise and class imbalance.",
        styles['Body']
    ))

    story.append(Paragraph("2.3 Advanced Gradient Boosting & Tree Ensemble Techniques", styles['SectionHeader']))
    story.append(Paragraph(
        "To achieve both non-linear representational power and computational efficiency, research shifted decisively toward tree-based "
        "ensemble methodologies. Ensemble learning leverages the wisdom of crowds by aggregating multiple weak learners (typically decision "
        "trees) into an accurate, robust predictor. The two primary paradigms are <b>Bagging (Bootstrap Aggregating)</b>, embodied by "
        "Random Forest, and <b>Boosting</b>, embodied by Gradient Boosted Decision Trees (GBDT) and XGBoost.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Chen and Guestrin (2016) introduced XGBoost (eXtreme Gradient Boosting), which revolutionized competitive machine learning and "
        "industrial fraud analytics. XGBoost incorporates second-order Taylor expansion approximations of the loss function alongside "
        "explicit tree complexity regularization terms ($\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum w^2$), effectively preventing "
        "overfitting on noisy tabular fraud datasets. Comprehensive benchmarks by Dal Pozzolo et al. (2015) confirmed that gradient boosting "
        "consistently dominates shallow networks across Area Under the Precision-Recall Curve (AUC-PR) metrics.",
        styles['Body']
    ))

    story.append(Paragraph("2.4 Deep Sequence & Recurrent Neural Network Architectures", styles['SectionHeader']))
    story.append(Paragraph(
        "A critical limitation identified in tree-based models is their inability to capture temporal sequential context. Jurgovsky et al. (2018) "
        "demonstrated that treating transactions as independent events severely degrades detection performance on Account Takeover (ATO) fraud, "
        "wherein an adversary's actions must be evaluated relative to a customer's historical behavioral baseline.",
        styles['Body']
    ))
    story.append(Paragraph(
        "To resolve this limitation, researchers adapted Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) networks to financial "
        "fraud detection. LSTMs maintain internal cell states regulated by input, forget, and output gates, allowing the network to retain "
        "long-term spending profiles while reacting dynamically to sudden deviations in transaction velocity, geographical jump distances, "
        "and merchant category transitions. Studies by Wang et al. (2019) validated that sequential LSTM models increase detection recall "
        "on ATO attacks by over 28% compared to non-sequential baselines.",
        styles['Body']
    ))

    story.append(Paragraph("2.5 Unsupervised Deep Anomaly Detection & Autoencoders", styles['SectionHeader']))
    story.append(Paragraph(
        "Supervised classifiers are inherently constrained by the historical labels present in their training corpora: they excel at "
        "detecting known fraud patterns, but remain vulnerable to zero-day attack vectors and novel money-laundering schemes. To address "
        "this blind spot, unsupervised deep anomaly detection utilizing <b>Autoencoder (AE)</b> neural networks has emerged as a powerful paradigm.",
        styles['Body']
    ))
    story.append(Paragraph(
        "As formalized by Chalapathy and Chawla (2019), an autoencoder is trained exclusively on legitimate, non-fraudulent transaction "
        "sequences to learn a low-dimensional manifold representation (the latent bottleneck). When a transaction sequence is passed through "
        "the trained network, the autoencoder attempts to reconstruct the input. For normal transactions, the reconstruction error "
        "$\|x - \hat{x}\|^2$ is minimal. However, when an anomalous fraud attempt (such as an unprecedented velocity surge) is introduced, "
        "the autoencoder fails to reconstruct the sequence accurately, yielding a high reconstruction loss that flags the transaction as an anomaly.",
        styles['Body']
    ))

    story.append(Paragraph("2.6 Mitigating Severe Class Imbalance (SMOTE & Resampling)", styles['SectionHeader']))
    story.append(Paragraph(
        "A ubiquitous challenge across all financial fraud literature is the extreme skew of class distributions. In authentic banking "
        "datasets, fraud rates rarely exceed 0.5% to 1.0%. Standard loss minimization causes learning algorithms to predict the majority "
        "legitimate class universally, achieving near-perfect nominal accuracy while completely failing to protect the system.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Chawla et al. (2002) pioneered the <b>Synthetic Minority Over-sampling Technique (SMOTE)</b> to decisively overcome this bottleneck. "
        "Instead of duplicating minority instances (which causes severe overfitting), SMOTE synthesizes novel synthetic minority samples "
        "along the line segments joining $k$-nearest minority neighbors in feature space: "
        "$$x_{new} = x_i + \lambda \cdot (x_{zi} - x_i), \quad \lambda \in [0, 1]$$ "
        "Extensive empirical validations by Dal Pozzolo et al. (2015) confirmed that combining SMOTE with calibrated ensemble voting "
        "maximizes true positive detection rates while maintaining stringent control over false alarm penalties.",
        styles['Body']
    ))

    story.append(Paragraph("2.7 Comparative Synthesis Matrix of Existing Literature", styles['SectionHeader']))
    story.append(Paragraph(
        "To summarize the state-of-the-art and contextualize the technical positioning of this dissertation, Table 2.1 presents a "
        "systematic comparative synthesis of foundational research contributions in financial fraud detection:",
        styles['Body']
    ))

    t2_data = [
        [Paragraph("<b>Authors & Year</b>", styles['TableHead']),
         Paragraph("<b>Methodology</b>", styles['TableHead']),
         Paragraph("<b>Primary Strengths</b>", styles['TableHead']),
         Paragraph("<b>Identified Limitations</b>", styles['TableHead'])],
        [Paragraph("Bhattacharyya et al. (2011)", styles['TableCell']),
         Paragraph("Logistic Regression, SVM, Random Forest", styles['TableCell']),
         Paragraph("Rigorous baseline comparison across tabular metrics", styles['TableCell']),
         Paragraph("No temporal modeling; poor handling of severe class skew", styles['TableCell'])],
        [Paragraph("Sahin et al. (2013)", styles['TableCell']),
         Paragraph("Decision Trees & SVM with Cost-Sensitive Loss", styles['TableCell']),
         Paragraph("Incorporates financial cost matrix into loss function", styles['TableCell']),
         Paragraph("High inference latency; does not scale to high-velocity streams", styles['TableCell'])],
        [Paragraph("Dal Pozzolo et al. (2015)", styles['TableCell']),
         Paragraph("Ensemble Classifiers with Undersampling", styles['TableCell']),
         Paragraph("Demonstrates probability calibration across data streams", styles['TableCell']),
         Paragraph("Lacks deep sequence learning; treats events as independent", styles['TableCell'])],
        [Paragraph("Chen & Guestrin (2016)", styles['TableCell']),
         Paragraph("XGBoost (eXtreme Gradient Boosting)", styles['TableCell']),
         Paragraph("State-of-the-art tabular accuracy and fast inference", styles['TableCell']),
         Paragraph("Fails on temporal behavioral sequences and ATO fraud", styles['TableCell'])],
        [Paragraph("Jurgovsky et al. (2018)", styles['TableCell']),
         Paragraph("LSTM Recurrent Networks on Transaction Sequences", styles['TableCell']),
         Paragraph("Captures temporal user spending profile and velocity", styles['TableCell']),
         Paragraph("Computationally expensive; lacks compliance audit mapping", styles['TableCell'])],
        [Paragraph("Wang et al. (2019)", styles['TableCell']),
         Paragraph("Hybrid CNN-LSTM Deep Architecture", styles['TableCell']),
         Paragraph("Combines spatial feature extraction with temporal memory", styles['TableCell']),
         Paragraph("Black-box model; completely uninterpretable to auditors", styles['TableCell'])],
        [Paragraph("<b>Proposed System (2026)</b>", styles['TableCell']),
         Paragraph("<b>Dual-Path Ensemble (XGBoost + LSTM/AE) + Compliance</b>", styles['TableCell']),
         Paragraph("<b>Fuses tabular ML, temporal deep learning, rules, and OWASP/PCI tags</b>", styles['TableCell']),
         Paragraph("Requires sequential state buffer; addressed via sliding windows", styles['TableCell'])]
    ]
    t2 = Table(t2_data, colWidths=[105, 125, 135, 115])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#eff6ff")),
    ]))
    story.append(t2)
    story.append(Paragraph("Table 2.1: Comparative Synthesis of Existing Machine Learning & Deep Learning Fraud Detection Literature", styles['Caption']))

    story.append(Paragraph("2.8 Identified Research Gaps & Proposed Research Novelty", styles['SectionHeader']))
    story.append(Paragraph(
        "A rigorous synthesis of the reviewed literature reveals three critical research and engineering gaps that have remained "
        "largely unaddressed in existing academic literature:",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>1. Architectural Fragmentation between Tabular and Sequential Modeling:</b> Prior studies universally treat supervised "
        "tabular classification and recurrent sequence modeling as competing alternatives. In practice, neither is sufficient on its own: "
        "tabular models miss temporal behavioral drift, while sequence models are overly complex for simple static card-testing exploits. "
        "<i>This dissertation bridges this divide by proposing a concurrent Dual-Path fusion architecture.</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "<b>2. Binary Classification vs. Calibrated Multi-Tier Action Policies:</b> Nearly all published models treat fraud detection "
        "as a binary 0/1 decision. In commercial banking reality, binary decisions create excessive customer friction. "
        "<i>This research introduces a calibrated multi-tier decision engine: auto-approving low-risk transactions, auto-blocking high-risk "
        "threats, and routing ambiguous intermediate cases to step-up Two-Factor Authentication (OTP/2FA).</i>",
        styles['Bullet']
    ))
    story.append(Paragraph(
        "<b>3. Complete Disconnect from Cybersecurity Regulatory Frameworks:</b> Academic literature has completely ignored industry "
        "compliance frameworks. A flagged transaction must be justifiable under regulatory scrutiny. "
        "<i>This dissertation integrates an automated Framework Mapping Engine that correlates every flagged transaction with its "
        "Fraud Lifecycle stage, OWASP API Security Top 10 (2023) vulnerability reference, and PCI DSS v4.0 control requirement.</i>",
        styles['Bullet']
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: THEORETICAL FOUNDATIONS & SECURITY FRAMEWORKS
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 3</b>", styles['ChapterHeader']))
    story.append(Paragraph("<b>THEORETICAL FOUNDATIONS & SECURITY FRAMEWORKS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    story.append(Paragraph("3.1 Mathematical Foundations of Supervised Tree Classifiers", styles['SectionHeader']))
    story.append(Paragraph(
        "Tree-based supervised ensembles constitute the core analytical engine of Path A in our architecture. Random Forest operates "
        "by building $B$ decorrelated decision trees, each trained on a bootstrap sample of the dataset $D$. During tree construction, "
        "at each split candidate node, only a random subset of $m \approx \sqrt{p}$ features is evaluated to maximize diversity among trees. "
        "The final ensemble prediction is calculated via majority vote or average probability: "
        "$$P_{RF}(y=1|x) = \frac{1}{B} \sum_{b=1}^B P_b(y=1|x)$$",
        styles['Body']
    ))
    story.append(Paragraph(
        "Gradient Boosting, in contrast, trains trees sequentially. Each successive tree $f_t(x)$ fits the pseudo-residuals of the previous "
        "ensemble prediction. In XGBoost, the objective function at step $t$ combines a differentiable convex loss function $l$ and an "
        "explicit tree complexity penalty $\Omega$:",
        styles['Body']
    ))
    story.append(Paragraph(
        "$$\mathcal{L}^{(t)} = \sum_{i=1}^n l\left(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)\right) + \Omega(f_t), \quad \text{where } \Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "Using second-order Taylor expansion approximations, the optimal leaf weights $w_j^*$ and split gain are computed analytically, "
        "yielding exceptionally rapid convergence and robust resistance to feature multicollinearity.",
        styles['Body']
    ))

    story.append(Paragraph("3.2 Recurrent Memory Mechanics in Temporal Sequence Modeling", styles['SectionHeader']))
    story.append(Paragraph(
        "Path B leverages Long Short-Term Memory (LSTM) recurrent networks to process temporal transaction vectors. Standard RNNs suffer "
        "from the vanishing gradient problem, wherein backpropagated error gradients exponentially decay over long time horizons. "
        "Hochreiter and Schmidhuber (1997) resolved this by introducing a constant error carousel governed by three non-linear multiplicative gates:",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>1. Forget Gate:</b> Decides what information to discard from the previous cell state $C_{t-1}$:<br/>"
        "$$f_t = \sigma\left(W_f \cdot [h_{t-1}, x_t] + b_f\right)$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "<b>2. Input Gate & Candidate State:</b> Determines what new candidate memory $\tilde{C}_t$ to store in the cell state:<br/>"
        "$$i_t = \sigma\left(W_i \cdot [h_{t-1}, x_t] + b_i\right), \quad \tilde{C}_t = \tanh\left(W_c \cdot [h_{t-1}, x_t] + b_c\right)$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "<b>3. Cell State Update & Output Gate:</b> Computes the new cell state $C_t$ and output hidden state $h_t$:<br/>"
        "$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t, \quad o_t = \sigma\left(W_o \cdot [h_{t-1}, x_t] + b_o\right), \quad h_t = o_t \odot \tanh(C_t)$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "In our fraud detection pipeline, the input vector $x_t \in \mathbb{R}^7$ represents time-series behavioral metrics at time $t$ "
        "(transaction amount delta, velocity, inter-transaction time gap, merchant risk score, location jump). The final hidden vector $h_T$ "
        "encapsulates the account's sequential trajectory, passing into a sigmoid dense layer to output anomaly probability $P_{seq}$.",
        styles['Body']
    ))

    story.append(Paragraph("3.3 Deep Autoencoder Manifold Reconstruction Principles", styles['SectionHeader']))
    story.append(Paragraph(
        "To complement supervised classification with unsupervised novelty detection, our architecture integrates a Deep Autoencoder. "
        "The autoencoder comprises two symmetric sub-networks: an <b>Encoder</b> $g_\phi: \mathcal{X} \rightarrow \mathcal{Z}$ that compresses "
        "input sequence vectors into a low-dimensional bottleneck code $z \in \mathbb{R}^k$ ($k < d$), and a <b>Decoder</b> $f_\theta: \mathcal{Z} \rightarrow \mathcal{X}$ "
        "that reconstructs the original vector $\hat{x} = f_\theta(g_\phi(x))$.",
        styles['Body']
    ))
    story.append(Paragraph(
        "The network parameters are optimized by minimizing the Mean Squared Reconstruction Error (MSE) over normal transactions:<br/>"
        "$$\mathcal{L}_{AE}(\theta, \phi) = \frac{1}{N} \sum_{i=1}^N \|x_i - f_\theta(g_\phi(x_i))\|^2$$",
        styles['Formula']
    ))
    story.append(Paragraph(
        "When an anomalous sequence (e.g., an abrupt burst of 8 transactions in 3 minutes from an unverified IP) is evaluated, the autoencoder's "
        "latent representation fails to reconstruct the out-of-distribution input, resulting in an elevated reconstruction error that directly "
        "drives the sequence anomaly score.",
        styles['Body']
    ))

    story.append(Paragraph("3.4 Synthetic Minority Oversampling (SMOTE) Formulation", styles['SectionHeader']))
    story.append(Paragraph(
        "To prevent supervised model degradation under the 0.8% minority fraud rate, SMOTE is applied exclusively to the training fold. "
        "For each minority class instance $x_i$, its $k$-nearest minority neighbors are computed using Euclidean distance: "
        "$$d(x_i, x_j) = \sqrt{\sum_{m=1}^p (x_{im} - x_{jm})^2}$$ "
        "A neighbor $x_{zi}$ is randomly selected, and a synthetic instance $x_{new}$ is generated along the connecting segment: "
        "$$x_{new} = x_i + \lambda \cdot (x_{zi} - x_i), \quad \lambda \sim U(0, 1)$$ "
        "This expands the decision boundary region around the minority class without introducing exact duplications, decisively boosting "
        "classifier recall on rare fraud categories.",
        styles['Body']
    ))

    story.append(Paragraph("3.5 OWASP API Security Top 10 (2023) Threat Modeling", styles['SectionHeader']))
    story.append(Paragraph(
        "Because modern payment fraud executes over programmatic REST and GraphQL endpoints, our system maps every classified exploit "
        "to the global standard for API security published by the Open Worldwide Application Security Project (OWASP):",
        styles['Body']
    ))

    t3_data = [
        [Paragraph("<b>OWASP API (2023) Category</b>", styles['TableHead']),
         Paragraph("<b>Vulnerability Description</b>", styles['TableHead']),
         Paragraph("<b>Targeted Fraud Exploit</b>", styles['TableHead']),
         Paragraph("<b>System Defense Mechanism</b>", styles['TableHead'])],
        [Paragraph("<b>API2:2023<br/>Broken Authentication</b>", styles['TableCell']),
         Paragraph("Compromised tokens, credential stuffing, missing 2FA", styles['TableCell']),
         Paragraph("Account Takeover (ATO) & unauthorized fund drain", styles['TableCell']),
         Paragraph("LSTM sequence tracking & dynamic Step-Up 2FA challenge", styles['TableCell'])],
        [Paragraph("<b>API3:2023<br/>Broken Object Property Authorization</b>", styles['TableCell']),
         Paragraph("Unauthorized manipulation of account property fields", styles['TableCell']),
         Paragraph("Synthetic Identity & forged Aadhaar/PAN linking", styles['TableCell']),
         Paragraph("Account age & identity consistency supervised scoring", styles['TableCell'])],
        [Paragraph("<b>API4:2023<br/>Unrestricted Resource Consumption</b>", styles['TableCell']),
         Paragraph("Missing rate limits, unbounded execution loops", styles['TableCell']),
         Paragraph("Transaction Velocity bursts & Card-Not-Present probing", styles['TableCell']),
         Paragraph("Hard velocity caps (>5 txns/5m) & autoencoder anomaly alerts", styles['TableCell'])],
        [Paragraph("<b>API9:2023<br/>Improper Inventory Management</b>", styles['TableCell']),
         Paragraph("Unmonitored endpoints, audit log tracking gaps", styles['TableCell']),
         Paragraph("Chargeback (Friendly) fraud & disputed digital purchases", styles['TableCell']),
         Paragraph("Normalized NDJSON event logging with ISO-8601 audit stamps", styles['TableCell'])]
    ]
    t3 = Table(t3_data, colWidths=[110, 120, 120, 130])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t3)
    story.append(Paragraph("Table 3.1: OWASP API Security Top 10 (2023) Threat Modeling & Fraud Detection Defenses", styles['Caption']))

    story.append(Paragraph("3.6 PCI DSS v4.0 Regulatory Security Controls", styles['SectionHeader']))
    story.append(Paragraph(
        "Compliance with the Payment Card Industry Data Security Standard (PCI DSS) v4.0 is mandatory for all financial entities "
        "storing, processing, or transmitting cardholder data. Our framework maps fraud incidents directly to PCI DSS regulatory requirements:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>PCI DSS Requirement 3 & 4 (Protect Stored Cardholder Data & Encrypt in Transit):</b> Enforced during Card-Not-Present (CNP) validation. PAN data is masked, and CVV codes are strictly excluded from persistent disk storage.", styles['Bullet']))
    story.append(Paragraph("• <b>PCI DSS Requirement 8 (Identify Users and Authenticate Access):</b> Enforced during Account Takeover (ATO) defense. Suspicious logins mandate multi-factor authentication (MFA/2FA) verification.", styles['Bullet']))
    story.append(Paragraph("• <b>PCI DSS Requirement 10 (Log and Monitor All Access to Network Resources & Cardholder Data):</b> Enforced via our ELK Stack logger. Every evaluation event writes an immutable, timestamped NDJSON record capturing transaction ID, risk score, triggered rules, and decision outcome.", styles['Bullet']))
    story.append(Paragraph("• <b>PCI DSS Requirement 12 (Support Information Security with Organizational Policies):</b> Enforced during Synthetic Identity detection to verify Know-Your-Customer (KYC) identity compliance.", styles['Bullet']))

    story.append(Paragraph("3.7 End-to-End Cyber Fraud Lifecycle Taxonomy", styles['SectionHeader']))
    story.append(Paragraph(
        "To provide holistic defense-in-depth, our system models financial attacks across the standard 5-stage Fraud Lifecycle: "
        "<b>1. Account Creation</b> (Synthetic Identity registration) $\\rightarrow$ "
        "<b>2. Testing / Probing</b> (Velocity bursts with micro-charges) $\\rightarrow$ "
        "<b>3. Account Compromise</b> (Account Takeover via stolen credentials) $\\rightarrow$ "
        "<b>4. Monetization</b> (High-value CNP fraud or offshore crypto transfer) $\\rightarrow$ "
        "<b>5. Post-Transaction Dispute</b> (Chargeback and dispute filing). Every transaction processed by our engine is explicitly "
        "tagged with its corresponding lifecycle stage to guide analyst investigations.",
        styles['Body']
    ))
    story.append(PageBreak())

    return story

print("report_chapters_1_to_3.py created successfully.")
