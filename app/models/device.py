from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class UserDevice(Base):
    """Modelo para los dispositivos móviles registrados de los usuarios"""
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_token = Column(String(255), nullable=False)
    device_platform = Column(String(20), nullable=False)  # android, ios, web
    device_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relaciones
    user = relationship("User", back_populates="devices")

    # Constraint para evitar duplicados
    __table_args__ = (
        UniqueConstraint('user_id', 'device_token', name='uix_user_device_token'),
    )


class UserNotificationPreference(Base):
    """Modelo para las preferencias de notificaciones de los usuarios"""
    __tablename__ = "user_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    enable_push = Column(Boolean, default=True, nullable=False)
    enable_academic = Column(Boolean, default=True, nullable=False)
    enable_payment = Column(Boolean, default=True, nullable=False)
    enable_attendance = Column(Boolean, default=True, nullable=False)
    enable_grade = Column(Boolean, default=True, nullable=False)
    enable_general = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="notification_preferences")
