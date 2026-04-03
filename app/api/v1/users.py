from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.middleware.rbac import require_role
from app.models.user import UserRole

router = APIRouter()

@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    if service.is_bootstrap():
        return service.create_user(data)
    require_role(UserRole.admin)(request)
    return service.create_user(data, caller_role=request.state.user_role)

@router.get("", response_model=list[UserResponse])
def list_users(request: Request, db: Session = Depends(get_db)):
    require_role(UserRole.viewer)(request)
    return UserService(db).get_users()

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, request: Request, db: Session = Depends(get_db)):
    require_role(UserRole.admin)(request)
    return UserService(db).update_user(user_id, data)
