import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Tuple, List
import pandas as pd


@dataclass
class NormalizedTransaction:
    transaction_date: date
    description: str
    amount_minor: int  # positive = income, negative = expense
    currency: str = "INR"
    source_file: Optional[str] = None
    external_id: Optional[str] = None
    category_name: Optional[str] = None


DATE_COLUMN_CANDIDATES = [
    "date", "transaction date", "transaction_date", "txn date", "txn_date",
    "trans date", "posting date", "posted date", "value date", "booking date"
]

DESCRIPTION_COLUMN_CANDIDATES = [
    "description", "details", "narrative", "narration", "transaction details",
    "transaction_details", "merchant", "payee", "particulars", "memo", "name"
]

AMOUNT_COLUMN_CANDIDATES = [
    "amount", "transaction amount", "transaction_amount", "txn amount", "txn_amount",
    "total", "net amount", "net_amount"
]

DEBIT_COLUMN_CANDIDATES = [
    "debit", "withdrawal", "withdrawals", "spent", "dr", "debit amount", "debit_amount"
]

CREDIT_COLUMN_CANDIDATES = [
    "credit", "deposit", "deposits", "received", "cr", "credit amount", "credit_amount"
]

TYPE_COLUMN_CANDIDATES = [
    "type", "transaction type", "transaction_type", "txn type", "cr/dr", "dr/cr"
]

CATEGORY_COLUMN_CANDIDATES = [
    "category", "category name", "category_name"
]


def clean_column_name(col: str) -> str:
    return re.sub(r"[_\s\-]+", " ", str(col).strip().lower())


def parse_date_value(val) -> Optional[date]:
    if val is None or pd.isna(val):
        return None
    if isinstance(val, (datetime, pd.Timestamp)):
        return val.date()
    if isinstance(val, date):
        return val

    s = str(val).strip()
    if not s:
        return None

    # Try standard formats
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%b %d, %Y", "%d %b %Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass

    # Fallback to pandas date parser
    try:
        dt = pd.to_datetime(s)
        return dt.date()
    except Exception:
        return None


def parse_amount_value(val) -> Optional[int]:
    """
    Parses an amount string/float/int into minor units (integer cents).
    Handles currency symbols, commas, and parentheses for negative values.
    """
    if val is None or pd.isna(val):
        return None

    if isinstance(val, (int, float)):
        return int(round(val * 100))

    s = str(val).strip()
    if not s:
        return None

    is_negative = False
    # Check for parentheses: (123.45)
    if s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1]
    elif s.startswith("-"):
        is_negative = True
        s = s[1:]
    elif s.endswith("-"):
        is_negative = True
        s = s[:-1]

    # Remove currency symbols and formatting commas
    s = re.sub(r"[^\d.]", "", s)
    if not s:
        return None

    try:
        float_val = float(s)
        cents = int(round(float_val * 100))
        return -cents if is_negative else cents
    except ValueError:
        return None


def detect_columns(columns: List[str]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Returns (date_col, desc_col, amount_col, debit_col, credit_col, type_col, cat_col)
    """
    cleaned_map = {col: clean_column_name(col) for col in columns}

    date_col = None
    desc_col = None
    amount_col = None
    debit_col = None
    credit_col = None
    type_col = None
    cat_col = None

    for col, clean in cleaned_map.items():
        if not date_col and clean in DATE_COLUMN_CANDIDATES:
            date_col = col
        elif not desc_col and clean in DESCRIPTION_COLUMN_CANDIDATES:
            desc_col = col
        elif not amount_col and clean in AMOUNT_COLUMN_CANDIDATES:
            amount_col = col
        elif not debit_col and clean in DEBIT_COLUMN_CANDIDATES:
            debit_col = col
        elif not credit_col and clean in CREDIT_COLUMN_CANDIDATES:
            credit_col = col
        elif not type_col and clean in TYPE_COLUMN_CANDIDATES:
            type_col = col
        elif not cat_col and clean in CATEGORY_COLUMN_CANDIDATES:
            cat_col = col

    return date_col, desc_col, amount_col, debit_col, credit_col, type_col, cat_col
