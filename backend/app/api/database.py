from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.init_db import reset_demo_data
from app.db.session import get_db


router = APIRouter(tags=["Database"])


@router.post("/reset-database")
def reset_database(db: Session = Depends(get_db)):
    reset_demo_data(db)
    return {"status": "ok", "message": "Demo financial data was reset."}