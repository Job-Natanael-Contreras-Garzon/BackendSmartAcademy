from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user
from app.models.user import User
from app.schemas.tuition import (
    TuitionCreate,
    TuitionUpdate,
    TuitionResponse,
    TuitionDetailResponse,
    TuitionStatus
)

router = APIRouter()

@router.post("/", response_model=TuitionResponse, status_code=status.HTTP_201_CREATED)
async def create_tuition(
    tuition_data: TuitionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden registrar pagos
):
    """Registrar matrícula/pago (solo administradores)"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id, user_id FROM students WHERE id = :student_id"),
        {"student_id": tuition_data.student_id}
    )
    student = result.first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar si ya existe un pago para el mismo estudiante, mes y año
    result = db.execute(
        text("""
        SELECT id 
        FROM student_tuition 
        WHERE student_id = :student_id AND month = :month AND year = :year
        """),
        {
            "student_id": tuition_data.student_id,
            "month": tuition_data.month,
            "year": tuition_data.year
        }
    )
    
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un registro de pago para este estudiante en {tuition_data.month} de {tuition_data.year}"
        )
    
    # Crear el registro de matrícula/pago
    now = datetime.now().date()
    result = db.execute(
        text("""
        INSERT INTO student_tuition (
            student_id, amount, month, year, status, description, 
            payment_date, due_date, created_at
        )
        VALUES (
            :student_id, :amount, :month, :year, :status, :description,
            :payment_date, :due_date, :created_at
        )
        RETURNING id, student_id, amount, month, year, status, description, 
                 payment_date, due_date, created_at
        """),
        {
            "student_id": tuition_data.student_id,
            "amount": tuition_data.amount,
            "month": tuition_data.month,
            "year": tuition_data.year,
            "status": tuition_data.status,
            "description": tuition_data.description,
            "payment_date": tuition_data.payment_date,
            "due_date": tuition_data.due_date,
            "created_at": now
        }
    )
    
    tuition = result.first()
    db.commit()
    
    # Convertir el resultado a diccionario
    tuition_dict = {
        "id": tuition.id,
        "student_id": tuition.student_id,
        "amount": float(tuition.amount),  # Convertir Decimal a float
        "month": tuition.month,
        "year": tuition.year,
        "status": tuition.status,
        "description": tuition.description,
        "payment_date": tuition.payment_date,
        "due_date": tuition.due_date,
        "created_at": tuition.created_at
    }
    
    return tuition_dict

@router.get("/", response_model=List[TuitionResponse])
async def list_tuitions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    month: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden ver todos los pagos
):
    """Listar matrículas/pagos (solo administradores)"""
    
    # Construir consulta base
    query = """
    SELECT id, student_id, amount, month, year, status, description, 
           payment_date, due_date, created_at
    FROM student_tuition
    WHERE 1=1
    """
    
    # Añadir filtros opcionales
    params = {}
    if status:
        query += " AND status = :status"
        params["status"] = status
    
    if month:
        query += " AND month = :month"
        params["month"] = month
    
    if year:
        query += " AND year = :year"
        params["year"] = year
    
    # Añadir paginación
    query += " ORDER BY created_at DESC LIMIT :limit OFFSET :skip"
    params["limit"] = limit
    params["skip"] = skip
    
    # Ejecutar consulta
    result = db.execute(text(query), params)
    
    tuitions = []
    for row in result:
        tuitions.append({
            "id": row.id,
            "student_id": row.student_id,
            "amount": float(row.amount),  # Convertir Decimal a float
            "month": row.month,
            "year": row.year,
            "status": row.status,
            "description": row.description,
            "payment_date": row.payment_date,
            "due_date": row.due_date,
            "created_at": row.created_at
        })
    
    return tuitions

@router.get("/student/{student_id}", response_model=List[TuitionDetailResponse])
async def get_student_tuitions(
    student_id: int,
    status: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener matrículas/pagos de un estudiante específico"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id, user_id FROM students WHERE id = :student_id"),
        {"student_id": student_id}
    )
    student = result.first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar permisos (solo el propio estudiante, administradores o tutores asignados)
    if not current_user.is_superuser and current_user.id != student.user_id:
        # Verificar si es tutor del estudiante
        result = db.execute(
            text("""
            SELECT id 
            FROM student_tutors 
            WHERE student_id = :student_id AND user_id = :user_id
            """),
            {"student_id": student_id, "user_id": current_user.id}
        )
        
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver los pagos de este estudiante"
            )
    
    # Construir consulta base con información detallada
    query = """
    SELECT 
        st.id, st.student_id, st.amount, st.month, st.year, 
        st.status, st.description, st.payment_date, st.due_date, st.created_at,
        s.full_name as student_name, s.code as student_code,
        g.name as group_name
    FROM student_tuition st
    JOIN students s ON s.id = st.student_id
    LEFT JOIN groups g ON g.id = s.group_id
    WHERE st.student_id = :student_id
    """
    
    # Añadir filtros opcionales
    params = {"student_id": student_id}
    if status:
        query += " AND st.status = :status"
        params["status"] = status
    
    if year:
        query += " AND st.year = :year"
        params["year"] = year
    
    # Ordenar por fecha de creación
    query += " ORDER BY st.created_at DESC"
    
    # Ejecutar consulta
    result = db.execute(text(query), params)
    
    tuitions = []
    for row in result:
        tuitions.append({
            "id": row.id,
            "student_id": row.student_id,
            "amount": float(row.amount),  # Convertir Decimal a float
            "month": row.month,
            "year": row.year,
            "status": row.status,
            "description": row.description,
            "payment_date": row.payment_date,
            "due_date": row.due_date,
            "created_at": row.created_at,
            "student_name": row.student_name,
            "student_code": row.student_code,
            "group_name": row.group_name
        })
    
    return tuitions

@router.get("/{tuition_id}", response_model=TuitionDetailResponse)
async def get_tuition_detail(
    tuition_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener detalle de una matrícula/pago específico"""
    # Obtener información detallada de la matrícula/pago
    result = db.execute(
        text("""
        SELECT 
            st.id, st.student_id, st.amount, st.month, st.year, 
            st.status, st.description, st.payment_date, st.due_date, st.created_at,
            s.full_name as student_name, s.code as student_code, s.user_id,
            g.name as group_name
        FROM student_tuition st
        JOIN students s ON s.id = st.student_id
        LEFT JOIN groups g ON g.id = s.group_id
        WHERE st.id = :tuition_id
        """),
        {"tuition_id": tuition_id}
    )
    
    tuition = result.first()
    if not tuition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula/pago no encontrado"
        )
    
    # Verificar permisos (solo el propio estudiante, administradores o tutores asignados)
    if not current_user.is_superuser and current_user.id != tuition.user_id:
        # Verificar si es tutor del estudiante
        result = db.execute(
            text("""
            SELECT id 
            FROM student_tutors 
            WHERE student_id = :student_id AND user_id = :user_id
            """),
            {"student_id": tuition.student_id, "user_id": current_user.id}
        )
        
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este pago"
            )
    
    # Convertir resultado a diccionario
    tuition_dict = {
        "id": tuition.id,
        "student_id": tuition.student_id,
        "amount": float(tuition.amount),  # Convertir Decimal a float
        "month": tuition.month,
        "year": tuition.year,
        "status": tuition.status,
        "description": tuition.description,
        "payment_date": tuition.payment_date,
        "due_date": tuition.due_date,
        "created_at": tuition.created_at,
        "student_name": tuition.student_name,
        "student_code": tuition.student_code,
        "group_name": tuition.group_name
    }
    
    return tuition_dict

@router.put("/{tuition_id}", response_model=TuitionResponse)
async def update_tuition(
    tuition_id: int,
    tuition_data: TuitionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden actualizar pagos
):
    """Actualizar matrícula/pago (solo administradores)"""
    # Verificar que la matrícula/pago existe
    result = db.execute(
        text("SELECT id FROM student_tuition WHERE id = :tuition_id"),
        {"tuition_id": tuition_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula/pago no encontrado"
        )
    
    # Preparar los campos a actualizar
    update_fields = {}
    if tuition_data.amount is not None:
        update_fields["amount"] = tuition_data.amount
    if tuition_data.status is not None:
        update_fields["status"] = tuition_data.status
    if tuition_data.description is not None:
        update_fields["description"] = tuition_data.description
    if tuition_data.payment_date is not None:
        update_fields["payment_date"] = tuition_data.payment_date
    if tuition_data.due_date is not None:
        update_fields["due_date"] = tuition_data.due_date
    
    if not update_fields:
        # No hay campos para actualizar, obtener datos actuales
        result = db.execute(
            text("""
            SELECT id, student_id, amount, month, year, status, description, 
                   payment_date, due_date, created_at
            FROM student_tuition
            WHERE id = :tuition_id
            """),
            {"tuition_id": tuition_id}
        )
        tuition = result.first()
        return {
            "id": tuition.id,
            "student_id": tuition.student_id,
            "amount": float(tuition.amount),
            "month": tuition.month,
            "year": tuition.year,
            "status": tuition.status,
            "description": tuition.description,
            "payment_date": tuition.payment_date,
            "due_date": tuition.due_date,
            "created_at": tuition.created_at
        }
    
    # Construir la consulta SQL de actualización
    set_clause = ", ".join(f"{field} = :{field}" for field in update_fields)
    query = f"""
    UPDATE student_tuition 
    SET {set_clause}
    WHERE id = :tuition_id
    RETURNING id, student_id, amount, month, year, status, description, 
              payment_date, due_date, created_at
    """
    
    # Añadir el ID a los parámetros
    update_fields["tuition_id"] = tuition_id
    
    # Ejecutar la actualización
    result = db.execute(text(query), update_fields)
    updated_tuition = result.first()
    db.commit()
    
    # Convertir resultado a diccionario
    tuition_dict = {
        "id": updated_tuition.id,
        "student_id": updated_tuition.student_id,
        "amount": float(updated_tuition.amount),  # Convertir Decimal a float
        "month": updated_tuition.month,
        "year": updated_tuition.year,
        "status": updated_tuition.status,
        "description": updated_tuition.description,
        "payment_date": updated_tuition.payment_date,
        "due_date": updated_tuition.due_date,
        "created_at": updated_tuition.created_at
    }
    
    return tuition_dict

@router.delete("/{tuition_id}", status_code=status.HTTP_200_OK)
async def delete_tuition(
    tuition_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser),  # Solo administradores pueden eliminar pagos
):
    """Eliminar matrícula/pago (solo administradores)"""
    # Verificar que la matrícula/pago existe
    result = db.execute(
        text("SELECT id FROM student_tuition WHERE id = :tuition_id"),
        {"tuition_id": tuition_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula/pago no encontrado"
        )
    
    # Eliminar el registro
    db.execute(
        text("DELETE FROM student_tuition WHERE id = :tuition_id"),
        {"tuition_id": tuition_id}
    )
    db.commit()
    
    return {"message": "Matrícula/pago eliminado correctamente"}
