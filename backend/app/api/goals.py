from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.goal import GoalCreate, GoalResponse, GoalList
from app.services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("", response_model=GoalResponse, status_code=201)
def create_goal(data: GoalCreate, db: Session = Depends(get_db)):
    service = GoalService(db)
    goal = service.create_goal(user_id=1, data=data)
    
    progress = round(min(max(goal.current_minor / goal.target_minor, 0.0), 1.0), 4)
    
    return {
        "id": goal.id,
        "name": goal.name,
        "target_minor": goal.target_minor,
        "current_minor": goal.current_minor,
        "target_date": goal.target_date,
        "progress": progress,
        "currency": goal.currency,
        "created_at": goal.created_at
    }

@router.get("", response_model=GoalList)
def get_goals(db: Session = Depends(get_db)):
    service = GoalService(db)
    goals = service.get_goals(user_id=1)
    return GoalList(items=goals)

@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    service = GoalService(db)
    deleted_id = service.delete_goal(user_id=1, goal_id=goal_id)
    return {"deleted": True, "id": deleted_id}
