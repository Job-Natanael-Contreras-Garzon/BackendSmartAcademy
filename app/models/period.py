from sqlalchemy import Column, Integer, String, Text, Date, Boolean
from app.db.base import Base

class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
