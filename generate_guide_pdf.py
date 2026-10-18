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
            self.drawString(54, letter[1] - 36, "AI-Powered Fraud Detection System — Local (CMD), GitHub & Vercel Guide")
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
        fontSize=21,
        leading=25,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=15,
        textColor=c_accent,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=7,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_accent,
        spaceBefore=9,
        spaceAfter=5,
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

    def make_callout(text, title="TIP / NOTE"):
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
    story.append(Paragraph("Complete Step-by-Step Guide: Running on CMD (Command Prompt), GitHub & Vercel", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=12))

    # Executive Overview
    story.append(Paragraph("1. Executive Project Summary", h1_style))
    story.append(Paragraph(
        "This project implements an enterprise-grade <b>Dual-Path AI Fraud Detection System</b> designed for online transactions "
        "(UPI, Credit/Debit Cards, Netbanking). It combines tree-based supervised machine learning (XGBoost / Random Forest), "
        "deep sequence anomaly detection (LSTM / Autoencoder), and heuristic rules mapped directly to "
        "<b>OWASP API Security Top 10 (2023)</b> and <b>PCI DSS v4.0</b> compliance standards.",
        body_style
    ))
    story.append(Spacer(1, 4))

    overview_table_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technical Architecture & Specs</b>", body_style)],
        [Paragraph("<b>Supervised Scoring (45%)</b>", body_style), Paragraph("XGBoost / Random Forest with SMOTE balancing tabular features", body_style)],
        [Paragraph("<b>Deep Sequence Scoring (40%)</b>", body_style), Paragraph("LSTM & Autoencoder sliding sequence ($T=10$) for temporal ATO detection", body_style)],
        [Paragraph("<b>Rule Overlay (15%)</b>", body_style), Paragraph("Velocity bursts, device mismatch penalties, high-value heuristics", body_style)],
        [Paragraph("<b>Decision Policy</b>", body_style), Paragraph("3-Tier Policy: <b>Approve</b> (&lt;35), <b>Step-Up 2FA</b> (35-70), <b>Block</b> (&gt;70)", body_style)],
        [Paragraph("<b>Currency Ecosystem</b>", body_style), Paragraph("Calibrated in Indian Rupees (INR ₹) for UPI, E-Commerce, Swiggy/Zomato, Gaming", body_style)],
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
    story.append(Paragraph("2. System Prerequisites", h1_style))
    story.append(Paragraph("Make sure your system has the following installed before proceeding:", body_style))
    story.append(Paragraph("• <b>Python 3.10, 3.11, or 3.12:</b> Download from <i>python.org</i>. <b>Important:</b> Check the box <i>'Add Python to PATH'</i> during installation.", bullet_style))
    story.append(Paragraph("• <b>Git:</b> Download and install from <i>git-scm.com</i>.", bullet_style))
    story.append(Paragraph("• <b>Modern Web Browser:</b> Chrome, Edge, Firefox, or Brave.", bullet_style))
    story.append(Spacer(1, 8))

    # Section 3: Step-by-Step Local Setup via CMD
    story.append(Paragraph("3. Running Locally Using Command Prompt (CMD) Inside Project Folder", h1_style))
    story.append(Paragraph(
        "<b>YES! You can run the entire project directly using Windows Command Prompt (CMD) inside the project folder.</b> "
        "In fact, running in CMD inside the folder is the easiest and most recommended method because it avoids PowerShell script execution policy errors.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 3.1 — How to Open CMD Directly Inside the Project Folder (The 2-Second Shortcut)", h2_style))
    story.append(Paragraph(
        "You do NOT need to type long paths or use complex <code>cd</code> commands. Follow this simple shortcut:",
        body_style
    ))
    story.append(Paragraph("1. Open the <code>ai_fraud_detection_system</code> project folder in Windows File Explorer.", bullet_style))
    story.append(Paragraph("2. Click on the <b>address / location bar</b> at the top of the folder window (where the folder path is shown).", bullet_style))
    story.append(Paragraph("3. Type <b><code>cmd</code></b> and press <b>Enter</b> on your keyboard.", bullet_style))
    story.append(Paragraph("4. A black Command Prompt window will instantly open, <b>already located inside your project folder!</b>", bullet_style))
    story.append(Spacer(1, 4))

    story.append(make_callout(
        "Whenever you open CMD via the File Explorer address bar, the prompt automatically displays your project folder path. You are immediately ready to run project commands!",
        "EXPLORER SHORTCUT"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.2 — Create & Activate Virtual Environment in CMD", h2_style))
    story.append(Paragraph(
        "Inside your opened CMD window, run the following commands to create and activate an isolated Python environment:",
        body_style
    ))
    story.append(make_code_box(
        ":: Create a virtual environment named 'venv'\n"
        "python -m venv venv\n\n"
        ":: Activate the virtual environment in CMD\n"
        "venv\\Scripts\\activate"
    ))
    story.append(Paragraph(
        "Once activated, you will see <b><code>(venv)</code></b> appear at the very beginning of your CMD line.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.3 — Install Project Dependencies", h2_style))
    story.append(Paragraph("Run the pip installation command inside CMD:", body_style))
    story.append(make_code_box("pip install -r requirements.txt"))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.4 — Verify System Tests (Optional & Fast)", h2_style))
    story.append(Paragraph("Run the automated verification suite to verify that dataset loading and ML models pass 100%:", body_style))
    story.append(make_code_box(
        ":: Run system test suite (100% passing check)\n"
        "python test_system.py"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.5 — Start the Web Application Server", h2_style))
    story.append(Paragraph("Launch the Flask application engine from your CMD window:", body_style))
    story.append(make_code_box("python app.py"))
    story.append(Paragraph(
        "CMD will display: <code>* Running on http://127.0.0.1:5000</code>.<br/>"
        "Open your web browser and navigate to: <b>http://127.0.0.1:5000</b> to view the live dashboard!",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 3.6 — Launch Live Real-Time Payment Stream (In a Second CMD Window)", h2_style))
    story.append(Paragraph(
        "To simulate real-time live payments arriving at the system every 2.5 seconds:",
        body_style
    ))
    story.append(Paragraph("1. Open the project folder in File Explorer again, click the address bar, type <b><code>cmd</code></b>, and press <b>Enter</b> to open a <b>second CMD window</b>.", bullet_style))
    story.append(Paragraph("2. In this second CMD window, activate the venv and run the streaming script:", bullet_style))
    story.append(make_code_box(
        "venv\\Scripts\\activate\n"
        "python live_checkout_stream.py"
    ))
    story.append(Paragraph(
        "This window will stream live incoming transactions. Keep both CMD windows open. "
        "Switch to your browser at <code>http://127.0.0.1:5000</code> to observe real-time transaction charts updating dynamically!",
        body_style
    ))
    story.append(Spacer(1, 8))

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

    # Section 5: GitHub Upload Instructions via CMD
    story.append(Paragraph("5. Step-by-Step Guide: Uploading Code to GitHub via CMD", h1_style))
    story.append(Paragraph(
        "You can run all Git upload commands directly inside the same Command Prompt (CMD) window:",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 5.1 — Create an Empty Repository on GitHub", h2_style))
    story.append(Paragraph("1. Log in to your GitHub account at <b>https://github.com</b>.", bullet_style))
    story.append(Paragraph("2. In the top-right corner, click the <b>+</b> icon and select <b>New repository</b> (or go to <b>https://github.com/new</b>).", bullet_style))
    story.append(Paragraph("3. Enter a <b>Repository name</b> (e.g. <code>ai-fraud-detection-system</code>).", bullet_style))
    story.append(Paragraph("4. Select <b>Public</b> or <b>Private</b>.", bullet_style))
    story.append(Paragraph("5. <b>CRITICAL:</b> Leave 'Add a README file', '.gitignore', and 'Choose a license' <b>UNCHECKED</b> (the project already has these configured).", bullet_style))
    story.append(Paragraph("6. Click the green <b>Create repository</b> button.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 5.2 — Run Git Commands in CMD", h2_style))
    story.append(Paragraph(
        "Inside your CMD window located in the project folder, run the following commands sequentially. "
        "Replace <code>&lt;YOUR_GITHUB_USERNAME&gt;</code> and <code>&lt;YOUR_REPOSITORY_NAME&gt;</code> with your actual GitHub username and repo name:",
        body_style
    ))
    story.append(make_code_box(
        ":: 1. Configure your Git identity (one-time setup)\n"
        "git config user.name \"Your Name\"\n"
        "git config user.email \"your_email@example.com\"\n\n"
        ":: 2. Initialize and stage all project files\n"
        "git init\n"
        "git add .\n"
        "git commit -m \"Initial commit of AI Fraud Detection System\"\n\n"
        ":: 3. Set branch to main\n"
        "git branch -M main\n\n"
        ":: 4. Link your GitHub repository\n"
        "git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git\n\n"
        ":: 5. Push code to GitHub\n"
        "git push -u origin main"
    ))
    story.append(Spacer(1, 6))
    story.append(make_callout(
        "If your project already has a remote configured, simply update it using: "
        "<code>git remote set-url origin https://github.com/&lt;YOUR_GITHUB_USERNAME&gt;/&lt;YOUR_REPOSITORY_NAME&gt;.git</code> and then run <code>git push -u origin main</code>.",
        "GIT REMOTE UPDATE"
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
    story.append(Paragraph("2. Click <b>Log In</b> or <b>Sign Up</b> and select <b>Continue with GitHub</b>.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.2 — Import Your GitHub Repository", h2_style))
    story.append(Paragraph("1. On the Vercel Dashboard, click the <b>Add New...</b> button in the top-right corner and select <b>Project</b>.", bullet_style))
    story.append(Paragraph("2. Under <b>Import Git Repository</b>, locate your repository (e.g. <code>ai-fraud-detection-system</code>) and click <b>Import</b>.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.3 — Deploy with 1-Click", h2_style))
    story.append(Paragraph("1. Leave <b>Framework Preset</b> as <b>Other</b> (Vercel automatically detects the Python runtime).", bullet_style))
    story.append(Paragraph("2. Leave <b>Root Directory</b> as <code>./</code>.", bullet_style))
    story.append(Paragraph("3. Click the blue <b>Deploy</b> button.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6.4 — Access Your Live Web Application", h2_style))
    story.append(Paragraph(
        "Vercel will build and deploy the Python app in 30–60 seconds. Once completed, Vercel provides a live public "
        "HTTPS URL (e.g. <code>https://ai-fraud-detection-system.vercel.app</code>) that anyone can visit globally!",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(make_callout(
        "Vercel runs as a serverless function environment. The web dashboard, interactive simulator, analyst queue, and metrics "
        "run fully on Vercel. Background continuous looping streams (like <code>live_checkout_stream.py</code>) are meant for local execution on CMD.",
        "SERVERLESS ARCHITECTURE NOTE"
    ))
    story.append(Spacer(1, 10))

    # Section 7: Troubleshooting FAQ
    story.append(Paragraph("7. Frequently Encountered Questions & Troubleshooting", h1_style))
    
    faq_data = [
        [Paragraph("<b>Scenario / Question</b>", body_style), Paragraph("<b>CMD Solution & Explanation</b>", body_style)],
        [
            Paragraph("<b>'python' is not recognized in CMD</b>", body_style),
            Paragraph("Python was not added to your Windows PATH during installation. Re-run the Python installer, select <b>Modify</b>, and ensure <b>'Add Python to environment variables'</b> is checked.", body_style)
        ],
        [
            Paragraph("<b>Port 5000 Already in Use</b>", body_style),
            Paragraph("If another app is using port 5000, start Flask on another port in CMD: <code>python app.py --port 5001</code> or edit port in <code>app.py</code>.", body_style)
        ],
        [
            Paragraph("<b>How to stop the server in CMD?</b>", body_style),
            Paragraph("Press <b>Ctrl + C</b> in the Command Prompt window to cleanly stop the Flask application or the live streaming simulator.", body_style)
        ],
        [
            Paragraph("<b>Git Authentication Error on Push</b>", body_style),
            Paragraph("GitHub requires a <b>Personal Access Token (PAT)</b> or GitHub Credential Manager. Generate a token under <i>GitHub Settings &gt; Developer Settings &gt; Personal Access Tokens</i> if prompted.", body_style)
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
