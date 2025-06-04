from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Participation(Base):
    __tablename__ = "participations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    date = Column(Date, nullable=False)
    score = Column(Float, nullable=False)  # Puntuación de 0 a 10
    period = Column(String, nullable=True) # Periodo académico del registro
    
    # Relaciones
    student = relationship("Student", back_populates="participations")