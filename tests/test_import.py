import sys
import os
import io
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import get_db
from app.main import app

# Create in-memory test database with StaticPool and check_same_thread=False
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    init_db(db_session=session)
    session.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_upload_standard_csv(client):
    csv_content = """Date,Description,Amount
2026-01-10,Netflix subscription,-15.99
2026-01-11,Swiggy food delivery,-24.50
2026-01-12,Uber ride,-18.20
2026-01-15,Acme Corp Payroll,3500.00
2026-01-16,Random Unknown Store,-12.00
"""
    files = {"file": ("statement.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 5
    assert data["skipped"] == 0
    # Netflix(Subscription), Swiggy(Dining & Food), Uber(Transport), Payroll(Salary) = 4 categorized
    assert data["categories_assigned"] == 4
    assert len(data["warnings"]) == 0


def test_upload_debit_credit_csv(client):
    csv_content = """Txn Date,Details,Debit,Credit
2026-02-01,Whole Foods Market,85.20,
2026-02-02,Client Invoice,,500.00
"""
    files = {"file": ("bank_stmt.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 2
    assert data["skipped"] == 0
    assert data["categories_assigned"] >= 1  # Whole Foods is Groceries


def test_duplicate_upload_prevention(client):
    csv_content = """Date,Description,Amount
2026-03-01,Amazon Shopping,-45.00
2026-03-02,Starbucks Coffee,-6.50
"""
    files = {"file": ("shopping.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    # First upload
    res1 = client.post("/api/upload", files=files)
    assert res1.status_code == 201
    assert res1.json()["imported"] == 2

    # Duplicate upload with same file content
    files = {"file": ("shopping.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    res2 = client.post("/api/upload", files=files)
    assert res2.status_code == 201
    data2 = res2.json()
    assert data2["imported"] == 0
    assert data2["skipped"] == 2
    assert any("Skipped duplicate" in w for w in data2["warnings"])


def test_upload_with_malformed_rows_handled_gracefully(client):
    csv_content = """Date,Description,Amount
2026-04-01,Target,-30.00
INVALID_DATE,Broken Row,-10.00
2026-04-03,, -5.00
2026-04-04,Valid Row,100.00
"""
    files = {"file": ("partial_bad.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 2
    assert data["skipped"] >= 2
    assert len(data["warnings"]) >= 2


def test_upload_excel_file(client):
    df = pd.DataFrame([
        {"Date": "2026-05-01", "Description": "Spotify", "Amount": -9.99},
        {"Date": "2026-05-02", "Description": "Trader Joe's", "Amount": -42.10},
    ])
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    files = {"file": ("statement.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 2
    assert data["categories_assigned"] == 2  # Spotify and Trader Joe's


def test_upload_unsupported_file_extension(client):
    files = {"file": ("script.exe", io.BytesIO(b"binary data"), "application/octet-stream")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert "Unsupported file format" in data["error"]["message"]


def test_upload_empty_file(client):
    files = {"file": ("empty.csv", io.BytesIO(b""), "text/csv")}
    response = client.post("/api/upload", files=files)

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "empty" in data["error"]["message"]


def test_categorizer_rules():
    from app.processing.categorizer import categorize_description

    assert categorize_description("SWIGGY BANGALORE IN") == "Dining & Food"
    assert categorize_description("ZOMATO ORDER #1234") == "Dining & Food"
    assert categorize_description("NETFLIX.COM PAYMENT") == "Subscription"
    assert categorize_description("SPOTIFY AB") == "Subscription"
    assert categorize_description("UBER TRIP HELP.UBER.COM") == "Transport"
    assert categorize_description("AMAZON RETAIL PURCHASE") == "Shopping"
    assert categorize_description("TOTALLY RANDOM VENDOR XYZ") == "Other"

