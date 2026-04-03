from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService
from app.middleware.rbac import require_role
from app.models.user import UserRole

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(request: Request, db: Session = Depends(get_db), _=Depends(require_role(UserRole.analyst))):
    return DashboardService(db).get_summary()
