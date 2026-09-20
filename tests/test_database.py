import sys
import os
import pytest
from datetime import date
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.base import Base
from app.db.init_db import init_db
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.recurring_payment import RecurringPayment
from app.models.budget import Budget
from app.models.goal import FinancialGoal
from app.models.monthly_summary import MonthlySummary


@pytest.fixture
def test_db_session():
    # In-memory SQLite for isolated test execution
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    # Run seed data logic on this test session
    init_db(db_session=session)
    
    yield session
    session.close()


def test_init_db_seeds_default_user_and_categories(test_db_session):
    # Verify default demo user was created
    user = test_db_session.execute(select(User).filter_by(id=1)).scalar_one_or_none()
    assert user is not None
    assert user.name == "Demo User"
    assert user.currency == "USD"

    # Verify categories were seeded
    categories = test_db_session.execute(select(Category)).scalars().all()
    assert len(categories) >= 15
    category_names = {c.name for c in categories}
    assert "Groceries" in category_names
    assert "Salary" in category_names
    assert "Other" in category_names
    assert "Subscription" in category_names


def test_reset_demo_data_clears_financial_records_but_preserves_reference_data(test_db_session):
    from app.db.init_db import reset_demo_data

    groceries = test_db_session.execute(select(Category).filter_by(name="Groceries")).scalar_one()
    test_db_session.add(Transaction(
        user_id=1,
        category_id=groceries.id,
        transaction_date=date(2026, 1, 15),
        description="Test purchase",
        amount_minor=-1200,
        currency="USD",
    ))
    test_db_session.add(FinancialGoal(
        user_id=1,
        name="Test goal",
        target_minor=10000,
        current_minor=1000,
        currency="USD",
    ))
    test_db_session.commit()

    reset_demo_data(test_db_session)

    assert test_db_session.query(Transaction).count() == 0
    assert test_db_session.query(FinancialGoal).count() == 0
    assert test_db_session.execute(select(User).filter_by(id=1)).scalar_one() is not None
    assert test_db_session.execute(select(Category).filter_by(name="Groceries")).scalar_one() is not None


def test_category_unique_name_constraint(test_db_session):
    dup = Category(name="Groceries", kind="expense")
    test_db_session.add(dup)
    with pytest.raises(IntegrityError):
        test_db_session.commit()
    test_db_session.rollback()


def test_transaction_creation_and_relationships(test_db_session):
    groceries = test_db_session.execute(select(Category).filter_by(name="Groceries")).scalar_one()

    tx = Transaction(
        user_id=1,
        category_id=groceries.id,
        transaction_date=date(2026, 1, 15),
        description="Whole Foods Market",
        amount_minor=-4250,  # $42.50 expense
        currency="USD",
        source_file="statement.csv",
        is_recurring_candidate=False,
    )
    test_db_session.add(tx)
    test_db_session.commit()

    loaded = test_db_session.execute(select(Transaction).filter_by(id=tx.id)).scalar_one()
    assert loaded.description == "Whole Foods Market"
    assert loaded.amount_minor == -4250
    assert loaded.user.id == 1
    assert loaded.category.name == "Groceries"


def test_budget_unique_constraint(test_db_session):
    groceries = test_db_session.execute(select(Category).filter_by(name="Groceries")).scalar_one()

    b1 = Budget(
        user_id=1,
        category_id=groceries.id,
        month="2026-01",
        limit_minor=50000,
        currency="USD",
    )
    test_db_session.add(b1)
    test_db_session.commit()

    # Duplicate budget for same user, category, month must fail
    b2 = Budget(
        user_id=1,
        category_id=groceries.id,
        month="2026-01",
        limit_minor=60000,
        currency="USD",
    )
    test_db_session.add(b2)
    with pytest.raises(IntegrityError):
        test_db_session.commit()
    test_db_session.rollback()


def test_recurring_payment_creation(test_db_session):
    sub_cat = test_db_session.execute(select(Category).filter_by(name="Subscription")).scalar_one()

    rp = RecurringPayment(
        user_id=1,
        category_id=sub_cat.id,
        merchant_name="Netflix",
        typical_amount_minor=1599,
        currency="USD",
        frequency="monthly",
        next_expected_date=date(2026, 2, 1),
        confidence=0.95,
        last_seen_date=date(2026, 1, 1),
    )
    test_db_session.add(rp)
    test_db_session.commit()

    loaded = test_db_session.execute(select(RecurringPayment).filter_by(merchant_name="Netflix")).scalar_one()
    assert loaded.typical_amount_minor == 1599
    assert loaded.frequency == "monthly"
    assert loaded.confidence == 0.95


def test_financial_goal_creation(test_db_session):
    goal = FinancialGoal(
        user_id=1,
        name="Emergency Fund",
        target_minor=1000000,  # $10,000.00
        current_minor=250000,   # $2,500.00
        target_date=date(2026, 12, 31),
        currency="USD",
    )
    test_db_session.add(goal)
    test_db_session.commit()

    loaded = test_db_session.execute(select(FinancialGoal).filter_by(name="Emergency Fund")).scalar_one()
    assert loaded.target_minor == 1000000
    assert loaded.current_minor == 250000


def test_monthly_summary_unique_constraint(test_db_session):
    s1 = MonthlySummary(
        user_id=1,
        month="2026-01",
        income_minor=500000,
        expense_minor=210000,
        net_minor=290000,
        transaction_count=45,
    )
    test_db_session.add(s1)
    test_db_session.commit()

    s2 = MonthlySummary(
        user_id=1,
        month="2026-01",
        income_minor=500000,
        expense_minor=210000,
        net_minor=290000,
        transaction_count=45,
    )
    test_db_session.add(s2)
    with pytest.raises(IntegrityError):
        test_db_session.commit()
    test_db_session.rollback()
