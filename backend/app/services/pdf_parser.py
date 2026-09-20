import re

import fitz
import pandas as pd


def _parse_pdf_line(line: str):
    text = line.strip()
    if not text:
        return None

    date_pattern = r"(?P<date>\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})"
    amount_pattern = r"(?P<amount>[-+]?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})|[-+]?\$?\d+(?:\.\d{2}))"
    pattern = re.compile(rf"^\s*{date_pattern}\s+(?P<description>.+?)\s+(?:{amount_pattern})\s*$")

    match = pattern.match(text)
    if not match:
        return None

    date_str = match.group("date")
    description = match.group("description").strip()
    amount_str = match.group("amount").replace("$", "").replace(",", "")

    try:
        amount = float(amount_str)
    except ValueError:
        return None

    if not description:
        return None

    return {"Date": date_str, "Description": description, "Amount": amount}


def parse_pdf_statement(file_bytes: bytes) -> pd.DataFrame:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError(f"Unable to open PDF file: {exc}") from exc

    parsed_data = []
    extracted_text = []

    try:
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                extracted_text.extend(page_text.splitlines())
    finally:
        doc.close()

    if not extracted_text:
        raise ValueError("PDF contains no readable text and appears to be image-only or unsupported.")

    for line in extracted_text:
        parsed = _parse_pdf_line(line)
        if parsed:
            parsed_data.append(parsed)

    if not parsed_data:
        raise ValueError("PDF contains no recognizable transaction rows; the layout appears unsupported for automatic parsing.")

    return pd.DataFrame(parsed_data, columns=["Date", "Description", "Amount"])
