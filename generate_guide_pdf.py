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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "AI-Powered Fraud Detection System — Setup & Deployment Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 30, footer_text)
        self.drawString(54, 30, "Confidential & Academic / Technical Project Documentation")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 42, letter[0] - 54, 42)
        
        self.restoreState()

def build_pdf(filename="Project_Setup_and_Deployment_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#2563eb")      # Blue 600
    c_sub = colors.HexColor("#334155")         # Slate 700
    c_body = colors.HexColor("#1e293b")        # Slate 800
    c_card_bg = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#cbd5e1")      # Slate 300
    c_code_bg = colors.HexColor("#0f172a")     # Dark code box
    c_code_text = colors.HexColor("#38bdf8")   # Cyan code
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=12,
        textColor=c_code_text
    )

    note_style = ParagraphStyle(
        'Note_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569")
    )

    def make_code_box(command_text):
        escaped = command_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')
        p = Paragraph(escaped, code_style)
        t = Table([[p]], colWidths=[letter[0] - 108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_code_bg),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#1e293b")),
        ]))
        return t

    def make_callout(text, title="IMPORTANT NOTE"):
        content = [
            Paragraph(f"<b>{title}:</b> {text}", note_style)
        ]
        t = Table([[content]], colWidths=[letter[0] - 108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('LINELEFT', (0, 0), (-1, -1), 3, c_accent),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#bfdbfe")),
        ]))
        return t

    story = []

    # Document Header Banner
    story.append(Paragraph("AI-Powered Fraud Detection System for Online Transactions", title_style))
    story.append(Paragraph("Complete Comprehensive Guide: Local Execution, GitHub Publishing & Vercel Cloud Deployment", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=14))

    # Executive Overview
    story.append(Paragraph("1. Executive Project Overview", h1_style))
    story.append(Paragraph(
        "This project is an advanced, production-grade <b>Dual-Path AI Fraud Detection System</b> designed "
        "specifically for modern digital payment systems (UPI, Credit/Debit Cards, Netbanking). It incorporates an "
        "<b>Ensemble Risk Scoring Engine</b> combining tree-based supervised machine learning (XGBoost / Random Forest), "
        "recurrent neural anomaly detection (LSTM / Autoencoder), and heuristic compliance overlays mapped to "
        "<b>OWASP API Security Top 10 (2023)</b> and <b>PCI DSS v4.0</b> requirements.",
        body_style
    ))
    story.append(Spacer(1, 4))

    overview_table_data = [
        [Paragraph("<b>Key Capability</b>", body_style), Paragraph("<b>Implementation Architecture</b>", body_style)],
        [Paragraph("<b>Supervised Scoring (45%)</b>", body_style), Paragraph("XGBoost / Random Forest with SMOTE balancing tabular features", body_style)],
        [Paragraph("<b>Deep Sequence Scoring (40%)</b>", body_style), Paragraph("LSTM & Autoencoder sequence window ($T=10$) for temporal ATO detection", body_style)],
        [Paragraph("<b>Rule Overlay (15%)</b>", body_style), Paragraph("Velocity bursts, device mismatch penalties, high-value heuristics", body_style)],
        [Paragraph("<b>Decision Policy</b>", body_style), Paragraph("Calibrated 3-tier action: <b>Approve</b> (&lt;35), <b>Step-Up 2FA</b> (35-70), <b>Block</b> (&gt;70)", body_style)],
        [Paragraph("<b>Currency Ecosystem</b>", body_style), Paragraph("Calibrated for Indian Rupee (INR ₹) UPI, Food Apps, E-Commerce, Gaming", body_style)],
    ]
    t_overview = Table(overview_table_data, colWidths=[160, letter[0] - 108 - 160])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))

    # Section 2: Prerequisites
    story.append(Paragraph("2. System Prerequisites & Environment", h1_style))
    story.append(Paragraph("Before starting, ensure the recipient's computer has the following tools installed:", body_style))
    story.append(Paragraph("• <b>Python 3.10, 3.11, or 3.12</b> installed (check with <code>python --version</code>). Ensure <i>Add Python to PATH</i> was checked during installation.", bullet_style))
    story.append(Paragraph("• <b>Git</b> installed (check with <code>git --version</code>) for version control and GitHub operations.", bullet_style))
    story.append(Paragraph("• <b>Modern Web Browser</b> (Google Chrome, Microsoft Edge, Mozilla Firefox, or Brave).", bullet_style))
    story.append(Paragraph("• <b>Code Editor / Terminal</b> (VS Code, Windows PowerShell, Terminal on macOS/Linux).", bullet_style))
    story.append(Spacer(1, 8))

    # Section 3: Step-by-Step Local Setup
    story.append(Paragraph("3. Step-by-Step Guide: Running the Project Locally", h1_style))
    story.append(Paragraph(
        "Follow these exact steps to run the complete fraud detection web dashboard and real-time transaction simulator on any Windows, macOS, or Linux machine.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 3.1 — Extract or Navigate to Project Folder", h2_style))
    story.append(Paragraph(
        "Place the project folder anywhere on your computer (e.g. <code>C:\\projects\\ai_fraud_detection_system</code> or <code>~/ai_fraud_detection_system</code>). Open your terminal/PowerShell inside this directory:",
        body_style
    ))
    story.append(make_code_box("cd path/to/ai_fraud_detection_system"))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.2 — Create & Activate Virtual Environment", h2_style))
    story.append(Paragraph(
        "It is strongly recommended to isolate dependencies inside a dedicated Python virtual environment:",
        body_style
    ))
    story.append(make_code_box(
        "# Windows (PowerShell or Command Prompt):\n"
        "python -m venv venv\n"
        ".\\venv\\Scripts\\activate\n\n"
        "# macOS / Linux:\n"
        "python3 -m venv venv\n"
        "source venv/bin/activate"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.3 — Install Dependencies", h2_style))
    story.append(Paragraph(
        "Install the required libraries listed in <code>requirements.txt</code>:",
        body_style
    ))
    story.append(make_code_box("pip install -r requirements.txt"))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.4 — Verify / Train Models (Optional & Automated)", h2_style))
    story.append(Paragraph(
        "The project comes with pre-trained models. However, you can run the automated verification test suite or retrain the models with one command:",
        body_style
    ))
    story.append(make_code_box(
        "# Run Automated Unit Verification (100% Passing Check):\n"
        "python test_system.py\n\n"
        "# (Optional) Retrain all models on a fresh 15,000 transaction dataset:\n"
        "python train_all.py"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.5 — Start the Flask Web Application", h2_style))
    story.append(Paragraph(
        "Launch the backend web server and API engine:",
        body_style
    ))
    story.append(make_code_box("python app.py"))
    story.append(Paragraph(
        "The terminal will indicate that the server is running on <b>http://127.0.0.1:5000</b>. "
        "Open this URL in your web browser to access the interactive dashboard.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.6 — Launch Real-Time Payment Stream Simulator", h2_style))
    story.append(Paragraph(
        "Open a <b>second terminal window</b>, activate the virtual environment, and run the real-time payment streaming simulator:",
        body_style
    ))
    story.append(make_code_box(
        "cd path/to/ai_fraud_detection_system\n"
        "# Activate venv (e.g. .\\venv\\Scripts\\activate)\n"
        "python live_checkout_stream.py"
    ))
    story.append(Paragraph(
        "This script continuously emits simulated UPI, Card, and Netbanking payments every 2.5 seconds. "
        "Switch back to your browser at <code>http://127.0.0.1:5000</code> to observe real-time charts updating automatically!",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Page Break for clean multi-page document
    story.append(PageBreak())

    # Section 4: Web Application Navigation
    story.append(Paragraph("4. Web Application User Guide & Modules", h1_style))
    story.append(Paragraph(
        "The web interface contains five specialized views accessible via the top navigation bar:",
        body_style
    ))

    nav_data = [
        [Paragraph("<b>Navigation Tab</b>", body_style), Paragraph("<b>Functionality & Evaluation Role</b>", body_style)],
        [Paragraph("<b>Dashboard (/)</b>", body_style), Paragraph("Displays total evaluated transactions, approval rates, 2FA challenges, blocked attacks, decision doughnut chart, and fraud categories bar chart.", body_style)],
        [Paragraph("<b>Live Simulator (/simulator)</b>", body_style), Paragraph("Allows entering custom transaction attributes (Amount ₹, Category, Device Risk, Velocity, Hour). Features 4 quick preset buttons (UPI Kirana, Card Fraud, ATO, Velocity Burst) to test instant risk evaluation.", body_style)],
        [Paragraph("<b>Analyst Queue (/queue)</b>", body_style), Paragraph("Interactive fraud analyst workstation. Allows manual inspection of flagged transactions with 1-click 'Approve' or 'Block Fraud' override actions.", body_style)],
        [Paragraph("<b>Model Metrics (/metrics)</b>", body_style), Paragraph("Visualizes model performance metrics (Precision, Recall, F1-Score, AUC-PR, ROC-AUC) along with interactive Precision-Recall and ROC curves.", body_style)],
        [Paragraph("<b>Framework Mapping (/framework)</b>", body_style), Paragraph("Detailed enterprise security audit matrix mapping all 5 fraud types to OWASP API Security Top 10 (2023) and PCI DSS v4.0 regulatory controls.", body_style)],
    ]
    t_nav = Table(nav_data, colWidths=[150, letter[0] - 108 - 150])
    t_nav.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_nav)
    story.append(Spacer(1, 12))

    # Section 5: GitHub Upload Instructions
    story.append(Paragraph("5. Step-by-Step Guide: Uploading Code to Your GitHub Repository", h1_style))
    story.append(Paragraph(
        "Follow these steps to upload the project code to your personal GitHub account:",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 5.1 — Create an Empty Repository on GitHub", h2_style))
    story.append(Paragraph("1. Log in to your GitHub account at <b>https://github.com</b>.", bullet_style))
    story.append(Paragraph("2. In the top-right corner, click the <b>+</b> icon and select <b>New repository</b> (or visit <b>https://github.com/new</b>).", bullet_style))
    story.append(Paragraph("3. Enter a <b>Repository name</b>, for example: <code>ai-fraud-detection-system</code>.", bullet_style))
    story.append(Paragraph("4. Select <b>Public</b> or <b>Private</b>.", bullet_style))
    story.append(Paragraph("5. <b>CRITICAL:</b> Leave 'Add a README file', '.gitignore', and 'Choose a license' <b>UNCHECKED</b> (the project already contains these files).", bullet_style))
    story.append(Paragraph("6. Click the green <b>Create repository</b> button.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 5.2 — Initialize and Push Code From Terminal", h2_style))
    story.append(Paragraph(
        "Open a terminal in the project directory and run the following commands sequentially. "
        "Replace <code>&lt;YOUR_GITHUB_USERNAME&gt;</code> and <code>&lt;YOUR_REPOSITORY_NAME&gt;</code> with your actual GitHub details:",
        body_style
    ))
    story.append(make_code_box(
        "# 1. Initialize git and configure your identity:\n"
        "git init\n"
        "git config user.name \"Your Name\"\n"
        "git config user.email \"your_email@example.com\"\n\n"
        "# 2. Stage all project files and commit:\n"
        "git add .\n"
        "git commit -m \"Initial commit of AI-Powered Fraud Detection System\"\n\n"
        "# 3. Set primary branch to main:\n"
        "git branch -M main\n\n"
        "# 4. Link your personal GitHub repository:\n"
        "git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git\n\n"
        "# 5. Push files to GitHub:\n"
        "git push -u origin main"
    ))
    story.append(Spacer(1, 6))
    story.append(make_callout(
        "If you are using an existing Git repository, you can reset the remote using: "
        "<code>git remote set-url origin https://github.com/&lt;YOUR_GITHUB_USERNAME&gt;/&lt;YOUR_REPOSITORY_NAME&gt;.git</code> followed by <code>git push -u origin main</code>.",
        "GIT REMOTE TIP"
    ))
    story.append(Spacer(1, 12))

    # Section 6: Vercel Deployment Instructions
    story.append(Paragraph("6. Step-by-Step Guide: Launching & Hosting on Vercel", h1_style))
    story.append(Paragraph(
        "The project is pre-configured with <code>vercel.json</code> and an <code>api/index.py</code> serverless WSGI wrapper, "
        "making deployment to Vercel completely automated.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 6.1 — Log in to Vercel", h2_style))
    story.append(Paragraph("1. Open your browser and navigate to <b>https://vercel.com</b>.", bullet_style))
    story.append(Paragraph("2. Click <b>Log In</b> or <b>Sign Up</b>.", bullet_style))
    story.append(Paragraph("3. Choose <b>Continue with GitHub</b>. This grants Vercel direct access to import your repository.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.2 — Import the Project Repository", h2_style))
    story.append(Paragraph("1. On the Vercel Dashboard, click the <b>Add New...</b> button in the top-right corner and select <b>Project</b>.", bullet_style))
    story.append(Paragraph("2. Under the <b>Import Git Repository</b> section, locate your repository (e.g. <code>ai-fraud-detection-system</code>).", bullet_style))
    story.append(Paragraph("3. Click the <b>Import</b> button next to your repository name.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.3 — Configure & Deploy", h2_style))
    story.append(Paragraph("1. <b>Project Name:</b> Keep default or customize (e.g. <code>ai-fraud-detection-system</code>).", bullet_style))
    story.append(Paragraph("2. <b>Framework Preset:</b> Leave as <b>Other</b> (Vercel automatically detects the Python runtime).", bullet_style))
    story.append(Paragraph("3. <b>Root Directory:</b> Leave as <code>./</code>.", bullet_style))
    story.append(Paragraph("4. Click the blue <b>Deploy</b> button.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.4 — Access Your Live Web Application", h2_style))
    story.append(Paragraph(
        "Vercel will build the Python environment in approximately 30–60 seconds. Once complete, you will see a "
        "<b>Congratulations!</b> screen with a preview screenshot and your live public URL (e.g. <code>https://ai-fraud-detection-system.vercel.app</code>). "
        "Anyone in the world can now interact with your fraud detection platform securely via HTTPS!",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(make_callout(
        "Vercel operates as a stateless Serverless Function environment. While the web dashboard, API evaluation, simulator, and metrics "
        "run seamlessly on Vercel, background continuous looping scripts (such as <code>live_checkout_stream.py</code>) should be executed on your local machine "
        "targeting either your local host (<code>http://127.0.0.1:5000/api/evaluate</code>) or your live Vercel endpoint.",
        "SERVERLESS ARCHITECTURE NOTE"
    ))
    story.append(Spacer(1, 10))

    # Section 7: Troubleshooting FAQ
    story.append(Paragraph("7. Frequently Encountered Questions & Troubleshooting", h1_style))
    
    faq_data = [
        [Paragraph("<b>Issue / Question</b>", body_style), Paragraph("<b>Resolution & Explanation</b>", body_style)],
        [
            Paragraph("<b>Port 5000 Already in Use</b>", body_style),
            Paragraph("If another app is using port 5000, start Flask on a different port: <code>flask run --port 5001</code> or edit line 185 of <code>app.py</code> to <code>port=5001</code>.", body_style)
        ],
        [
            Paragraph("<b>Script Execution Policy Error (Windows)</b>", body_style),
            Paragraph("If PowerShell blocks virtual environment activation, run: <code>Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned</code> then re-activate.", body_style)
        ],
        [
            Paragraph("<b>Git Authentication Error on Push</b>", body_style),
            Paragraph("GitHub requires a <b>Personal Access Token (PAT)</b> or GitHub Credential Manager instead of your account password. Generate a token under <i>GitHub Settings &gt; Developer Settings &gt; Personal Access Tokens</i>.", body_style)
        ],
        [
            Paragraph("<b>Modifying Thresholds / Weights</b>", body_style),
            Paragraph("All global decision boundaries (35 / 70) and ensemble weights (45% supervised, 40% sequence, 15% rules) are centralized in <code>config.py</code> for rapid tuning.", body_style)
        ]
    ]
    t_faq = Table(faq_data, colWidths=[150, letter[0] - 108 - 150])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_faq)
    story.append(Spacer(1, 14))

    # Final Summary Sign-off
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
    story.append(Paragraph(
        "<b>Document Information:</b> Generated for academic distribution, project assessment, and technical review. "
        "Contains complete instructions for autonomous replication, source control, and cloud serverless hosting.",
        note_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    target_path = sys.argv[1] if len(sys.argv) > 1 else "Project_Setup_and_Deployment_Guide.pdf"
    build_pdf(target_path)
