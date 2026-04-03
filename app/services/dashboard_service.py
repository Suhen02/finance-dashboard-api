from sqlalchemy.orm import Session
from app.repositories.record_repository import RecordRepository

class DashboardService:
    def __init__(self, db: Session):
        self.repo = RecordRepository(db)

    def get_summary(self) -> dict:
        totals = self.repo.get_totals()
        return {
            "total_income": totals["total_income"],
            "total_expense": totals["total_expense"],
            "net_balance": totals["total_income"] - totals["total_expense"],
            "category_breakdown": self.repo.get_category_breakdown(),
            "monthly_trends": self.repo.get_monthly_trends(),
            "recent_transactions": self.repo.get_recent(5),
        }
