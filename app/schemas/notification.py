from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Tipos de notificaciones"""
    SYSTEM = "system"
    ACADEMIC = "academic"
    PAYMENT = "payment"
    ATTENDANCE = "attendance"
    GRADE = "grade"
    GENERAL = "general"


class NotificationPriority(str, Enum):
    """Niveles de prioridad para notificaciones"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationBase(BaseModel):
    """Esquema base para notificaciones"""
    title: str
    content: str
    type: NotificationType = NotificationType.GENERAL
    priority: NotificationPriority = NotificationPriority.MEDIUM
    recipient_id: int  # ID del usuario destinatario
    sender_id: Optional[int] = None  # ID del usuario remitente, None para notificaciones del sistema


class NotificationCreate(NotificationBase):
    """Esquema para crear una notificación"""
    pass


class NotificationUpdate(BaseModel):
    """Esquema para actualizar una notificación"""
    is_read: Optional[bool] = None
    read_at: Optional[datetime] = None


class NotificationResponse(NotificationBase):
    """Esquema para respuesta de notificaciones"""
    id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationDetailResponse(NotificationResponse):
    """Esquema para respuesta detallada de notificaciones"""
    sender_name: Optional[str] = None
    recipient_name: str
