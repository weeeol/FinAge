import sys
import os
import pytest
from datetime import date
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.models.category import Category
from app.models.transaction import Transaction

def test_create_budget(client: TestClient):
    response = client.post("/api/budgets", json={
        "category": "Entertainment",
        "month": "2026-10",
        "limit_minor": 10000,
        "currency": "USD"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Entertainment"
    assert data["limit_minor"] == 10000

def test_create_duplicate_budget(client: TestClient):
    client.post("/api/budgets", json={
        "category": "Dining",
        "month": "2026-11",
        "limit_minor": 5000,
        "currency": "USD"
    })
    response = client.post("/api/budgets", json={
        "category": "Dining",
        "month": "2026-11",
        "limit_minor": 8000,
        "currency": "USD"
    })
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "duplicate_budget"

def test_get_budget_status(client: TestClient, db_session):
    client.post("/api/budgets", json={
        "category": "Utilities",
        "month": "2026-12",
        "limit_minor": 20000,
        "currency": "USD"
    })
    
    cat = db_session.query(Category).filter_by(name="Utilities").first()
    t1 = Transaction(
        user_id=1,
        category_id=cat.id,
        transaction_date=date(2026, 12, 5),
        description="Electric",
        amount_minor=-15000,
        currency="USD"
    )
    db_session.add(t1)
    db_session.commit()
    
    response = client.get("/api/analytics/budgets?month=2026-12")
    assert response.status_code == 200
    data = response.json()
    
    budget_status = next(b for b in data["items"] if b["category"] == "Utilities")
    assert budget_status["limit_minor"] == 20000
    assert budget_status["spent_minor"] == 15000
    assert budget_status["remaining_minor"] == 5000
    assert budget_status["percent_used"] == 0.75
    assert budget_status["status"] == "on_track"


def test_delete_budget(client: TestClient):
    response = client.post("/api/budgets", json={
        "category": "Travel",
        "month": "2026-09",
        "limit_minor": 30000,
        "currency": "USD"
    })
    budget_id = response.json()["id"]

    delete_response = client.delete(f"/api/budgets/{budget_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True
    assert delete_response.json()["id"] == budget_id

    follow_up = client.get("/api/analytics/budgets?month=2026-09")
    assert follow_up.status_code == 200
    assert all(item["budget_id"] != budget_id for item in follow_up.json()["items"])
