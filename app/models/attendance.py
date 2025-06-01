from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date, nullable=False)
    present = Column(Boolean, default=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    # Relaciones
    student = relationship("Student", back_populates="attendances")