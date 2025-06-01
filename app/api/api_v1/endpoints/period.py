from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.period import PeriodCreate, PeriodUpdate, PeriodResponse

router = APIRouter()

@router.post("/", response_model=PeriodResponse, status_code=status.HTTP_201_CREATED)
async def create_period(
    period_data: PeriodCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Crear nuevo periodo académico (solo administradores)"""
    # Verificar si ya existe un periodo con el mismo nombre
    result = db.execute(
        text("SELECT id FROM periods WHERE name = :name"),
        {"name": period_data.name}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un periodo con este nombre"
        )
    
    # Validar fechas si se proporcionan
    if period_data.start_date and period_data.end_date:
        if period_data.start_date > period_data.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
    
    # Crear el periodo usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO periods (name, start_date, end_date, description, is_active) 
        VALUES (:name, :start_date, :end_date, :description, :is_active)
        RETURNING id, name, start_date, end_date, description, is_active
        """),
        {
            "name": period_data.name,
            "start_date": period_data.start_date,
            "end_date": period_data.end_date,
            "description": period_data.description,
            "is_active": period_data.is_active
        }
    )
    
    new_period = result.first()
    db.commit()
    
    return PeriodResponse(
        id=new_period.id,
        name=new_period.name,
        start_date=new_period.start_date,
        end_date=new_period.end_date,
        description=new_period.description,
        is_active=new_period.is_active
    )

@router.get("/", response_model=List[PeriodResponse])
async def read_periods(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar periodos académicos con opción de filtrado por estado"""
    # Construir la consulta base
    query = """
    SELECT id, name, start_date, end_date, description, is_active
    FROM periods
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtro de estado activo si se proporciona
    if is_active is not None:
        query += " AND is_active = :is_active"
        params["is_active"] = is_active
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY start_date DESC, name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    periods = result.fetchall()
    
    return [
        PeriodResponse(
            id=period.id,
            name=period.name,
            start_date=period.start_date,
            end_date=period.end_date,
            description=period.description,
            is_active=period.is_active
        )
        for period in periods
    ]

@router.get("/current", response_model=PeriodResponse)
async def get_current_period(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener el periodo académico actual (basado en fechas o estado activo)"""
    # Intentar encontrar un periodo que incluya la fecha actual
    today = date.today()
    result = db.execute(
        text("""
        SELECT id, name, start_date, end_date, description, is_active
        FROM periods
        WHERE is_active = true AND start_date <= :today AND end_date >= :today
        ORDER BY start_date DESC
        LIMIT 1
        """),
        {"today": today}
    )
    
    period = result.first()
    
    # Si no hay periodo que incluya la fecha actual, buscar el último periodo activo
    if not period:
        result = db.execute(
            text("""
            SELECT id, name, start_date, end_date, description, is_active
            FROM periods
            WHERE is_active = true
            ORDER BY start_date DESC
            LIMIT 1
            """)
        )
        period = result.first()
    
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay periodos académicos activos en este momento"
        )
    
    return PeriodResponse(
        id=period.id,
        name=period.name,
        start_date=period.start_date,
        end_date=period.end_date,
        description=period.description,
        is_active=period.is_active
    )

@router.get("/{period_id}", response_model=PeriodResponse)
async def read_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener periodo académico por ID"""
    result = db.execute(
        text("""
        SELECT id, name, start_date, end_date, description, is_active
        FROM periods
        WHERE id = :period_id
        """),
        {"period_id": period_id}
    )
    
    period = result.first()
    
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )
    
    return PeriodResponse(
        id=period.id,
        name=period.name,
        start_date=period.start_date,
        end_date=period.end_date,
        description=period.description,
        is_active=period.is_active
    )

@router.put("/{period_id}", response_model=PeriodResponse)
async def update_period(
    period_id: int,
    period_data: PeriodUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Actualizar periodo académico (solo administradores)"""
    # Verificar que el periodo existe
    result = db.execute(
        text("SELECT id FROM periods WHERE id = :period_id"),
        {"period_id": period_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"period_id": period_id}
    
    if period_data.name is not None:
        # Verificar que no exista otro periodo con el mismo nombre
        result = db.execute(
            text("SELECT id FROM periods WHERE name = :name AND id != :period_id"),
            {"name": period_data.name, "period_id": period_id}
        )
        if result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro periodo con este nombre"
            )
        
        update_fields.append("name = :name")
        params["name"] = period_data.name
    
    if period_data.start_date is not None:
        update_fields.append("start_date = :start_date")
        params["start_date"] = period_data.start_date
    
    if period_data.end_date is not None:
        update_fields.append("end_date = :end_date")
        params["end_date"] = period_data.end_date
    
    if period_data.description is not None:
        update_fields.append("description = :description")
        params["description"] = period_data.description
    
    if period_data.is_active is not None:
        update_fields.append("is_active = :is_active")
        params["is_active"] = period_data.is_active
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Validar fechas si se están actualizando ambas
    if "start_date" in params and "end_date" in params:
        if params["start_date"] > params["end_date"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
    # Si solo se actualiza una fecha, obtener la otra para validar
    elif "start_date" in params or "end_date" in params:
        current_period = db.execute(
            text("SELECT start_date, end_date FROM periods WHERE id = :period_id"),
            {"period_id": period_id}
        ).first()
        
        start_date = params.get("start_date", current_period.start_date)
        end_date = params.get("end_date", current_period.end_date)
        
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
    
    # Actualizar periodo usando SQL directo
    query = f"UPDATE periods SET {', '.join(update_fields)} WHERE id = :period_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el periodo actualizado
    result = db.execute(
        text("""
        SELECT id, name, start_date, end_date, description, is_active
        FROM periods 
        WHERE id = :period_id
        """),
        {"period_id": period_id}
    )
    updated_period = result.first()
    
    return PeriodResponse(
        id=updated_period.id,
        name=updated_period.name,
        start_date=updated_period.start_date,
        end_date=updated_period.end_date,
        description=updated_period.description,
        is_active=updated_period.is_active
    )

@router.delete("/{period_id}", status_code=status.HTTP_200_OK)
async def delete_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),
):
    """Eliminar periodo académico (solo administradores)"""
    # Verificar que el periodo existe
    result = db.execute(
        text("SELECT id FROM periods WHERE id = :period_id"),
        {"period_id": period_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )
    
    # Verificar si hay cursos o calificaciones asociadas a este periodo
    result = db.execute(
        text("SELECT id FROM courses WHERE period_id = :period_id LIMIT 1"),
        {"period_id": period_id}
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el periodo porque tiene cursos asociados"
        )
    
    # Eliminar periodo usando SQL directo
    db.execute(
        text("DELETE FROM periods WHERE id = :period_id"),
        {"period_id": period_id}
    )
    db.commit()
    
    return {"message": "Periodo eliminado correctamente"}
