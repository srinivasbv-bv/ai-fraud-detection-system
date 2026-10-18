import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(PROJECT_DIR, 'assets', 'report_figures')

def get_report_styles():
    base_styles = getSampleStyleSheet()
    
    styles = {
        'CoverTitle': ParagraphStyle(
            'CoverTitle',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=15
        ),
        'CoverSubtitle': ParagraphStyle(
            'CoverSubtitle',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1e3a8a"),
            spaceAfter=25
        ),
        'CoverBody': ParagraphStyle(
            'CoverBody',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1e293b")
        ),
        'CoverInstitution': ParagraphStyle(
            'CoverInstitution',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a")
        ),
        'ChapterHeader': ParagraphStyle(
            'ChapterHeader',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=15,
            spaceAfter=18,
            keepWithNext=True
        ),
        'SectionHeader': ParagraphStyle(
            'SectionHeader',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=13,
            leading=17,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1e3a8a"),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        ),
        'SubSectionHeader': ParagraphStyle(
            'SubSectionHeader',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=11,
            leading=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0284c7"),
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=10,
            leading=14.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=8,
            firstLineIndent=20
        ),
        'BodyNoIndent': ParagraphStyle(
            'BodyNoIndent',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=10,
            leading=14.5,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=8
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1e293b"),
            leftIndent=24,
            firstLineIndent=-12,
            spaceAfter=5
        ),
        'Formula': ParagraphStyle(
            'Formula',
            parent=base_styles['Normal'],
            fontName='Times-Italic',
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=6,
            spaceAfter=6
        ),
        'Caption': ParagraphStyle(
            'Caption',
            parent=base_styles['Normal'],
            fontName='Times-BoldItalic',
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475569"),
            spaceBefore=6,
            spaceAfter=12,
            keepWithNext=True
        ),
        'TableHead': ParagraphStyle(
            'TableHead',
            parent=base_styles['Normal'],
            fontName='Times-Bold',
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a")
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=8.5,
            leading=11.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1e293b")
        ),
        'TableCellCenter': ParagraphStyle(
            'TableCellCenter',
            parent=base_styles['Normal'],
            fontName='Times-Roman',
            fontSize=8.5,
            leading=11.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1e293b")
        ),
        'CodeBlock': ParagraphStyle(
            'CodeBlock',
            parent=base_styles['Normal'],
            fontName='Courier',
            fontSize=7.8,
            leading=10.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#0f172a")
        )
    }
    return styles

def make_callout_box(text, title="NOTE / SPECIFICATION"):
    styles = get_report_styles()
    p_title = Paragraph(f"<b>{title}:</b>", styles['SubSectionHeader'])
    p_text = Paragraph(text, styles['BodyNoIndent'])
    t = Table([[p_title], [p_text]], colWidths=[letter[0] - 108])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINELEFT', (0, 0), (-1, -1), 3, colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    return t

def make_code_box(code_text, chunk_lines=28):
    styles = get_report_styles()
    lines = code_text.splitlines()
    flowables = []
    
    for i in range(0, len(lines), chunk_lines):
        chunk = "\n".join(lines[i:i + chunk_lines])
        escaped = chunk.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')
        p = Paragraph(escaped, styles['CodeBlock'])
        t = Table([[p]], colWidths=[letter[0] - 108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        flowables.append(t)
        if i + chunk_lines < len(lines):
            flowables.append(Spacer(1, 4))
            
    return flowables

print("Updated report_builder_base.py with chunking make_code_box.")
