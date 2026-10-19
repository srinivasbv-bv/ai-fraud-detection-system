import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

# Brand Colors
COLOR_NAVY_DARK  = hex_to_rgb('#0B1329') # Title & Closing BG
COLOR_NAVY_BAR   = hex_to_rgb('#0F172A') # Top Header
COLOR_BLUE_ACCENT= hex_to_rgb('#2563EB') # Highlight
COLOR_CYAN_ACCENT= hex_to_rgb('#06B6D4') # Accent border
COLOR_CARD_BG    = hex_to_rgb('#FFFFFF') # Card White
COLOR_PAGE_BG    = hex_to_rgb('#F8FAFC') # Content Slide BG
COLOR_TEXT_MAIN  = hex_to_rgb('#1E293B') # Body Text
COLOR_TEXT_MUTED = hex_to_rgb('#64748B') # Subtext
COLOR_GREEN      = hex_to_rgb('#059669') # Metric/Success
COLOR_RED        = hex_to_rgb('#DC2626') # Alert/Fraud
COLOR_AMBER      = hex_to_rgb('#D97706') # Step-Up/Warning
COLOR_BORDER     = hex_to_rgb('#CBD5E1') # Card Border

def create_deck(filename="AI_Fraud_Detection_System_Project_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="M.Sc. Computer Science Project Review"):
        # Header banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = COLOR_NAVY_BAR
        header_shape.line.fill.background()

        # Accent line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.08), prs.slide_width, Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BLUE_ACCENT
        line.line.fill.background()

        # Header Text Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = category.upper()
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN_ACCENT

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(20)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 255, 255)

        # Footer
        ft_tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.15), Inches(11.7), Inches(0.3))
        ft_tf = ft_tb.text_frame
        ft_tf.margin_top = ft_tf.margin_bottom = ft_tf.margin_left = ft_tf.margin_right = 0
        p_ft = ft_tf.paragraphs[0]
        p_ft.text = "Department of Studies in Computer Science | Karnataka State Open University (KSOU), Mysuru"
        p_ft.font.name = "Segoe UI"
        p_ft.font.size = Pt(8.5)
        p_ft.font.color.rgb = COLOR_TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_bg(slide1, COLOR_NAVY_DARK)

    # Accent decorative bar
    dec_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.12), Inches(4.5))
    dec_bar.fill.solid()
    dec_bar.fill.fore_color.rgb = COLOR_BLUE_ACCENT
    dec_bar.line.fill.background()

    # Title Box
    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.2))
    ttf = tbox.text_frame
    ttf.word_wrap = True
    
    tp1 = ttf.paragraphs[0]
    tp1.text = "M.Sc. COMPUTER SCIENCE — FINAL PROJECT REVIEW & VIVA DEFENSE"
    tp1.font.name = "Segoe UI"
    tp1.font.size = Pt(12)
    tp1.font.bold = True
    tp1.font.color.rgb = COLOR_CYAN_ACCENT

    tp2 = ttf.add_paragraph()
    tp2.text = "AI-Powered Real-Time Fraud Detection System\nfor Indian Banking Transactions"
    tp2.font.name = "Segoe UI"
    tp2.font.size = Pt(28)
    tp2.font.bold = True
    tp2.font.color.rgb = RGBColor(255, 255, 255)
    tp2.space_before = Pt(8)

    tp3 = ttf.add_paragraph()
    tp3.text = "A Hybrid Multi-Tier Framework Combining Gradient Boosting, Bi-directional LSTM & Heuristics with Sub-25ms Inference"
    tp3.font.name = "Segoe UI"
    tp3.font.size = Pt(12)
    tp3.font.color.rgb = hex_to_rgb('#94A3B8')
    tp3.space_before = Pt(6)

    # Metadata Card
    meta_box = add_card(slide1, Inches(1.2), Inches(3.8), Inches(11.0), Inches(2.3), bg_color=hex_to_rgb('#131F3B'), border_color=hex_to_rgb('#203058'))
    m_tb = slide1.shapes.add_textbox(Inches(1.5), Inches(4.0), Inches(10.4), Inches(1.9))
    mtf = m_tb.text_frame
    mtf.word_wrap = True

    p = mtf.paragraphs[0]
    p.text = "PROJECT METADATA & INSTITUTIONAL AFFILIATION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN_ACCENT

    p = mtf.add_paragraph()
    p.text = "• Candidate: [CANDIDATE NAME]   |   Register Number: [REGISTER NUMBER]"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_before = Pt(6)

    p = mtf.add_paragraph()
    p.text = "• Project Guide: Smt. Suneetha, Associate Professor, Department of Studies in Computer Science"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.space_before = Pt(4)

    p = mtf.add_paragraph()
    p.text = "• Institution: Karnataka State Open University (KSOU), Mukthagangothri, Mysuru - 570006"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = hex_to_rgb('#CBD5E1')
    p.space_before = Pt(4)

    p = mtf.add_paragraph()
    p.text = "• Deployment: Live at https://ai-fraud-detection-system-five.vercel.app  |  Academic Year 2025–2026"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CYAN_ACCENT
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & CORE HIGHLIGHTS
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_bg(slide2, COLOR_PAGE_BG)
    add_header(slide2, "Executive Summary & Core Project Highlights")

    cards_data = [
        ("13.0+ Billion", "Monthly UPI Transactions", "Explosive growth in Indian digital payments requires sub-second fraud protection across UPI, IMPS, RTGS, and RuPay.", COLOR_BLUE_ACCENT),
        ("18 – 25 ms", "Real-Time Inference Latency", "Engineered to comfortably operate within the NPCI / RBI 50ms gateway switch SLA on commodity CPU hardware.", COLOR_GREEN),
        ("0.978", "ROC-AUC Benchmark", "Hybrid ensemble outperforms standalone models (0.87–0.92) with 94.2% precision and 91.5% recall under extreme imbalance.", COLOR_BLUE_ACCENT),
        ("3-Tier Policy", "Adaptive Friction Decisioning", "Replaces blunt allow/block with Auto-Approve (<30), Step-Up OTP 2FA (30–70), and Outright Block (>70).", COLOR_AMBER)
    ]

    for i, (stat, title, desc, clr) in enumerate(cards_data):
        c_left = Inches(0.8 + i * 2.98)
        add_card(slide2, c_left, Inches(1.4), Inches(2.8), Inches(2.2))
        tb = slide2.shapes.add_textbox(c_left + Inches(0.15), Inches(1.5), Inches(2.5), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = stat
        p.font.name = "Segoe UI"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = clr

        p = tf.add_paragraph()
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(6)

    # Bottom summary box
    add_card(slide2, Inches(0.8), Inches(3.85), Inches(11.73), Inches(3.0))
    tb_bot = slide2.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.33), Inches(2.7))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True

    p = tf_bot.paragraphs[0]
    p.text = "RESEARCH & TECHNICAL VALUE PROPOSITION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    bullets = [
        "<b>Multi-Modal Ensemble Synergy:</b> Unifies static feature tabular classification (LightGBM/GBDT), deep sequential context analysis (Bi-directional LSTM), and zero-latency heuristic business rules.",
        "<b>Indian Domestic Rail Grounding:</b> Modeled in Indian Rupees (₹), addressing micro-ticket Kirana QR payments, large-ticket RTGS business transfers, and geographic travel velocity constraints between Indian cities.",
        "<b>Explainable AI (XAI) & Human-in-the-Loop (HITL):</b> Provides fraud analysts with transparent feature-attribution risk breakdowns and operational triage tools rather than an uninterpretable black-box.",
        "<b>Regulatory & Framework Compliance:</b> Directly grounded in RBI Digital Payment Security Guidelines (2021), OWASP API Security Top 10, and PCI-DSS v4.0 audit logging standards."
    ]
    for b in bullets:
        p = tf_bot.add_paragraph()
        p.text = "• " + b.replace("<b>", "").replace("</b>", "")
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & DOMAIN MOTIVATION
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_bg(slide3, COLOR_PAGE_BG)
    add_header(slide3, "Problem Statement & Indian Financial Domain Motivation")

    # Left Card: Traditional Rule-Based Flaws
    add_card(slide3, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
    tb_l = slide3.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(5.1))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "LIMITATIONS OF LEGACY FRAUD SYSTEMS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    points_l = [
        ("Static Hardcoded Thresholds:", "Traditional systems flag transactions purely by static amounts (e.g. > ₹50,000). Attackers easily bypass this through 'smurfing' or micro-probing (series of ₹2,000 payments)."),
        ("Over 80% False Positive Ratio:", "Legitimate users making genuine festival purchases, travel bookings, or emergency hospital bills get falsely blocked, causing severe customer frustration and churn."),
        ("Absence of Temporal Awareness:", "Treating transactions as independent isolated events misses temporal account takeovers (e.g., password change followed immediately by 5 rapid transfers)."),
        ("Maintenance & Rule Explosion:", "Rule engines grow to thousands of conflicting if-else statements that degrade switch processing throughput.")
    ]
    for title, desc in points_l:
        p = tf_l.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # Right Card: The Indian Payment Landscape
    add_card(slide3, Inches(6.8), Inches(1.4), Inches(5.73), Inches(5.5))
    tb_r = slide3.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.1))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "THE MODERN INDIAN PAYMENT THREAT LANDSCAPE"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    points_r = [
        ("UPI QR Code Phishing & Reverse Requests:", "Fraudsters send collect requests masked as cashback receipts or spoof legitimate merchant soundboxes."),
        ("Automated Bot Velocity Bursts:", "Credential stuffing and card testing attacks executing 8–10 transactions within 60 seconds across online e-commerce checkouts."),
        ("Extreme Geo-Location Impossibility:", "Transactions occurring across geographically distant Indian cities (e.g., Bengaluru physical ATM followed 20 minutes later by a Delhi POS tap)."),
        ("High-Risk Nighttime Account Takeovers (ATO):", "SIM swapping or malware-enabled credential theft occurring during odd hours (1 AM to 4 AM) accompanied by rapid balance liquidation.")
    ]
    for title, desc in points_r:
        p = tf_r.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: PROJECT OBJECTIVES & SCOPE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_bg(slide4, COLOR_PAGE_BG)
    add_header(slide4, "Project Objectives & Technical Scope")

    objectives = [
        ("1. Multi-Tier Hybrid Modeling", "Build an ensemble architecture harmonizing supervised tree-based classification (LightGBM/GBDT), deep sequence learning (Bi-directional LSTM), and heuristic business logic to capture both static and sequential fraud dynamics."),
        ("2. Sub-25ms Real-Time Inference SLA", "Optimize feature transformations, numeric standardizations, and model inference pipelines to evaluate transactions in <25ms, complying with NPCI and RBI payment switch processing limits."),
        ("3. Adaptive 3-Tier Risk Policy", "Replace binary allow/block decisions with an adaptive risk-based friction model: Auto-Approve (score <30), Step-Up OTP/Biometric 2FA (score 30–70), and Outright Block (score >70)."),
        ("4. Explainable AI & Human Triage Queue", "Provide fraud analysts with localized feature importance breakdowns explaining *why* a transaction was flagged, coupled with a Level-2 triage investigation queue for dispute resolution."),
        ("5. Enterprise & Regulatory Alignment", "Ground system telemetry and auditing in RBI Digital Payment Security Guidelines (2021), OWASP API Security Top 10, and PCI-DSS v4.0 non-repudiation mandates.")
    ]

    for i, (title, desc) in enumerate(objectives):
        top_pos = Inches(1.4 + i * 1.08)
        add_card(slide4, Inches(0.8), top_pos, Inches(11.73), Inches(0.96))
        tb = slide4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.33), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_ACCENT

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: LITERATURE SURVEY & RESEARCH GAPS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_bg(slide5, COLOR_PAGE_BG)
    add_header(slide5, "Literature Survey & Research Gaps Analysis")

    rows = [
        ("Approach / Methodology", "Core Advantages", "Critical Deficiencies / Gaps", "Our Proposed Solution"),
        ("Rule-Based Systems (Heuristic IF-THEN)", "Fast, zero latency, highly interpretable by non-technical staff.", "High false positives (>80%), brittle, fails on unseen patterns.", "Retained as a 20% deterministic guardrail for extreme blacklists & caps."),
        ("Classical Supervised ML (Logistic, Random Forest)", "Learns non-linear boundaries, adapts to labeled fraud patterns.", "Treats transactions as isolated points, ignores temporal velocity.", "Gradient Boosted Trees (LightGBM) optimized with scale_pos_weight for static features."),
        ("Unsupervised Anomaly (Isolation Forest, Autoencoder)", "Detects zero-day anomalies without needing historical labels.", "High false alarm rate on genuine seasonal bursts or paydays.", "Integrated into anomaly scoring to catch zero-day deviations."),
        ("Deep Sequence Models (Vanilla RNN, LSTM)", "Captures sequential dependencies across historical transaction events.", "High computational cost, slower inference latency if unoptimized.", "Bi-directional LSTM with bounded sliding window (N=10) executing in <10ms."),
        ("Our Proposed Hybrid Framework", "Synergistic ensemble balancing precision, recall, and zero-day capture.", "Requires careful calibration of component risk weights.", "Dynamic re-weighting with 3-tier adaptive friction policy & sub-25ms latency.")
    ]

    table_shape = slide5.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.4))
    table = table_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(3.1)
    table.columns[3].width = Inches(3.03)

    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_value in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Segoe UI"
            if r_idx == 0:
                p.font.size = Pt(10)
                p.font.bold = True
                p.font.color.rgb = RGBColor(255, 255, 255)
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_BAR
            elif r_idx == len(rows) - 1:
                p.font.size = Pt(9)
                p.font.bold = True
                p.font.color.rgb = COLOR_BLUE_ACCENT
                cell.fill.solid()
                cell.fill.fore_color.rgb = hex_to_rgb('#EFF6FF')
            else:
                p.font.size = Pt(8.5)
                p.font.color.rgb = COLOR_TEXT_MAIN
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else hex_to_rgb('#F8FAFC')

    # =========================================================================
    # SLIDE 6: PROPOSED SYSTEM ARCHITECTURE (WITH DIAGRAM)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_bg(slide6, COLOR_PAGE_BG)
    add_header(slide6, "Proposed System Architecture & End-to-End Pipeline")

    arch_fig = os.path.join("assets", "report_figures", "fig1_system_architecture.png")
    if os.path.exists(arch_fig):
        slide6.shapes.add_picture(arch_fig, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.4))
    else:
        add_card(slide6, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.4))

    # Right Explanation Card
    add_card(slide6, Inches(8.2), Inches(1.4), Inches(4.33), Inches(5.4))
    tb_arch = slide6.shapes.add_textbox(Inches(8.4), Inches(1.55), Inches(3.93), Inches(5.1))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    p.text = "THREE-TIER MODULAR PIPELINE"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    arch_bullets = [
        ("1. Ingestion Layer:", "Consumes live payment requests across UPI QR, IMPS, RTGS, and RuPay card checkouts formatted as JSON payloads."),
        ("2. Feature Vectorization:", "Transforms raw transaction inputs into a 23-dimensional static feature vector and a 7-dimensional temporal sequence tensor."),
        ("3. Model Inference Engine:", "Parallel evaluation across GBDT, Bi-directional LSTM, and Business Rule Overlay."),
        ("4. Decision Matrix:", "Outputs unified Risk Score [0–100] mapping to Auto-Approve, Step-Up 2FA, or Block."),
        ("5. Analyst & Audit Loop:", "Stores forensic events in ELK/SIEM JSON format and provides interactive triage.")
    ]
    for b_title, b_desc in arch_bullets:
        p = tf_arch.add_paragraph()
        p.text = f"• {b_title} {b_desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: MATHEMATICAL & ALGORITHMIC FOUNDATIONS
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_bg(slide7, COLOR_PAGE_BG)
    add_header(slide7, "Mathematical Modeling & Algorithmic Formulations")

    # Left: LSTM Equations & Diagram
    add_card(slide7, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
    tb_m1 = slide7.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(2.2))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True

    p = tf_m1.paragraphs[0]
    p.text = "1. BI-DIRECTIONAL LSTM GATING EQUATIONS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    eqs = [
        "• Forget Gate:  f_t = σ(W_f · [h_{t-1}, x_t] + b_f)",
        "• Input Gate:   i_t = σ(W_i · [h_{t-1}, x_t] + b_i)",
        "• Candidate:    C~_t = tanh(W_c · [h_{t-1}, x_t] + b_c)",
        "• Cell State:   C_t = f_t * C_{t-1} + i_t * C~_t",
        "• Output Gate:  o_t = σ(W_o · [h_{t-1}, x_t] + b_o)",
        "• Hidden State: h_t = o_t * tanh(C_t)"
    ]
    for eq in eqs:
        p = tf_m1.add_paragraph()
        p.text = eq
        p.font.name = "Consolas"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(2)

    lstm_fig = os.path.join("assets", "report_figures", "fig6_lstm_cell.png")
    if os.path.exists(lstm_fig):
        slide7.shapes.add_picture(lstm_fig, Inches(1.0), Inches(4.0), Inches(5.3), Inches(2.7))

    # Right: Ensemble Scoring & Rules
    add_card(slide7, Inches(6.8), Inches(1.4), Inches(5.73), Inches(5.5))
    tb_m2 = slide7.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.1))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True

    p = tf_m2.paragraphs[0]
    p.text = "2. HYBRID ENSEMBLE RISK SCORE FORMULA"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    m2_content = [
        ("Ensemble Risk Formulation:", "Risk Score = 100 × ( w₁·P_supervised + w₂·P_sequence + w₃·R_rules )\nwhere w₁=0.45, w₂=0.35, w₃=0.20 (Default Baseline)."),
        ("Dynamic Re-Weighting Policy:", "If a high-severity business rule triggers (e.g. Blacklisted IP/Card or Velocity Burst >5 txns in 5 mins with r_rules ≥ 0.8), weights dynamically adjust to:\nw₁=0.30, w₂=0.30, w₃=0.40 (ensuring rule dominance)."),
        ("Haversine Geographic Velocity Metric:", "d = 2R · arcsin( sqrt( sin²(Δφ/2) + cos φ₁·cos φ₂·sin²(Δλ/2) ) )\nVelocity v = d / Δt. If v > 800 km/h between successive transactions, a severe geographic anomaly flag triggers."),
        ("Reconstruction Loss (Autoencoder):", "MSE = (1/d) · Σ (x_j - x^_j)². High reconstruction error isolates zero-day transaction anomalies that deviate from typical user spending clusters.")
    ]
    for m_title, m_desc in m2_content:
        p = tf_m2.add_paragraph()
        p.text = f"• {m_title}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

        p = tf_m2.add_paragraph()
        p.text = m_desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(1)

    # =========================================================================
    # SLIDE 8: DATASET ENGINEERING & INDIAN PAYMENT CONTEXT
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_bg(slide8, COLOR_PAGE_BG)
    add_header(slide8, "Dataset Engineering & Indian Banking Rails Calibration")

    data_cards = [
        ("Indian Payment Rails Modeled", [
            "<b>Unified Payments Interface (UPI):</b> P2P transfer, P2M QR-code payments, dynamic collect requests.",
            "<b>Immediate Payment Service (IMPS):</b> 24x7 instant interbank transfers with account/IFSC verification.",
            "<b>RTGS & NEFT:</b> High-value corporate settlements (RTGS > ₹2 Lakhs) and batch retail transfers.",
            "<b>RuPay & Domestic Cards:</b> E-commerce gateway checkouts, POS terminal dips, and contactless NFC taps."
        ]),
        ("Synthetic Data Engine & Statistical Grounding", [
            "<b>DPDP Act 2023 Compliance:</b> Synthetic generator used to comply with RBI/DPDP customer privacy mandates.",
            "<b>Benford's Law Validation:</b> Natural currency amounts adhere to logarithmic first-digit distributions.",
            "<b>Indian Geographic Distance Matrix:</b> Calibrated real latitude/longitude travel times between Indian cities.",
            "<b>Merchant Category Codes (MCC):</b> Modeled local categories: upi_kirana_retail, irctc_railways, fuel_station, crypto_gaming."
        ])
    ]

    for i, (title, items) in enumerate(data_cards):
        c_left = Inches(0.8 + i * 5.95)
        add_card(slide8, c_left, Inches(1.4), Inches(5.75), Inches(5.5))
        tb = slide8.shapes.add_textbox(c_left + Inches(0.2), Inches(1.55), Inches(5.35), Inches(5.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.name = "Segoe UI"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_ACCENT

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item.replace("<b>", "").replace("</b>", "")
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 9: TRANSACTION LIFECYCLE & EXECUTION FLOW (DIAGRAM)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_bg(slide9, COLOR_PAGE_BG)
    add_header(slide9, "Real-Time Transaction Lifecycle & Sequence Flow")

    flow_fig = os.path.join("assets", "report_figures", "fig2_transaction_flowchart.png")
    if os.path.exists(flow_fig):
        slide9.shapes.add_picture(flow_fig, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))
    else:
        add_card(slide9, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    seq_fig = os.path.join("assets", "report_figures", "fig3_sequence_diagram.png")
    if os.path.exists(seq_fig):
        slide9.shapes.add_picture(seq_fig, Inches(7.0), Inches(1.4), Inches(5.53), Inches(5.4))
    else:
        add_card(slide9, Inches(7.0), Inches(1.4), Inches(5.53), Inches(5.4))

    # =========================================================================
    # SLIDE 10: REAL-TIME DECISIONING POLICY & RISK TIERS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_bg(slide10, COLOR_PAGE_BG)
    add_header(slide10, "Adaptive Three-Tier Risk Decisioning Policy")

    tiers = [
        ("TIER 1: AUTO-APPROVE", "Risk Score: 0 – 29.99", COLOR_GREEN, [
            "Frictionless instant transaction clearance.",
            "Normal spending amount matching customer history.",
            "Low device risk score (<0.30) and known IP geolocation.",
            "Inference and response emitted in <18 milliseconds.",
            "Represents ~92% of authentic daily consumer traffic."
        ]),
        ("TIER 2: STEP-UP 2FA", "Risk Score: 30.00 – 69.99", COLOR_AMBER, [
            "Dynamic friction challenge rather than outright block.",
            "Mandates instant OTP or mobile biometric fingerprint.",
            "Prevents customer cart abandonment on edge cases.",
            "Triggered by new merchant categories or moderate velocity.",
            "Complies with RBI Adaptive Risk Authentication Guidelines."
        ]),
        ("TIER 3: OUTRIGHT BLOCK", "Risk Score: 70.00 – 100.0", COLOR_RED, [
            "Immediate transaction rejection at payment gateway switch.",
            "Escalated instantly to the Level-2 Analyst Review Queue.",
            "Triggered by blacklists, velocity bursts, or extreme geo-jumps.",
            "Generates immutable SIEM audit event with forensic metadata.",
            "Stops balance liquidation and protects bank capital."
        ])
    ]

    for i, (t_title, t_sub, t_clr, t_bullets) in enumerate(tiers):
        t_left = Inches(0.8 + i * 3.98)
        add_card(slide10, t_left, Inches(1.4), Inches(3.78), Inches(5.5))
        
        # Header block inside card
        card_hdr = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, t_left, Inches(1.4), Inches(3.78), Inches(1.0))
        card_hdr.fill.solid()
        card_hdr.fill.fore_color.rgb = t_clr
        card_hdr.line.fill.background()

        tb_h = slide10.shapes.add_textbox(t_left + Inches(0.15), Inches(1.45), Inches(3.48), Inches(0.9))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = t_title
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        p = tf_h.add_paragraph()
        p.text = t_sub
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)

        tb_b = slide10.shapes.add_textbox(t_left + Inches(0.15), Inches(2.55), Inches(3.48), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for b_idx, b_item in enumerate(t_bullets):
            p = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p.text = f"• {b_item}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: SYSTEM IMPLEMENTATION & TECHNOLOGY STACK
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_bg(slide11, COLOR_PAGE_BG)
    add_header(slide11, "Software Architecture & Enterprise Technology Stack")

    tech_stack = [
        ("Backend & Inference Core", "Python 3.11+, Flask / FastAPI Microframework", "Lightweight, sub-millisecond serialization, native PyTorch/Scikit-learn integration, RESTful endpoints."),
        ("Machine Learning Engine", "PyTorch, LightGBM, Scikit-learn, Joblib", "Bi-directional LSTM sequence model, gradient boosted decision trees, minmax scalers, one-hot encoders."),
        ("Presentation & Visualization", "HTML5, Tailwind CSS, Chart.js, Vanilla JS", "Real-time responsive dashboard, dynamic risk gauges, asynchronous polling without framework bloat."),
        ("Logging, SIEM & Auditing", "Structured JSON Logger, ELK Stack Schema", "Immutable non-repudiation logging of all risk scores, features, and analyst interventions for compliance."),
        ("Cloud Deployment & Hosting", "Vercel Serverless Edge Platform, Git CI/CD", "Global edge routing, automated continuous deployment, serverless scaling, production SSL/TLS encryption.")
    ]

    for i, (layer, tech, detail) in enumerate(tech_stack):
        top_pos = Inches(1.4 + i * 1.08)
        add_card(slide11, Inches(0.8), top_pos, Inches(11.73), Inches(0.96))
        tb = slide11.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.33), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{layer.upper()}  —  "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_ACCENT

        # add tech name in bold dark
        p.text += tech

        p = tf.add_paragraph()
        p.text = detail
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 12: EXPERIMENTAL EVALUATION & RESULTS BENCHMARK
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_bg(slide12, COLOR_PAGE_BG)
    add_header(slide12, "Empirical Experimental Results & Performance Benchmarks")

    metric_rows = [
        ("Model / System Architecture", "Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC", "Inference Latency"),
        ("Baseline Business Rules Only", "0.621", "0.584", "0.602", "0.680", "0.540", "< 2 ms"),
        ("Isolation Forest (Unsupervised)", "0.785", "0.712", "0.747", "0.825", "0.730", "8.2 ms"),
        ("Bi-directional LSTM (Sequence)", "0.894", "0.842", "0.867", "0.931", "0.884", "11.5 ms"),
        ("Supervised LightGBM / GBDT", "0.931", "0.889", "0.909", "0.965", "0.932", "5.4 ms"),
        ("Proposed Hybrid Ensemble (Our System)", "0.942", "0.915", "0.928", "0.978", "0.951", "18.6 ms")
    ]

    t_shape12 = slide12.shapes.add_table(len(metric_rows), 7, Inches(0.8), Inches(1.4), Inches(11.73), Inches(3.6))
    tbl12 = t_shape12.table
    tbl12.columns[0].width = Inches(3.2)
    tbl12.columns[1].width = Inches(1.4)
    tbl12.columns[2].width = Inches(1.4)
    tbl12.columns[3].width = Inches(1.4)
    tbl12.columns[4].width = Inches(1.4)
    tbl12.columns[5].width = Inches(1.4)
    tbl12.columns[6].width = Inches(1.53)

    for r_idx, row in enumerate(metric_rows):
        for c_idx, val in enumerate(row):
            c = tbl12.cell(r_idx, c_idx)
            c.text = val
            p = c.text_frame.paragraphs[0]
            p.font.name = "Segoe UI"
            if r_idx == 0:
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = RGBColor(255, 255, 255)
                c.fill.solid()
                c.fill.fore_color.rgb = COLOR_NAVY_BAR
            elif r_idx == len(metric_rows) - 1:
                p.font.size = Pt(9)
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN
                c.fill.solid()
                c.fill.fore_color.rgb = hex_to_rgb('#ECFDF5')
            else:
                p.font.size = Pt(8.5)
                p.font.color.rgb = COLOR_TEXT_MAIN
                c.fill.solid()
                c.fill.fore_color.rgb = COLOR_CARD_BG if r_idx % 2 == 1 else hex_to_rgb('#F8FAFC')

    # Bottom Takeaway Card
    add_card(slide12, Inches(0.8), Inches(5.2), Inches(11.73), Inches(1.7))
    tb_t = slide12.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.33), Inches(1.5))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "KEY EMPIRICAL TAKEAWAYS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    takeaways = [
        "<b>Superior Imbalance Handling:</b> PR-AUC jumps from 0.540 (baseline) to 0.951 in our hybrid system, ensuring minimal false alarms under extreme 0.1% fraud prevalence.",
        "<b>Balanced Precision & Recall:</b> Reaches 94.2% precision (protecting legitimate customer payments) and 91.5% recall (intercepting actual financial losses).",
        "<b>Strict Real-Time Performance:</b> Complete ensemble inference pipeline executes in 18.6 ms, well inside the NPCI 50ms switch constraint."
    ]
    for tk in takeaways:
        p = tf_t.add_paragraph()
        p.text = "• " + tk.replace("<b>", "").replace("</b>", "")
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 13: VISUAL RESULTS: ROC, PR & CONFUSION MATRIX (FIGURES)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_bg(slide13, COLOR_PAGE_BG)
    add_header(slide13, "Visual Evaluation: ROC, Precision-Recall & Confusion Matrix")

    pr_fig = os.path.join("assets", "report_figures", "fig8_pr_roc_curves.png")
    if os.path.exists(pr_fig):
        slide13.shapes.add_picture(pr_fig, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.4))
    else:
        add_card(slide13, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.4))

    cm_fig = os.path.join("assets", "report_figures", "fig9_confusion_matrix.png")
    if os.path.exists(cm_fig):
        slide13.shapes.add_picture(cm_fig, Inches(6.8), Inches(1.4), Inches(5.73), Inches(5.4))
    else:
        add_card(slide13, Inches(6.8), Inches(1.4), Inches(5.73), Inches(5.4))

    # =========================================================================
    # SLIDE 14: RISK SCORE DISTRIBUTION & ANOMALY SEPARATION (FIGURE)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_bg(slide14, COLOR_PAGE_BG)
    add_header(slide14, "Risk Score Separation & Telemetry Distribution Analysis")

    risk_fig = os.path.join("assets", "report_figures", "fig10_risk_distribution.png")
    if os.path.exists(risk_fig):
        slide14.shapes.add_picture(risk_fig, Inches(0.8), Inches(1.4), Inches(6.5), Inches(5.4))
    else:
        add_card(slide14, Inches(0.8), Inches(1.4), Inches(6.5), Inches(5.4))

    # Right Card: Distribution Insights
    add_card(slide14, Inches(7.6), Inches(1.4), Inches(4.93), Inches(5.4))
    tb_rd = slide14.shapes.add_textbox(Inches(7.8), Inches(1.55), Inches(4.53), Inches(5.1))
    tf_rd = tb_rd.text_frame
    tf_rd.word_wrap = True

    p = tf_rd.paragraphs[0]
    p.text = "STATISTICAL SEPARATION ANALYSIS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    r_insights = [
        ("Bimodal Distribution Separation:", "Legitimate transactions cluster sharply between 0 and 25, while fraudulent transactions cluster cleanly above 75. This wide margin of separation minimizes edge-case ambiguity."),
        ("Controlled Step-Up Zone (30–70):", "Only 4.8% of transactions fall into the intermediate Step-Up zone, ensuring that genuine customers are not inundated with unnecessary OTP challenges."),
        ("Rapid Convergence Under Adversarial Bursts:", "When an attacker initiates a burst of transactions within 60 seconds, the score escalates from Tier 1 to Tier 3 within 2 transactions, stopping catastrophic drains."),
        ("Audit Integrity:", "All scored events produce an immutable JSON telemetry record capturing model probabilities and triggered rule strings.")
    ]
    for r_t, r_d in r_insights:
        p = tf_rd.add_paragraph()
        p.text = f"• {r_t} {r_d}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 15: LIVE SYSTEM DEMONSTRATION & USER INTERFACES
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_bg(slide15, COLOR_PAGE_BG)
    add_header(slide15, "Live System Walkthrough & Interactive User Interfaces")

    features = [
        ("1. Central Operations Command Center (/)", "Real-time incoming transaction stream with live KPI counters (Total Processed, Approval Rate, Step-Up 2FA Rate, Blocked Count, Avg Risk Score) and dynamic fraud category distribution charts."),
        ("2. Interactive Real-Time Transaction Simulator (/simulator)", "Interactive testing sandbox allowing examiners to adjust INR amounts, merchant categories, device risks, velocities, and distance jumps, or trigger one-click attack simulations with live Explainable AI breakdowns."),
        ("3. Human-in-the-Loop Analyst Triage Queue (/queue)", "Level-2 investigation queue for Step-Up (30–70) and Blocked (>70) payments, providing digital forensic inspection, false positive release buttons, and confirmed fraud blacklist propagation."),
        ("4. Model Performance Telemetry & Curves (/metrics)", "Interactive browser visualization of ROC-AUC curves, Precision-Recall curves, confusion matrices, and latency comparison tables."),
        ("5. Regulatory Compliance & Architecture Mapping (/framework)", "Direct interactive mapping of detected attack vectors to RBI 2021 Security Guidelines, OWASP API Top 10, and PCI-DSS v4.0.")
    ]

    for i, (f_title, f_desc) in enumerate(features):
        top_pos = Inches(1.4 + i * 1.08)
        add_card(slide15, Inches(0.8), top_pos, Inches(11.73), Inches(0.96))
        tb = slide15.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.33), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f_title
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_ACCENT

        p = tf.add_paragraph()
        p.text = f_desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 16: REGULATORY & SECURITY COMPLIANCE (RBI, OWASP, PCI)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_bg(slide16, COLOR_PAGE_BG)
    add_header(slide16, "Regulatory Compliance & Cybersecurity Governance")

    compliances = [
        ("RBI Digital Payment Security Guidelines (2021)", COLOR_BLUE_ACCENT, [
            "Section 5.1: Mandatory real-time transaction velocity checks.",
            "Section 7.3: Adaptive risk-based multi-factor authentication (Step-Up 2FA).",
            "Section 8.2: Automated blocking of anomalous foreign and out-of-pattern geolocations."
        ]),
        ("OWASP API Security Top 10 Defenses", COLOR_RED, [
            "API1: Broken Object Level Authorization (BOLA) mitigations.",
            "API4: Unrestricted Resource Consumption / Automated Bot Burst rate limiting.",
            "API8: Security Misconfiguration & API parameter payload tamper prevention."
        ]),
        ("PCI-DSS v4.0 Governance Standards", COLOR_GREEN, [
            "Requirement 10: Immutable audit logging of all transactional risk evaluations.",
            "Requirement 11: Real-time anomaly detection across network endpoints.",
            "Cardholder Data Security: Zero plaintext storage of CVV and full PAN."
        ])
    ]

    for i, (c_name, c_clr, c_points) in enumerate(compliances):
        c_left = Inches(0.8 + i * 3.98)
        add_card(slide16, c_left, Inches(1.4), Inches(3.78), Inches(5.5))

        hdr = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.4), Inches(3.78), Inches(1.0))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = c_clr
        hdr.line.fill.background()

        tb_h = slide16.shapes.add_textbox(c_left + Inches(0.15), Inches(1.45), Inches(3.48), Inches(0.9))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = c_name
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        tb_b = slide16.shapes.add_textbox(c_left + Inches(0.15), Inches(2.55), Inches(3.48), Inches(4.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for p_idx, p_item in enumerate(c_points):
            p = tf_b.paragraphs[0] if p_idx == 0 else tf_b.add_paragraph()
            p.text = f"• {p_item}"
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 17: CONCLUSION & FUTURE RESEARCH EXTENSIONS
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_bg(slide17, COLOR_PAGE_BG)
    add_header(slide17, "Project Conclusion & Future Research Directions")

    # Left: Conclusion
    add_card(slide17, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
    tb_c = slide17.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(5.1))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "RESEARCH SUMMARY & ACHIEVEMENTS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    conclusions = [
        "<b>Successful Multi-Tier Engineering:</b> Proved that blending LightGBM tabular classification, Bi-directional LSTM sequence learning, and heuristic business logic outperforms single-model paradigms.",
        "<b>Rigorous Sub-25ms Real-Time Inference:</b> Satisfied NPCI and RBI payment switch processing constraints without sacrificing predictive depth.",
        "<b>Drastic False Alarm Reduction:</b> Reduced customer friction by replacing binary blocking with an adaptive 3-tier Step-Up OTP authentication policy.",
        "<b>Live Production Proof-of-Concept:</b> Deployed and accessible on global edge serverless infrastructure with full audit compliance."
    ]
    for conc in conclusions:
        p = tf_c.add_paragraph()
        p.text = "• " + conc.replace("<b>", "").replace("</b>", "")
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # Right: Future Scope
    add_card(slide17, Inches(6.8), Inches(1.4), Inches(5.73), Inches(5.5))
    tb_fs = slide17.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.1))
    tf_fs = tb_fs.text_frame
    tf_fs.word_wrap = True

    p = tf_fs.paragraphs[0]
    p.text = "FUTURE RESEARCH EXTENSIONS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    future_points = [
        ("Graph Neural Networks (GNN):", "Model cross-account transaction graphs to discover coordinated mule account rings, layered money laundering networks, and syndicate hubs."),
        ("Cross-Bank Federated Learning:", "Enable competing financial institutions (SBI, HDFC, ICICI, etc.) to train collaborative fraud models without centralizing or sharing private customer financial data."),
        ("Reinforcement Learning from Human Feedback (RLHF):", "Dynamically tune ensemble weights and score thresholds based on daily analyst dispute resolutions and confirmed chargeback rates."),
        ("Edge TPU Hardware Acceleration:", "Deploy quantized INT8 models directly to POS terminals and payment switches for sub-5 millisecond response times.")
    ]
    for f_title, f_desc in future_points:
        p = tf_fs.add_paragraph()
        p.text = f"• {f_title} {f_desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 18: REFERENCES & KEY STANDARDS
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_bg(slide18, COLOR_PAGE_BG)
    add_header(slide18, "Academic References & Regulatory Literature")

    add_card(slide18, Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.5))
    tb_ref = slide18.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.33), Inches(5.1))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    p = tf_ref.paragraphs[0]
    p.text = "SELECT BIBLIOGRAPHY & REGULATORY STANDARDS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_ACCENT

    refs = [
        "[1] Reserve Bank of India (RBI), 'Master Direction on Digital Payment Security Controls', RBI/2020-21/74, Master Direction No. 04/2021, Feb 2021.",
        "[2] National Payments Corporation of India (NPCI), 'UPI Procedural Guidelines and Operational Risk Framework', NPCI Circular 2023–24.",
        "[3] Ke, G., Meng, Q., Finley, T., et al., 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree', Advances in Neural Information Processing Systems (NeurIPS), 2017.",
        "[4] Hochreiter, S., & Schmidhuber, J., 'Long Short-Term Memory', Neural Computation, 9(8), pp. 1735–1780, 1997.",
        "[5] Liu, F. T., Ting, K. M., & Zhou, Z. H., 'Isolation Forest', IEEE International Conference on Data Mining (ICDM), pp. 413–422, 2008.",
        "[6] Payment Card Industry Security Standards Council (PCI-SSC), 'Payment Card Industry Data Security Standard (PCI-DSS) v4.0', 2022.",
        "[7] Open Web Application Security Project (OWASP), 'OWASP API Security Top 10 2023', OWASP Foundation.",
        "[8] Ministry of Law and Justice, Government of India, 'The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)', Aug 2023."
    ]
    for r in refs:
        p = tf_ref.add_paragraph()
        p.text = r
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 19: THANK YOU & Q&A DEFENSE
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_bg(slide19, COLOR_NAVY_DARK)

    # Center card
    add_card(slide19, Inches(1.5), Inches(1.2), Inches(10.33), Inches(5.1), bg_color=hex_to_rgb('#131F3B'), border_color=hex_to_rgb('#203058'))

    tb_end = slide19.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.73), Inches(4.5))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    p = tf_end.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.name = "Segoe UI"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    p = tf_end.add_paragraph()
    p.text = "QUESTIONS & ORAL DEFENSE"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = tf_end.add_paragraph()
    p.text = "AI-Powered Real-Time Fraud Detection System for Indian Banking Transactions"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(18)

    p = tf_end.add_paragraph()
    p.text = "Department of Studies in Computer Science\nKarnataka State Open University (KSOU), Mukthagangothri, Mysuru"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = hex_to_rgb('#CBD5E1')
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)

    p = tf_end.add_paragraph()
    p.text = "Under the Guidance of: Smt. Suneetha, Associate Professor, DoS in Computer Science, KSOU"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = hex_to_rgb('#94A3B8')
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)

    p = tf_end.add_paragraph()
    p.text = "Live Web Application: https://ai-fraud-detection-system-five.vercel.app\nOpen-Source Codebase: https://github.com/srinivasbv-bv/ai-fraud-detection-system"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(12)

    prs.save(filename)
    print(f"PowerPoint Presentation successfully generated: {filename}")

if __name__ == "__main__":
    create_deck()
