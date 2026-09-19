import io
from typing import List, Tuple
import pandas as pd

from app.processing.normalizer import (
    NormalizedTransaction,
    detect_columns,
    parse_date_value,
    parse_amount_value,
    clean_column_name,
)
from app.processing.categorizer import categorize_description


def parse_statement_file(content: bytes, filename: str) -> Tuple[List[NormalizedTransaction], List[str]]:
    """
    Parses CSV or XLSX bytes and returns a tuple of (normalized_transactions, warnings).
    """
    filename_lower = filename.lower()
    df = None
    warnings: List[str] = []

    if filename_lower.endswith(".csv"):
        # Try multiple delimiters and encodings
        encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
        delimiters = [",", ";", "\t"]
        loaded = False

        for enc in encodings:
            if loaded:
                break
            for sep in delimiters:
                try:
                    df = pd.read_csv(io.BytesIO(content), sep=sep, encoding=enc)
                    if len(df.columns) >= 2:
                        loaded = True
                        break
                except Exception:
                    continue

        if not loaded or df is None:
            raise ValueError("Unable to read CSV file. Please verify delimiter and encoding.")

    elif filename_lower.endswith((".xlsx", ".xls")):
        try:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        except Exception as e:
            raise ValueError(f"Unable to read Excel file: {str(e)}")
    else:
        raise ValueError(f"Unsupported file format for: {filename}. Expected .csv or .xlsx.")

    if df.empty:
        return [], ["File contains no data rows."]

    # Detect mapped columns
    col_names = [str(c) for c in df.columns]
    date_col, desc_col, amount_col, debit_col, credit_col, type_col, cat_col = detect_columns(col_names)

    if not date_col:
        raise ValueError(f"Could not identify a Date column. Found columns: {col_names}")
    if not desc_col:
        raise ValueError(f"Could not identify a Description column. Found columns: {col_names}")
    if not amount_col and not (debit_col or credit_col):
        raise ValueError(f"Could not identify Amount or Debit/Credit columns. Found columns: {col_names}")

    normalized: List[NormalizedTransaction] = []

    for idx, row in df.iterrows():
        row_num = idx + 2  # 1-indexed plus header

        # Parse date
        raw_date = row[date_col]
        txn_date = parse_date_value(raw_date)
        if not txn_date:
            warnings.append(f"Row {row_num}: Invalid or missing date '{raw_date}'. Row skipped.")
            continue

        # Parse description
        raw_desc = str(row[desc_col]).strip() if pd.notna(row[desc_col]) else ""
        if not raw_desc or raw_desc.lower() in ("nan", "none", "null"):
            warnings.append(f"Row {row_num}: Missing description. Row skipped.")
            continue

        # Parse amount
        amount_minor = 0
        if amount_col and pd.notna(row.get(amount_col)):
            val = parse_amount_value(row[amount_col])
            if val is None:
                warnings.append(f"Row {row_num}: Invalid amount '{row[amount_col]}'. Row skipped.")
                continue

            # Check if there is an explicit type column indicating debit/credit
            if type_col and pd.notna(row.get(type_col)):
                t_val = str(row[type_col]).strip().lower()
                if t_val in ("debit", "dr", "expense", "withdrawal", "spent"):
                    amount_minor = -abs(val)
                elif t_val in ("credit", "cr", "income", "deposit", "received"):
                    amount_minor = abs(val)
                else:
                    amount_minor = val
            else:
                amount_minor = val

        elif debit_col or credit_col:
            # Separate Debit and Credit columns
            debit_val = parse_amount_value(row.get(debit_col)) if debit_col and pd.notna(row.get(debit_col)) else None
            credit_val = parse_amount_value(row.get(credit_col)) if credit_col and pd.notna(row.get(credit_col)) else None

            if debit_val is not None and debit_val != 0:
                amount_minor = -abs(debit_val)
            elif credit_val is not None and credit_val != 0:
                amount_minor = abs(credit_val)
            else:
                warnings.append(f"Row {row_num}: Both debit and credit are empty or zero. Row skipped.")
                continue
        else:
            warnings.append(f"Row {row_num}: No amount found. Row skipped.")
            continue

        # Extract explicit category if provided in statement
        explicit_cat = str(row[cat_col]).strip() if cat_col and pd.notna(row.get(cat_col)) else None
        assigned_category = categorize_description(raw_desc, explicit_category=explicit_cat)

        normalized.append(
            NormalizedTransaction(
                transaction_date=txn_date,
                description=raw_desc,
                amount_minor=amount_minor,
                currency="USD",
                source_file=filename,
                category_name=assigned_category,
            )
        )

    return normalized, warnings
