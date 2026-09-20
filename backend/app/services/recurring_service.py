import re
import statistics
from datetime import date, timedelta
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from app.models.transaction import Transaction
from app.models.recurring_payment import RecurringPayment
from app.schemas.analytics import RecurringPaymentItem, RecurringAnalyticsResponse


def clean_merchant_name(description: str) -> str:
    """
    Cleans raw transaction descriptions into identifiable merchant names.
    Removes transaction noise, URLs, card numbers, and timestamps.
    """
    s = description.strip()

    # Remove domain prefixes like help. or www.
    s = re.sub(r"\b(help|www|api|pay|m)\.", " ", s, flags=re.IGNORECASE)

    # Remove domain suffixes like .com, .net, .org, .co, etc.
    s = re.sub(r"\.(com|net|org|io|in|co|us|gov|edu)\b", " ", s, flags=re.IGNORECASE)

    # Remove common noise words
    noise_patterns = [
        r"\bpos\s*debit\b", r"\bach\b", r"\brecurring\b", r"\bsubscription\b",
        r"\bautopay\b", r"\bdirect\s*debit\b", r"\bpayment\b", r"\bbill\b",
        r"\bcard\s*purchase\b", r"\bfee\b", r"\border\b"
    ]
    for pat in noise_patterns:
        s = re.sub(pat, " ", s, flags=re.IGNORECASE)

    # Remove card numbers, IDs and hashes (e.g. *1234, #9876, 12345678)
    s = re.sub(r"[\*#]\w+", " ", s)
    s = re.sub(r"\b\d{4,}\b", " ", s)

    # Remove trailing/leading punctuation and excess spaces
    s = re.sub(r"[^\w\s&]", " ", s)

    # Deduplicate repeated adjacent or consecutive words (e.g. "Uber Trip Uber" -> "Uber Trip")
    words = []
    seen = set()
    for w in s.split():
        lw = w.lower()
        if lw not in seen:
            words.append(w)
            seen.add(lw)
    s = " ".join(words).strip()

    if not s:
        return description.strip().title()

    # Return Title Cased clean merchant
    return s.title()

    # Return Title Cased clean merchant
    return s.title()


def add_month_to_date(d: date) -> date:
    """Calculates roughly the same day in the next month."""
    year = d.year + (d.month // 12)
    month = (d.month % 12) + 1
    day = min(d.day, 28)  # Safe day for all months
    return date(year, month, day)


class RecurringService:
    def __init__(self, db: Session):
        self.db = db

    def detect_and_sync_recurring(self, user_id: int = 1) -> RecurringAnalyticsResponse:
        # 1. Fetch all expense transactions for the user
        txns = (
            self.db.execute(
                select(Transaction)
                .filter(Transaction.user_id == user_id, Transaction.amount_minor < 0)
                .order_by(Transaction.transaction_date.asc())
            )
            .scalars()
            .all()
        )

        # 2. Group transactions by clean merchant name
        grouped: Dict[str, List[Transaction]] = defaultdict(list)
        for t in txns:
            merchant = clean_merchant_name(t.description)
            grouped[merchant].append(t)

        detected_items: List[RecurringPaymentItem] = []
        db_records: List[RecurringPayment] = []

        # 3. Analyze each merchant group with >= 2 occurrences
        for merchant, items in grouped.items():
            if len(items) < 2:
                continue

            # Sort strictly by date
            items.sort(key=lambda x: x.transaction_date)
            dates = [t.transaction_date for t in items]
            amounts = [abs(t.amount_minor) for t in items]

            # Calculate intervals
            intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
            if not intervals:
                continue

            avg_interval = statistics.mean(intervals)
            std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0.0

            # Check amount consistency
            median_amount = int(statistics.median(amounts))
            all_exact_amount = all(a == amounts[0] for a in amounts)
            amount_variation = (max(amounts) - min(amounts)) / median_amount if median_amount > 0 else 0

            frequency = "unknown"
            confidence = 0.50
            next_date: Optional[date] = None
            last_date = dates[-1]

            # Heuristics for Monthly (~30 days, tolerance 24-35)
            if 24 <= avg_interval <= 35:
                frequency = "monthly"
                base = 0.75
                if len(items) >= 3:
                    base += 0.12
                if all_exact_amount:
                    base += 0.10
                elif amount_variation <= 0.05:
                    base += 0.05
                if std_interval <= 4:
                    base += 0.05
                confidence = min(0.99, round(base, 2))
                next_date = add_month_to_date(last_date)

            # Heuristics for Weekly (~7 days, tolerance 5-9)
            elif 5 <= avg_interval <= 9:
                frequency = "weekly"
                base = 0.70
                if len(items) >= 3:
                    base += 0.15
                if all_exact_amount:
                    base += 0.10
                confidence = min(0.98, round(base, 2))
                next_date = last_date + timedelta(days=7)

            # Heuristics for Annual (~365 days, tolerance 340-380)
            elif 340 <= avg_interval <= 380:
                frequency = "annual"
                base = 0.80
                if all_exact_amount:
                    base += 0.15
                confidence = min(0.95, round(base, 2))
                try:
                    next_date = date(last_date.year + 1, last_date.month, last_date.day)
                except ValueError:
                    next_date = last_date + timedelta(days=365)

            # Only accept high-confidence detected recurring payments
            if frequency != "unknown" and confidence >= 0.65 and next_date is not None:
                detected_items.append(
                    RecurringPaymentItem(
                        merchant_name=merchant,
                        typical_amount_minor=median_amount,
                        frequency=frequency,
                        next_expected_date=next_date.isoformat(),
                        confidence=confidence,
                    )
                )

                # Prepare DB record
                cat_id = items[-1].category_id  # latest category
                db_records.append(
                    RecurringPayment(
                        user_id=user_id,
                        category_id=cat_id,
                        merchant_name=merchant,
                        typical_amount_minor=median_amount,
                        currency="INR",
                        frequency=frequency,
                        next_expected_date=next_date,
                        confidence=confidence,
                        last_seen_date=last_date,
                    )
                )

        # 4. Sync detected obligations with database table
        if db_records:
            # Clear previous detected items for user and refresh with updated analytics
            self.db.execute(delete(RecurringPayment).filter(RecurringPayment.user_id == user_id))
            self.db.add_all(db_records)
            self.db.commit()

        # Sort items: highest typical amount first
        detected_items.sort(key=lambda x: x.typical_amount_minor, reverse=True)

        return RecurringAnalyticsResponse(items=detected_items)
