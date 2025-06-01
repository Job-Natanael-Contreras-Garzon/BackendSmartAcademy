from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import date
from enum import Enum


class TuitionStatus(str, Enum):
    """Estados posibles de una matrícula/pago"""
    PAID = "paid"
    PENDING = "pending"
    OVERDUE = "overdue"


class Month(str, Enum):
    """Meses del año para pagos mensuales"""
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"


class TuitionBase(BaseModel):
    """Esquema base para matrículas y pagos"""
    student_id: int
    amount: float = Field(..., ge=0)  # Debe ser un valor no negativo
    month: Month
    year: int = Field(..., ge=2000, le=2100)  # Rango válido de años
    status: TuitionStatus
    description: Optional[str] = None
    payment_date: Optional[date] = None
    due_date: Optional[date] = None

    @validator('payment_date')
    def payment_date_must_be_valid_for_paid(cls, v, values):
        if 'status' in values and values['status'] == TuitionStatus.PAID and not v:
            raise ValueError('El campo payment_date es obligatorio para pagos con estado "paid"')
        return v

    @validator('due_date')
    def due_date_should_be_set(cls, v, values):
        if 'status' in values and values['status'] in [TuitionStatus.PENDING, TuitionStatus.OVERDUE] and not v:
            raise ValueError('El campo due_date es recomendado para pagos con estado "pending" o "overdue"')
        return v


class TuitionCreate(TuitionBase):
    """Esquema para crear una matrícula/pago"""
    pass


class TuitionUpdate(BaseModel):
    """Esquema para actualizar una matrícula/pago"""
    amount: Optional[float] = Field(None, ge=0)
    status: Optional[TuitionStatus] = None
    description: Optional[str] = None
    payment_date: Optional[date] = None
    due_date: Optional[date] = None


class TuitionResponse(TuitionBase):
    """Esquema para respuesta de matrícula/pago"""
    id: int
    created_at: date

    class Config:
        from_attributes = True


class TuitionDetailResponse(TuitionResponse):
    """Esquema para respuesta detallada de matrícula/pago"""
    student_name: str
    student_code: Optional[str] = None
    group_name: Optional[str] = None
