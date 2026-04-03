from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.record import RecordType

class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=1, max_length=100)
    date: date
    notes: Optional[str] = None

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[date] = None
    notes: Optional[str] = None

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: RecordType
    category: str
    date: date
    notes: Optional[str]
    user_id: int
    class Config:
        from_attributes = True
