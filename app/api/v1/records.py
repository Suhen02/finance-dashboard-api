from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.services.record_service import RecordService
from app.middleware.rbac import require_role
from app.models.user import UserRole
from app.models.record import RecordType
from typing import Optional
from datetime import date

router = APIRouter()

@router.post("", response_model=RecordResponse, status_code=201)
def create_record(data: RecordCreate, request: Request, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    return RecordService(db).create_record(data, user_id=request.state.user_id)

@router.get("", response_model=list[RecordResponse])
def list_records(
    request: Request, db: Session = Depends(get_db),
    _=Depends(require_role(UserRole.viewer)),
    skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    type: Optional[RecordType] = None,
    start_date: Optional[date] = None, end_date: Optional[date] = None,
):
    return RecordService(db).get_records(skip, limit, category, type, start_date, end_date)

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(record_id: int, request: Request, db: Session = Depends(get_db), _=Depends(require_role(UserRole.viewer))):
    return RecordService(db).get_record(record_id)

@router.put("/{record_id}", response_model=RecordResponse)
def update_record(record_id: int, data: RecordUpdate, request: Request, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    return RecordService(db).update_record(record_id, data)

@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: int, request: Request, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    RecordService(db).delete_record(record_id)
