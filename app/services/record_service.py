from sqlalchemy.orm import Session
from app.repositories.record_repository import RecordRepository
from app.models.record import FinancialRecord, RecordType
from app.schemas.record import RecordCreate, RecordUpdate
from app.exceptions.app_exception import AppException
from typing import Optional
from datetime import date

class RecordService:
    def __init__(self, db: Session):
        self.repo = RecordRepository(db)

    def create_record(self, data: RecordCreate, user_id: int) -> FinancialRecord:
        record = FinancialRecord(
            amount=data.amount, type=data.type, category=data.category,
            date=data.date, notes=data.notes, user_id=user_id
        )
        return self.repo.create(record)

    def get_records(self, skip: int = 0, limit: int = 20,
                    category: Optional[str] = None,
                    type_filter: Optional[RecordType] = None,
                    start_date: Optional[date] = None,
                    end_date: Optional[date] = None):
        return self.repo.get_all(skip, limit, category, type_filter, start_date, end_date)

    def get_record(self, record_id: int) -> FinancialRecord:
        record = self.repo.get_by_id(record_id)
        if not record:
            raise AppException("Record not found", 404)
        return record

    def update_record(self, record_id: int, data: RecordUpdate) -> FinancialRecord:
        record = self.repo.get_by_id(record_id)
        if not record:
            raise AppException("Record not found", 404)
        return self.repo.update(record, data.model_dump(exclude_unset=True))

    def delete_record(self, record_id: int):
        record = self.repo.get_by_id(record_id)
        if not record:
            raise AppException("Record not found", 404)
        self.repo.delete(record)
