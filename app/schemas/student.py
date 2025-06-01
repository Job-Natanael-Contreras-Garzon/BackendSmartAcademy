from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True