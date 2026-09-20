import fitz
import pandas as pd
import re

def parse_pdf_statement(file_bytes: bytes) -> pd.DataFrame:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    lines = []
    for page in doc:
        text = page.get_text("text")
        lines.extend(text.split("\n"))

    date_pattern = r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})"
    amount_pattern = r"(-?\$?\d+,\d{3}\.\d{2}|-?\$?\d+\.\d{2})"
    pattern = re.compile(rf"^\s*{date_pattern}\s+(.+?)\s+{amount_pattern}\s*$")
    
    parsed_data = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = pattern.match(line)
        if match:
            date_str = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3).replace('$', '').replace(',', '')
            
            try:
                amount = float(amount_str)
                parsed_data.append({
                    "Date": date_str,
                    "Description": description,
                    "Amount": amount
                })
            except ValueError:
                pass

    return pd.DataFrame(parsed_data, columns=["Date", "Description", "Amount"])
