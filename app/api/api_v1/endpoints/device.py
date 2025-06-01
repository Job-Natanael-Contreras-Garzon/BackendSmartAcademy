from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.config.database import get_db
from app.core.security import get_current_active_user, get_current_active_superuser
from app.models.user import User
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DevicePlatform,
    NotificationPreferences
)

router = APIRouter()

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Registra un dispositivo para notificaciones push.
    Un usuario puede tener múltiples dispositivos registrados.
    """
    # Verificar si el dispositivo ya está registrado para este usuario
    result = db.execute(
        text("""
        SELECT id FROM user_devices 
        WHERE user_id = :user_id AND device_token = :device_token
        """),
        {
            "user_id": current_user.id,
            "device_token": device_data.device_token
        }
    )
    
    device = result.first()
    if device:
        # Si el dispositivo ya existe, actualizarlo
        result = db.execute(
            text("""
            UPDATE user_devices 
            SET device_platform = :device_platform, device_name = :device_name, 
                is_active = TRUE, updated_at = :updated_at
            WHERE id = :id
            RETURNING id, user_id, device_token, device_platform, device_name, 
                    created_at, is_active
            """),
            {
                "id": device.id,
                "device_platform": device_data.device_platform,
                "device_name": device_data.device_name,
                "updated_at": datetime.now()
            }
        )
        db.commit()
        updated_device = result.first()
        
        # Convertir a diccionario
        return {
            "id": updated_device.id,
            "user_id": updated_device.user_id,
            "device_token": updated_device.device_token,
            "device_platform": updated_device.device_platform,
            "device_name": updated_device.device_name,
            "created_at": updated_device.created_at.isoformat(),
            "is_active": updated_device.is_active
        }
    
    # Si no existe, crear un nuevo registro
    now = datetime.now()
    result = db.execute(
        text("""
        INSERT INTO user_devices (
            user_id, device_token, device_platform, device_name, 
            created_at, updated_at, is_active
        )
        VALUES (
            :user_id, :device_token, :device_platform, :device_name, 
            :created_at, :updated_at, TRUE
        )
        RETURNING id, user_id, device_token, device_platform, device_name, 
                created_at, is_active
        """),
        {
            "user_id": current_user.id,
            "device_token": device_data.device_token,
            "device_platform": device_data.device_platform,
            "device_name": device_data.device_name,
            "created_at": now,
            "updated_at": now
        }
    )
    
    db.commit()
    new_device = result.first()
    
    # Convertir a diccionario
    return {
        "id": new_device.id,
        "user_id": new_device.user_id,
        "device_token": new_device.device_token,
        "device_platform": new_device.device_platform,
        "device_name": new_device.device_name,
        "created_at": new_device.created_at.isoformat(),
        "is_active": new_device.is_active
    }

@router.get("/", response_model=List[DeviceResponse])
async def get_user_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Obtiene todos los dispositivos registrados del usuario actual"""
    result = db.execute(
        text("""
        SELECT id, user_id, device_token, device_platform, device_name, 
               created_at, is_active
        FROM user_devices
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        """),
        {"user_id": current_user.id}
    )
    
    devices = []
    for row in result:
        devices.append({
            "id": row.id,
            "user_id": row.user_id,
            "device_token": row.device_token,
            "device_platform": row.device_platform,
            "device_name": row.device_name,
            "created_at": row.created_at.isoformat(),
            "is_active": row.is_active
        })
    
    return devices

@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Elimina (desactiva) un dispositivo registrado"""
    # Verificar que el dispositivo existe y pertenece al usuario
    result = db.execute(
        text("""
        SELECT id, user_id FROM user_devices
        WHERE id = :device_id
        """),
        {"device_id": device_id}
    )
    
    device = result.first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )
    
    # Verificar permisos (solo el propio usuario puede eliminar sus dispositivos)
    if device.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este dispositivo"
        )
    
    # Marcar como inactivo en lugar de eliminar físicamente
    db.execute(
        text("""
        UPDATE user_devices
        SET is_active = FALSE, updated_at = :updated_at
        WHERE id = :device_id
        """),
        {"device_id": device_id, "updated_at": datetime.now()}
    )
    
    db.commit()
    
    return {"message": "Dispositivo eliminado correctamente"}

@router.get("/preferences", response_model=NotificationPreferences)
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Obtiene las preferencias de notificaciones del usuario actual"""
    result = db.execute(
        text("""
        SELECT enable_push, enable_academic, enable_payment, 
               enable_attendance, enable_grade, enable_general
        FROM user_notification_preferences
        WHERE user_id = :user_id
        """),
        {"user_id": current_user.id}
    )
    
    preferences = result.first()
    
    # Si no hay preferencias configuradas, crear con valores predeterminados
    if not preferences:
        db.execute(
            text("""
            INSERT INTO user_notification_preferences (
                user_id, enable_push, enable_academic, enable_payment, 
                enable_attendance, enable_grade, enable_general, created_at
            )
            VALUES (
                :user_id, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, :created_at
            )
            """),
            {"user_id": current_user.id, "created_at": datetime.now()}
        )
        db.commit()
        
        return {
            "enable_push": True,
            "enable_academic": True,
            "enable_payment": True,
            "enable_attendance": True,
            "enable_grade": True,
            "enable_general": True
        }
    
    # Convertir a diccionario
    return {
        "enable_push": preferences.enable_push,
        "enable_academic": preferences.enable_academic,
        "enable_payment": preferences.enable_payment,
        "enable_attendance": preferences.enable_attendance,
        "enable_grade": preferences.enable_grade,
        "enable_general": preferences.enable_general
    }

@router.put("/preferences", response_model=NotificationPreferences)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Actualiza las preferencias de notificaciones del usuario actual"""
    # Verificar si ya existen preferencias
    result = db.execute(
        text("""
        SELECT id FROM user_notification_preferences
        WHERE user_id = :user_id
        """),
        {"user_id": current_user.id}
    )
    
    existing = result.first()
    
    if existing:
        # Actualizar preferencias existentes
        db.execute(
            text("""
            UPDATE user_notification_preferences
            SET enable_push = :enable_push,
                enable_academic = :enable_academic,
                enable_payment = :enable_payment,
                enable_attendance = :enable_attendance,
                enable_grade = :enable_grade,
                enable_general = :enable_general,
                updated_at = :updated_at
            WHERE user_id = :user_id
            """),
            {
                "user_id": current_user.id,
                "enable_push": preferences.enable_push,
                "enable_academic": preferences.enable_academic,
                "enable_payment": preferences.enable_payment,
                "enable_attendance": preferences.enable_attendance,
                "enable_grade": preferences.enable_grade,
                "enable_general": preferences.enable_general,
                "updated_at": datetime.now()
            }
        )
    else:
        # Crear nuevas preferencias
        db.execute(
            text("""
            INSERT INTO user_notification_preferences (
                user_id, enable_push, enable_academic, enable_payment, 
                enable_attendance, enable_grade, enable_general, 
                created_at, updated_at
            )
            VALUES (
                :user_id, :enable_push, :enable_academic, :enable_payment, 
                :enable_attendance, :enable_grade, :enable_general, 
                :created_at, :updated_at
            )
            """),
            {
                "user_id": current_user.id,
                "enable_push": preferences.enable_push,
                "enable_academic": preferences.enable_academic,
                "enable_payment": preferences.enable_payment,
                "enable_attendance": preferences.enable_attendance,
                "enable_grade": preferences.enable_grade,
                "enable_general": preferences.enable_general,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        )
    
    db.commit()
    
    return preferences
