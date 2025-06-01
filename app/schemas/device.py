from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class DevicePlatform(str, Enum):
    """Plataformas soportadas para dispositivos móviles"""
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


class DeviceBase(BaseModel):
    """Esquema base para dispositivos"""
    device_token: str = Field(..., description="Token FCM del dispositivo")
    device_platform: DevicePlatform = Field(..., description="Plataforma del dispositivo")
    device_name: Optional[str] = Field(None, description="Nombre descriptivo del dispositivo")


class DeviceCreate(DeviceBase):
    """Esquema para registrar un nuevo dispositivo"""
    pass


class DeviceResponse(DeviceBase):
    """Esquema para respuesta de dispositivo"""
    id: int
    user_id: int
    created_at: str
    is_active: bool = True

    class Config:
        from_attributes = True


class NotificationPreferences(BaseModel):
    """Preferencias de notificaciones para un usuario"""
    enable_push: bool = Field(True, description="Habilitar notificaciones push")
    enable_academic: bool = Field(True, description="Notificaciones académicas")
    enable_payment: bool = Field(True, description="Notificaciones de pagos")
    enable_attendance: bool = Field(True, description="Notificaciones de asistencia")
    enable_grade: bool = Field(True, description="Notificaciones de calificaciones")
    enable_general: bool = Field(True, description="Notificaciones generales")
