from sqlalchemy import Column, Integer, Float, String, Date, Enum as SAEnum, ForeignKey
from app.core.database import Base
import enum

class RecordType(str, enum.Enum):
    income = "income"
    expense = "expense"

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SAEnum(RecordType), nullable=False)
    category = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
