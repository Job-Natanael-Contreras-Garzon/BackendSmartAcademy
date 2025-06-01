from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PeriodBase(BaseModel):
    name: str  # Ejemplo: "Q1-2025"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    is_active: bool = True

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class PeriodResponse(PeriodBase):
    id: int

    class Config:
        orm_mode = True
