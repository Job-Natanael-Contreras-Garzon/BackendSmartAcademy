from sqlalchemy import Column, Integer, Float, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    period = Column(String(20))  # Ej: "Q1-2025"
    value = Column(Float, nullable=False)
    date_recorded = Column(Date)
    
    # Relaciones
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")