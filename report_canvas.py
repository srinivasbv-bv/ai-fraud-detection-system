import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

# ==============================================================================
# Two-Pass Numbered Canvas for Academic Thesis
# Supports Roman numerals for front matter and Arabic numerals for chapters
# ==============================================================================
class AcademicThesisCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicThesisCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"\n>>> TOTAL DISSERTATION PAGES RENDERED: {num_pages} PAGES <<<\n")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_academic_decorations(num_pages)
            super(AcademicThesisCanvas, self).showPage()
        super(AcademicThesisCanvas, self).save()

    def draw_academic_decorations(self, total_pages):
        page_num = self._pageNumber
        self.saveState()

        # Suppress headers and footers on Cover Page (page 1)
        if page_num > 1:
            self.setFont("Times-Roman", 9)
            self.setFillColor(colors.HexColor("#475569"))

            # Running Header
            header_text = "AI-POWERED FRAUD DETECTION SYSTEM FOR ONLINE TRANSACTIONS"
            self.drawString(54, letter[1] - 36, header_text)
            self.drawRightString(letter[0] - 54, letter[1] - 36, "MSc. CS Project Report")
            self.setStrokeColor(colors.HexColor("#94a3b8"))
            self.setLineWidth(0.6)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

            # Running Footer
            self.line(54, 46, letter[0] - 54, 46)
            self.drawString(54, 32, "Department of Studies in Computer Science, KSOU, Mysore")
            self.drawRightString(letter[0] - 54, 32, f"Page {page_num} of {total_pages}")

        self.restoreState()

print("AcademicThesisCanvas defined successfully.")
