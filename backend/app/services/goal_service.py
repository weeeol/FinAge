from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.goal import FinancialGoal
from app.schemas.goal import GoalCreate

class GoalService:
    def __init__(self, db: Session):
        self.db = db

    def create_goal(self, user_id: int, data: GoalCreate) -> FinancialGoal:
        if data.target_minor <= 0:
            exc = HTTPException(status_code=400, detail="Target amount must be greater than zero.")
            exc.code = "validation_error"
            raise exc

        goal = FinancialGoal(
            user_id=user_id,
            name=data.name,
            target_minor=data.target_minor,
            current_minor=data.current_minor,
            target_date=data.target_date,
            currency=data.currency,
        )
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def get_goals(self, user_id: int) -> List[dict]:
        goals = self.db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).all()
        result = []
        for goal in goals:
            progress = round(min(max(goal.current_minor / goal.target_minor, 0.0), 1.0), 4)
            result.append({
                "id": goal.id,
                "name": goal.name,
                "target_minor": goal.target_minor,
                "current_minor": goal.current_minor,
                "target_date": goal.target_date,
                "progress": progress,
                "currency": goal.currency,
                "created_at": goal.created_at,
            })
        return result
