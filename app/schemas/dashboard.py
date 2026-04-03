from pydantic import BaseModel
from typing import List, Dict, Any

class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_breakdown: List[Dict[str, Any]]
    monthly_trends: List[Dict[str, Any]]
    recent_transactions: List[Dict[str, Any]]
