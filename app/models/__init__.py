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
from .role import Role
from .user_device import UserDevice  # Added UserDevice model import
from .user_notification_preference import UserNotificationPreference  # Added UserNotificationPreference model import
from .notification import Notification  # Added Notification model import

# Exportamos todos los modelos
__all__ = [
    "Base",
    "User",
    "Student",
    "Course",
    "Grade",
    "Attendance",
    "Participation",
    "Role",
    "UserDevice",  # Added UserDevice to __all__
    "UserNotificationPreference",  # Added UserNotificationPreference to __all__
    "Notification",  # Added Notification to __all__
]