import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import fitz
import pytest

from app.processing.parser import parse_statement_file
from app.services.pdf_parser import parse_pdf_statement


def create_text_pdf_bytes(lines):
    doc = fitz.open()
    page = doc.new_page()
    text = "\n".join(lines)
    page.insert_text((72, 72), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_blank_pdf_bytes():
    doc = fitz.open()
    page = doc.new_page()
    # Intentionally leave the page blank to simulate an image-only / unreadable PDF.
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_parse_pdf_statement_extracts_text_entries():
    pdf_bytes = create_text_pdf_bytes([
        "2026-01-05 Grocery Market -42.50",
        "2026-01-07 Salary 1500.00",
    ])

    df = parse_pdf_statement(pdf_bytes)

    assert len(df) == 2
    assert df.iloc[0]["Date"] == "2026-01-05"
    assert df.iloc[0]["Description"] == "Grocery Market"
    assert df.iloc[0]["Amount"] == -42.5
    assert df.iloc[1]["Date"] == "2026-01-07"
    assert df.iloc[1]["Description"] == "Salary"
    assert df.iloc[1]["Amount"] == 1500.0


def test_parse_statement_file_rejects_image_only_pdf():
    blank_pdf = create_blank_pdf_bytes()

    with pytest.raises(ValueError, match="no readable text|image-only|unsupported"):
        parse_statement_file(blank_pdf, "blank.pdf")
