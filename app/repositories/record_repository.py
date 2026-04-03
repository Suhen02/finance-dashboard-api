from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract, case
from app.models.record import FinancialRecord, RecordType
from typing import Optional
from datetime import date

class RecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, record: FinancialRecord) -> FinancialRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, record_id: int) -> FinancialRecord | None:
        return self.db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    def get_all(self, skip: int = 0, limit: int = 20,
                category: Optional[str] = None,
                type_filter: Optional[RecordType] = None,
                start_date: Optional[date] = None,
                end_date: Optional[date] = None):
        q = self.db.query(FinancialRecord)
        if category:
            q = q.filter(FinancialRecord.category == category)
        if type_filter:
            q = q.filter(FinancialRecord.type == type_filter)
        if start_date:
            q = q.filter(FinancialRecord.date >= start_date)
        if end_date:
            q = q.filter(FinancialRecord.date <= end_date)
        return q.order_by(desc(FinancialRecord.date)).offset(skip).limit(limit).all()

    def update(self, record: FinancialRecord, data: dict) -> FinancialRecord:
        for k, v in data.items():
            if v is not None:
                setattr(record, k, v)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: FinancialRecord):
        self.db.delete(record)
        self.db.commit()

    def get_totals(self):
        result = self.db.query(
            func.coalesce(func.sum(case((FinancialRecord.type == RecordType.income, FinancialRecord.amount), else_=0)), 0).label("total_income"),
            func.coalesce(func.sum(case((FinancialRecord.type == RecordType.expense, FinancialRecord.amount), else_=0)), 0).label("total_expense"),
        ).first()
        return {"total_income": float(result.total_income), "total_expense": float(result.total_expense)}

    def get_category_breakdown(self):
        rows = self.db.query(
            FinancialRecord.category,
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total")
        ).group_by(FinancialRecord.category, FinancialRecord.type).all()
        return [{"category": r.category, "type": r.type.value, "total": float(r.total)} for r in rows]

    def get_monthly_trends(self):
        rows = self.db.query(
            func.strftime("%Y-%m", FinancialRecord.date).label("month"),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total")
        ).group_by("month", FinancialRecord.type).order_by("month").all()
        return [{"month": r.month, "type": r.type.value, "total": float(r.total)} for r in rows]

    def get_recent(self, limit: int = 5):
        rows = self.db.query(FinancialRecord).order_by(desc(FinancialRecord.date)).limit(limit).all()
        return [{"id": r.id, "amount": r.amount, "type": r.type.value, "category": r.category, "date": str(r.date), "notes": r.notes, "user_id": r.user_id} for r in rows]
