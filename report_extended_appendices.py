import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from report_builder_base import get_report_styles, make_code_box

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_code_file(rel_path):
    path = os.path.join(PROJECT_DIR, rel_path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return f"# File {rel_path} not found"

def build_extended_appendices():
    styles = get_report_styles()
    story = []

    story.append(Paragraph("<b>COMPLETE SOURCE CODE LISTINGS</b>", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=18))

    # Appendix A: config.py
    story.append(Paragraph("APPENDIX A: SYSTEM CONFIGURATION (config.py)", styles['SectionHeader']))
    story.append(Paragraph("The centralized configuration file defines threshold parameters, weights, and regulatory taxonomies:", styles['BodyNoIndent']))
    config_code = read_code_file('config.py')
    story.extend(make_code_box(config_code))
    story.append(PageBreak())

    # Appendix B: data/generator.py
    story.append(Paragraph("APPENDIX B: BENCHMARK DATASET GENERATOR (data/generator.py)", styles['SectionHeader']))
    story.append(Paragraph("The data generation module synthesizes 15,000 realistic Indian transactions and sliding temporal sequences:", styles['BodyNoIndent']))
    gen_code = read_code_file(os.path.join('data', 'generator.py'))
    story.extend(make_code_box(gen_code))
    story.append(PageBreak())

    # Appendix C: data/dataset_loader.py
    story.append(Paragraph("APPENDIX C: DATASET PREPROCESSING & SMOTE RESAMPLING (data/dataset_loader.py)", styles['SectionHeader']))
    story.append(Paragraph("Handles StandardScaler normalization, OneHotEncoding, and SMOTE class-imbalance oversampling:", styles['BodyNoIndent']))
    loader_code = read_code_file(os.path.join('data', 'dataset_loader.py'))
    story.extend(make_code_box(loader_code))
    story.append(PageBreak())

    # Appendix D: models/ensemble_engine.py
    story.append(Paragraph("APPENDIX D: ENSEMBLE RISK SCORING ENGINE (models/ensemble_engine.py)", styles['SectionHeader']))
    story.append(Paragraph("Executes the calibrated multi-criteria fusion function and enforces heuristic business rule penalties:", styles['BodyNoIndent']))
    engine_code = read_code_file(os.path.join('models', 'ensemble_engine.py'))
    story.extend(make_code_box(engine_code))
    story.append(PageBreak())

    # Appendix E: framework/mapping_engine.py
    story.append(Paragraph("APPENDIX E: REGULATORY FRAMEWORK MAPPING ENGINE (framework/mapping_engine.py)", styles['SectionHeader']))
    story.append(Paragraph("Maps evaluated transactions to OWASP API Security Top 10 (2023) and PCI DSS v4.0 audit requirements:", styles['BodyNoIndent']))
    map_code = read_code_file(os.path.join('framework', 'mapping_engine.py'))
    story.extend(make_code_box(map_code))
    story.append(PageBreak())

    # Appendix F: logging_elk/elk_logger.py
    story.append(Paragraph("APPENDIX F: SECURITY AUDIT & NDJSON LOGGING SERVICE (logging_elk/elk_logger.py)", styles['SectionHeader']))
    story.append(Paragraph("Formats transaction evaluations into immutable ISO-8601 JSON documents for Logstash and Elasticsearch:", styles['BodyNoIndent']))
    elk_code = read_code_file(os.path.join('logging_elk', 'elk_logger.py'))
    story.extend(make_code_box(elk_code))
    story.append(PageBreak())

    # Appendix G: app.py
    story.append(Paragraph("APPENDIX G: FLASK REST API SERVER & WEB DASHBOARD (app.py)", styles['SectionHeader']))
    story.append(Paragraph("Defines REST API endpoints and web routes for interactive analyst workstations and simulator testing:", styles['BodyNoIndent']))
    app_code = read_code_file('app.py')
    story.extend(make_code_box(app_code))
    story.append(PageBreak())

    # Appendix H: test_system.py
    story.append(Paragraph("APPENDIX H: AUTOMATED VERIFICATION TEST SUITE (test_system.py)", styles['SectionHeader']))
    story.append(Paragraph("Executes automated unit and integration tests across data generation, legitimate checkout, and velocity bursts:", styles['BodyNoIndent']))
    test_code = read_code_file('test_system.py')
    story.extend(make_code_box(test_code))
    story.append(PageBreak())

    return story

print("report_extended_appendices.py updated successfully.")
