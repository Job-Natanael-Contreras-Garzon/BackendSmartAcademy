from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationDetailResponse,
    NotificationType,
    NotificationPriority
)

router = APIRouter()

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Crear una notificación (administradores pueden crear para cualquiera, usuarios solo para sí mismos)"""
    # Verificar que el destinatario existe
    result = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": notification_data.recipient_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario destinatario no encontrado"
        )
    
    # Verificar permisos: solo administradores pueden crear notificaciones para otros usuarios
    if not current_user.is_superuser and current_user.id != notification_data.recipient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear notificaciones para otros usuarios"
        )
    
    # Si no se especifica sender_id, usar el ID del usuario actual
    sender_id = notification_data.sender_id or current_user.id
    
    # Crear la notificación
    now = datetime.now()
    result = db.execute(
        text("""
        INSERT INTO notifications (
            title, content, type, priority, recipient_id, sender_id, 
            is_read, created_at, read_at
        )
        VALUES (
            :title, :content, :type, :priority, :recipient_id, :sender_id, 
            :is_read, :created_at, :read_at
        )
        RETURNING id, title, content, type, priority, recipient_id, sender_id, 
                 is_read, created_at, read_at
        """),
        {
            "title": notification_data.title,
            "content": notification_data.content,
            "type": notification_data.type,
            "priority": notification_data.priority,
            "recipient_id": notification_data.recipient_id,
            "sender_id": sender_id,
            "is_read": False,
            "created_at": now,
            "read_at": None
        }
    )
    
    notification = result.first()
    db.commit()
    
    # Convertir el resultado a diccionario
    notification_dict = {
        "id": notification.id,
        "title": notification.title,
        "content": notification.content,
        "type": notification.type,
        "priority": notification.priority,
        "recipient_id": notification.recipient_id,
        "sender_id": notification.sender_id,
        "is_read": notification.is_read,
        "created_at": notification.created_at,
        "read_at": notification.read_at
    }
    
    return notification_dict

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def create_bulk_notifications(
    recipient_ids: List[int] = Body(...),
    title: str = Body(...),
    content: str = Body(...),
    type: NotificationType = Body(NotificationType.GENERAL),
    priority: NotificationPriority = Body(NotificationPriority.MEDIUM),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),  # Solo administradores pueden enviar notificaciones masivas
):
    """Crear notificaciones masivas para múltiples usuarios (solo administradores)"""
    # Verificar que hay al menos un destinatario
    if not recipient_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes especificar al menos un destinatario"
        )
    
    # Verificar que todos los destinatarios existen
    placeholders = ", ".join([str(id) for id in recipient_ids])
    result = db.execute(
        text(f"SELECT id FROM users WHERE id IN ({placeholders})")
    )
    found_ids = [row[0] for row in result]
    
    if len(found_ids) != len(recipient_ids):
        missing_ids = set(recipient_ids) - set(found_ids)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Los siguientes IDs de usuario no existen: {missing_ids}"
        )
    
    # Crear notificaciones para cada destinatario
    now = datetime.now()
    created_count = 0
    
    for recipient_id in recipient_ids:
        db.execute(
            text("""
            INSERT INTO notifications (
                title, content, type, priority, recipient_id, sender_id, 
                is_read, created_at, read_at
            )
            VALUES (
                :title, :content, :type, :priority, :recipient_id, :sender_id, 
                :is_read, :created_at, :read_at
            )
            """),
            {
                "title": title,
                "content": content,
                "type": type,
                "priority": priority,
                "recipient_id": recipient_id,
                "sender_id": current_user.id,
                "is_read": False,
                "created_at": now,
                "read_at": None
            }
        )
        created_count += 1
    
    db.commit()
    
    return {
        "message": f"Se han creado {created_count} notificaciones correctamente",
        "count": created_count
    }

@router.get("/user/{user_id}", response_model=List[NotificationDetailResponse])
async def get_user_notifications(
    user_id: int,
    is_read: Optional[bool] = None,
    type: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Obtener notificaciones de un usuario específico (solo el propio usuario o administradores)"""
    # Verificar permisos
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver las notificaciones de este usuario"
        )
    
    # Verificar que el usuario existe
    result = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Construir consulta base con información detallada
    query = """
    SELECT 
        n.id, n.title, n.content, n.type, n.priority,
        n.recipient_id, n.sender_id, n.is_read, n.created_at, n.read_at,
        ur.full_name as recipient_name,
        us.full_name as sender_name
    FROM notifications n
    JOIN users ur ON ur.id = n.recipient_id
    LEFT JOIN users us ON us.id = n.sender_id
    WHERE n.recipient_id = :user_id
    """
    
    # Añadir filtros opcionales
    params = {"user_id": user_id}
    if is_read is not None:
        query += " AND n.is_read = :is_read"
        params["is_read"] = is_read
    
    if type:
        query += " AND n.type = :type"
        params["type"] = type
    
    if priority:
        query += " AND n.priority = :priority"
        params["priority"] = priority
    
    # Añadir ordenamiento y paginación
    query += " ORDER BY n.created_at DESC LIMIT :limit OFFSET :skip"
    params["limit"] = limit
    params["skip"] = skip
    
    # Ejecutar consulta
    result = db.execute(text(query), params)
    
    notifications = []
    for row in result:
        notifications.append({
            "id": row.id,
            "title": row.title,
            "content": row.content,
            "type": row.type,
            "priority": row.priority,
            "recipient_id": row.recipient_id,
            "sender_id": row.sender_id,
            "is_read": row.is_read,
            "created_at": row.created_at,
            "read_at": row.read_at,
            "recipient_name": row.recipient_name,
            "sender_name": row.sender_name
        })
    
    return notifications

@router.get("/{notification_id}", response_model=NotificationDetailResponse)
async def get_notification_detail(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Obtener detalle de una notificación específica"""
    # Obtener información detallada de la notificación
    result = db.execute(
        text("""
        SELECT 
            n.id, n.title, n.content, n.type, n.priority,
            n.recipient_id, n.sender_id, n.is_read, n.created_at, n.read_at,
            ur.full_name as recipient_name,
            us.full_name as sender_name
        FROM notifications n
        JOIN users ur ON ur.id = n.recipient_id
        LEFT JOIN users us ON us.id = n.sender_id
        WHERE n.id = :notification_id
        """),
        {"notification_id": notification_id}
    )
    
    notification = result.first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    
    # Verificar permisos (solo el propio destinatario o administradores)
    if current_user.id != notification.recipient_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta notificación"
        )
    
    # Convertir resultado a diccionario
    notification_dict = {
        "id": notification.id,
        "title": notification.title,
        "content": notification.content,
        "type": notification.type,
        "priority": notification.priority,
        "recipient_id": notification.recipient_id,
        "sender_id": notification.sender_id,
        "is_read": notification.is_read,
        "created_at": notification.created_at,
        "read_at": notification.read_at,
        "recipient_name": notification.recipient_name,
        "sender_name": notification.sender_name
    }
    
    return notification_dict

@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Marcar una notificación como leída"""
    # Verificar que la notificación existe y obtener información básica
    result = db.execute(
        text("""
        SELECT id, recipient_id, is_read 
        FROM notifications 
        WHERE id = :notification_id
        """),
        {"notification_id": notification_id}
    )
    
    notification = result.first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    
    # Verificar permisos (solo el propio destinatario o administradores)
    if current_user.id != notification.recipient_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para marcar esta notificación"
        )
    
    # Si ya está marcada como leída, simplemente devolver la información
    if notification.is_read:
        result = db.execute(
            text("""
            SELECT * FROM notifications WHERE id = :notification_id
            """),
            {"notification_id": notification_id}
        )
        notification = result.first()
        return {
            "id": notification.id,
            "title": notification.title,
            "content": notification.content,
            "type": notification.type,
            "priority": notification.priority,
            "recipient_id": notification.recipient_id,
            "sender_id": notification.sender_id,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
            "read_at": notification.read_at
        }
    
    # Marcar como leída y actualizar read_at
    now = datetime.now()
    result = db.execute(
        text("""
        UPDATE notifications 
        SET is_read = TRUE, read_at = :read_at
        WHERE id = :notification_id
        RETURNING id, title, content, type, priority, recipient_id, sender_id, 
                 is_read, created_at, read_at
        """),
        {"notification_id": notification_id, "read_at": now}
    )
    
    updated_notification = result.first()
    db.commit()
    
    return {
        "id": updated_notification.id,
        "title": updated_notification.title,
        "content": updated_notification.content,
        "type": updated_notification.type,
        "priority": updated_notification.priority,
        "recipient_id": updated_notification.recipient_id,
        "sender_id": updated_notification.sender_id,
        "is_read": updated_notification.is_read,
        "created_at": updated_notification.created_at,
        "read_at": updated_notification.read_at
    }

@router.delete("/{notification_id}", status_code=status.HTTP_200_OK)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Eliminar una notificación (solo el propio destinatario o administradores)"""
    # Verificar que la notificación existe y obtener información básica
    result = db.execute(
        text("""
        SELECT id, recipient_id 
        FROM notifications 
        WHERE id = :notification_id
        """),
        {"notification_id": notification_id}
    )
    
    notification = result.first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    
    # Verificar permisos (solo el propio destinatario o administradores)
    if current_user.id != notification.recipient_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta notificación"
        )
    
    # Eliminar la notificación
    db.execute(
        text("DELETE FROM notifications WHERE id = :notification_id"),
        {"notification_id": notification_id}
    )
    db.commit()
    
    return {"message": "Notificación eliminada correctamente"}
