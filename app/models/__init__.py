# app/models/__init__.py

# Importamos Base desde app.db.base
from app.db.base import Base

# Importamos todos los modelos (con mayúscula inicial)
from .user import User
from .student import Student
from .course import Course
from .grade import Grade
from .attendance import Attendance
from .participation import Participation

# Exportamos todos los modelos
__all__ = [
    "Base",
    "User",
    "Student",
    "Course",
    "Grade",
    "Attendance",
    "Participation",
]