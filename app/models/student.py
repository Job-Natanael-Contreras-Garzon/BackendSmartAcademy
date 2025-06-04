from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True)
    date_of_birth = Column(Date)
    address = Column(String(200))
    phone = Column(String(50))  # Increased length from 20 to 50
    
    # Relaciones
    grades = relationship("Grade", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    participations = relationship("Participation", back_populates="student")