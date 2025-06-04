from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy import Enum

from app.db.base import Base


class NotificationType(str, enum.Enum):
    """Tipos de notificaciones"""
    SYSTEM = "system"
    ACADEMIC = "academic"
    PAYMENT = "payment"
    ATTENDANCE = "attendance"
    GRADE = "grade"
    GENERAL = "general"


class NotificationPriority(str, enum.Enum):
    """Niveles de prioridad para notificaciones"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Notification(Base):
    """Modelo para las notificaciones del sistema"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.GENERAL, nullable=False)
    priority = Column(Enum(NotificationPriority), default=NotificationPriority.MEDIUM, nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    read_at = Column(DateTime, nullable=True)

    # Las relaciones están definidas mediante backref en el modelo User
