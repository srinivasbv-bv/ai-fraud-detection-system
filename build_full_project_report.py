import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from report_canvas import AcademicThesisCanvas
from report_front_matter import build_front_matter
from report_chapters_1_to_3 import build_chapters_1_to_3
from report_chapters_4_to_6 import build_chapters_4_to_6
from report_chapters_7_to_10 import build_chapters_7_to_10
from report_extensions import build_extended_chapters
from report_back_matter import build_back_matter
from report_extended_appendices import build_extended_appendices

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(PROJECT_DIR, "MSc_Computer_Science_Project_Report.pdf")

def generate_report():
    print("=" * 70)
    print(" COMPILING FULL MSC COMPUTER SCIENCE DISSERTATION REPORT")
    print(f" Target File: {OUTPUT_PDF}")
    print("=" * 70)

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,   # 0.75 in
        rightMargin=54,  # 0.75 in
        topMargin=54,    # 0.75 in
        bottomMargin=54  # 0.75 in
    )

    story = []

    print("1. Assembling Front Matter (Cover, Certificate, Declaration, TOC, Figures, Tables, Abbreviations)...")
    story.extend(build_front_matter())

    print("2. Assembling Chapters 1 to 3 (Introduction, Literature Review, Theoretical Foundations)...")
    story.extend(build_chapters_1_to_3())

    print("3. Assembling Chapters 4 to 6 (SRS, System Architecture, Methodology & Equations)...")
    story.extend(build_chapters_4_to_6())

    print("4. Assembling Extended Analysis & Benchmarks (XAI, DFD Subsystems, Per-Category Metrics)...")
    story.extend(build_extended_chapters())

    print("5. Assembling Chapters 7 to 10 (Implementation, Testing, UI Walkthrough, Conclusion)...")
    story.extend(build_chapters_7_to_10())

    print("6. Assembling References & Bibliography (30+ IEEE Citations)...")
    story.extend(build_back_matter())

    print("7. Assembling Complete Source Code Listings (Appendices A to H)...")
    story.extend(build_extended_appendices())

    print(f"\nTotal story flowables assembled: {len(story)}. Rendering PDF with AcademicThesisCanvas...")
    doc.build(story, canvasmaker=AcademicThesisCanvas)

    print("=" * 70)
    print(" DISSERTATION BUILD SUCCESSFULLY COMPLETED!")
    print(f" Output Location: {OUTPUT_PDF}")
    print("=" * 70)

if __name__ == '__main__':
    generate_report()
