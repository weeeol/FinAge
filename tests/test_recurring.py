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
from app.services.recurring_service import clean_merchant_name

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


def test_clean_merchant_name():
    assert clean_merchant_name("NETFLIX.COM SUBSCRIPTION") == "Netflix"
    assert clean_merchant_name("POS DEBIT SPOTIFY USA *9876") == "Spotify Usa"
    assert clean_merchant_name("UBER TRIP HELP.UBER.COM") == "Uber Trip"
    assert clean_merchant_name("Chevron Gas Station #1234") == "Chevron Gas Station"


def test_recurring_empty_db(client):
    res = client.get("/api/analytics/recurring")
    assert res.status_code == 200
    assert res.json() == {"items": []}


def test_detect_monthly_recurring_subscription(client, db_session):
    sub_cat = db_session.query(Category).filter_by(name="Subscription").first()

    # Netflix monthly payments on the 5th of Jan, Feb, Mar 2026
    txns = [
        Transaction(user_id=1, category_id=sub_cat.id, transaction_date=date(2026, 1, 5), description="Netflix.com Subscription", amount_minor=-1599),
        Transaction(user_id=1, category_id=sub_cat.id, transaction_date=date(2026, 2, 5), description="Netflix.com Subscription", amount_minor=-1599),
        Transaction(user_id=1, category_id=sub_cat.id, transaction_date=date(2026, 3, 5), description="Netflix.com Subscription", amount_minor=-1599),
        # Irregular gas station visits
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 1, 3), description="Chevron Gas Station", amount_minor=-4500),
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 1, 14), description="Chevron Gas Station", amount_minor=-3200),
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 3, 20), description="Chevron Gas Station", amount_minor=-5100),
    ]
    db_session.add_all(txns)
    db_session.commit()

    res = client.get("/api/analytics/recurring")
    assert res.status_code == 200
    items = res.json()["items"]

    # Netflix must be detected as monthly subscription
    netflix_items = [i for i in items if "Netflix" in i["merchant_name"]]
    assert len(netflix_items) == 1
    netflix = netflix_items[0]
    assert netflix["typical_amount_minor"] == 1599
    assert netflix["frequency"] == "monthly"
    assert netflix["confidence"] >= 0.85
    assert netflix["next_expected_date"] == "2026-04-05"

    # Irregular Chevron gas should NOT be classified as recurring subscription
    chevron_items = [i for i in items if "Chevron" in i["merchant_name"]]
    assert len(chevron_items) == 0


def test_detect_weekly_recurring_obligation(client, db_session):
    txns = [
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 1, 1), description="Weekly Meal Prep Service", amount_minor=-6500),
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 1, 8), description="Weekly Meal Prep Service", amount_minor=-6500),
        Transaction(user_id=1, category_id=None, transaction_date=date(2026, 1, 15), description="Weekly Meal Prep Service", amount_minor=-6500),
    ]
    db_session.add_all(txns)
    db_session.commit()

    res = client.get("/api/analytics/recurring")
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) == 1
    meal_prep = items[0]
    assert meal_prep["frequency"] == "weekly"
    assert meal_prep["typical_amount_minor"] == 6500
    assert meal_prep["confidence"] >= 0.85
    assert meal_prep["next_expected_date"] == "2026-01-22"
