import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import pytest
from fastapi.testclient import TestClient
from datetime import date
from app.models.category import Category
from app.models.transaction import Transaction

def test_get_monthly_summary(client: TestClient, db_session):
    cat = Category(name="Dining", kind="expense")
    db_session.add(cat)
    db_session.commit()
    
    t1 = Transaction(
        user_id=1,
        category_id=cat.id,
        transaction_date=date(2026, 1, 5),
        description="Restaurant A",
        amount_minor=-5000,
        currency="USD"
    )
    t2 = Transaction(
        user_id=1,
        category_id=cat.id,
        transaction_date=date(2026, 1, 10),
        description="Salary",
        amount_minor=100000,
        currency="USD"
    )
    # Large expense to trigger anomaly rule
    t3 = Transaction(
        user_id=1,
        category_id=cat.id,
        transaction_date=date(2026, 1, 15),
        description="Very Large Expense",
        amount_minor=-50000, 
        currency="USD"
    )
    db_session.add_all([t1, t2, t3])
    db_session.commit()

    response = client.get("/api/monthly-summary?month=2026-01")
    assert response.status_code == 200
    data = response.json()
    
    assert data["month"] == "2026-01"
    assert data["income_minor"] == 100000
    assert data["expense_minor"] == 55000
    assert data["net_minor"] == 45000
    
    assert len(data["top_categories"]) > 0
    assert data["top_categories"][0]["category"] == "Dining"
    assert data["top_categories"][0]["amount_minor"] == 55000
    
    # Check insight generation (Rule 2: Large transaction > 30% of total outflow)
    # Total outflow = 55000. 30% is 16500. t3 is 50000, which is > 16500.
    assert len(data["insights"]) >= 1
    anomaly_insight = next((i for i in data["insights"] if i["type"] == "anomaly"), None)
    assert anomaly_insight is not None
    assert anomaly_insight["severity"] == "warning"
