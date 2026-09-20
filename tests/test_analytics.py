import sys
import os
from datetime import date
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import get_db
from app.models.category import Category
from app.models.transaction import Transaction
from app.main import app

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    init_db(db_session=session)
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def seed_test_transactions(db_session):
    groceries = db_session.query(Category).filter_by(name="Groceries").first()
    dining = db_session.query(Category).filter_by(name="Dining & Food").first()
    salary = db_session.query(Category).filter_by(name="Salary").first()

    txns = [
        # January 2026
        Transaction(user_id=1, category_id=salary.id, transaction_date=date(2026, 1, 1), description="Salary", amount_minor=500000),
        Transaction(user_id=1, category_id=groceries.id, transaction_date=date(2026, 1, 5), description="Market", amount_minor=-5000),
        Transaction(user_id=1, category_id=dining.id, transaction_date=date(2026, 1, 10), description="Burger Place", amount_minor=-2500),
        Transaction(user_id=1, category_id=groceries.id, transaction_date=date(2026, 1, 15), description="Supermarket", amount_minor=-2500),
        # February 2026
        Transaction(user_id=1, category_id=salary.id, transaction_date=date(2026, 2, 1), description="Salary", amount_minor=500000),
        Transaction(user_id=1, category_id=groceries.id, transaction_date=date(2026, 2, 10), description="Grocery Store", amount_minor=-10000),
    ]
    db_session.add_all(txns)
    db_session.commit()


def test_transactions_summary_empty_db(client):
    response = client.get("/api/transactions/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["income_minor"] == 0
    assert data["expense_minor"] == 0
    assert data["net_minor"] == 0
    assert data["transaction_count"] == 0
    assert data["currency"] == "INR"


def test_transactions_list_and_summary_with_data(client, db_session):
    seed_test_transactions(db_session)

    # Test summary
    res_summary = client.get("/api/transactions/summary")
    assert res_summary.status_code == 200
    s_data = res_summary.json()
    assert s_data["income_minor"] == 1000000  # 500k * 2
    assert s_data["expense_minor"] == 20000   # 5k + 2.5k + 2.5k + 10k
    assert s_data["net_minor"] == 980000
    assert s_data["transaction_count"] == 6

    # Test list pagination
    res_list = client.get("/api/transactions?page=1&page_size=3")
    assert res_list.status_code == 200
    l_data = res_list.json()
    assert len(l_data["items"]) == 3
    assert l_data["total"] == 6
    assert l_data["page"] == 1
    assert l_data["page_size"] == 3

    # Test category filter
    res_cat = client.get("/api/transactions?category=Dining %26 Food")
    assert res_cat.status_code == 200
    assert res_cat.json()["total"] == 1
    assert res_cat.json()["items"][0]["description"] == "Burger Place"

    # Test date range filter
    res_date = client.get("/api/transactions?from_date=2026-02-01&to_date=2026-02-28")
    assert res_date.status_code == 200
    assert res_date.json()["total"] == 2


def test_monthly_analytics(client, db_session):
    seed_test_transactions(db_session)

    response = client.get("/api/analytics/monthly?months=6")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2

    jan = data["items"][0]
    assert jan["month"] == "2026-01"
    assert jan["income_minor"] == 500000
    assert jan["expense_minor"] == 10000  # 5000 + 2500 + 2500
    assert jan["net_minor"] == 490000

    feb = data["items"][1]
    assert feb["month"] == "2026-02"
    assert feb["income_minor"] == 500000
    assert feb["expense_minor"] == 10000
    assert feb["net_minor"] == 490000


def test_category_analytics(client, db_session):
    seed_test_transactions(db_session)

    # Total across all months: Groceries: 17500 (87.5%), Dining: 2500 (12.5%)
    res_all = client.get("/api/analytics/categories")
    assert res_all.status_code == 200
    items = res_all.json()["items"]
    assert len(items) == 2
    assert items[0]["category"] == "Groceries"
    assert items[0]["amount_minor"] == 17500
    assert items[0]["transaction_count"] == 3
    assert items[0]["share"] == 0.875

    assert items[1]["category"] == "Dining & Food"
    assert items[1]["amount_minor"] == 2500
    assert items[1]["share"] == 0.125

    # Filtered by January 2026: Groceries: 7500 (75%), Dining: 2500 (25%)
    res_jan = client.get("/api/analytics/categories?month=2026-01")
    assert res_jan.status_code == 200
    jan_items = res_jan.json()["items"]
    assert len(jan_items) == 2
    assert jan_items[0]["category"] == "Groceries"
    assert jan_items[0]["amount_minor"] == 7500
    assert jan_items[0]["share"] == 0.75

    assert jan_items[1]["category"] == "Dining & Food"
    assert jan_items[1]["amount_minor"] == 2500
    assert jan_items[1]["share"] == 0.25
