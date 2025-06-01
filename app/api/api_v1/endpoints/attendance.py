from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from pydantic import BaseModel, Field

from app.config.database import get_db
from app.core.security import get_current_active_superuser, get_current_active_user, get_current_active_teacher
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse, AttendanceDetailResponse, AttendanceStatus

router = APIRouter()

@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden registrar asistencia
):
    """Registrar asistencia (solo profesores)"""
    # Verificar que el estudiante existe
    result = db.execute(
        text("SELECT id FROM students WHERE id = :student_id"),
        {"student_id": attendance_data.student_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": attendance_data.course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar que el profesor tiene permiso para registrar asistencia en este curso
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": attendance_data.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para registrar asistencia en este curso"
        )
    
    # Verificar que el estudiante está en el curso (a través del grupo asignado al curso)
    result = db.execute(
        text("""
        SELECT s.id 
        FROM students s
        JOIN courses c ON s.group_id = c.group_id
        WHERE s.id = :student_id AND c.id = :course_id
        """),
        {"student_id": attendance_data.student_id, "course_id": attendance_data.course_id}
    )
    if not result.first():
        # Si no hay coincidencia por grupo, advertir pero permitir (podría ser un caso especial)
        print("Advertencia: El estudiante no está en el grupo asignado a este curso")
    
    # Verificar si ya existe un registro para este estudiante, curso y fecha
    result = db.execute(
        text("""
        SELECT id FROM attendances 
        WHERE student_id = :student_id AND course_id = :course_id AND date = :date
        """),
        {
            "student_id": attendance_data.student_id,
            "course_id": attendance_data.course_id,
            "date": attendance_data.date
        }
    )
    existing = result.first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un registro de asistencia para este estudiante, curso y fecha"
        )
    
    # Crear el registro de asistencia usando SQL directo
    result = db.execute(
        text("""
        INSERT INTO attendances (student_id, course_id, date, status, notes) 
        VALUES (:student_id, :course_id, :date, :status, :notes)
        RETURNING id, student_id, course_id, date, status, notes
        """),
        {
            "student_id": attendance_data.student_id,
            "course_id": attendance_data.course_id,
            "date": attendance_data.date,
            "status": attendance_data.status.value,
            "notes": attendance_data.notes
        }
    )
    
    new_attendance = result.first()
    db.commit()
    
    return AttendanceResponse(
        id=new_attendance.id,
        student_id=new_attendance.student_id,
        course_id=new_attendance.course_id,
        date=new_attendance.date,
        status=new_attendance.status,
        notes=new_attendance.notes
    )

@router.get("/", response_model=List[AttendanceDetailResponse])
async def read_attendances(
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    status: Optional[AttendanceStatus] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Listar registros de asistencia con opciones de filtrado"""
    # Construir la consulta base
    query = """
    SELECT a.id, a.student_id, a.course_id, a.date, a.status, a.notes,
           CONCAT(u.full_name) as student_name, s.student_code,
           sb.name as subject_name, 
           tu.full_name as teacher_name,
           gr.group_name
    FROM attendances a
    JOIN students s ON a.student_id = s.id
    JOIN users u ON s.user_id = u.id
    JOIN courses c ON a.course_id = c.id
    JOIN subjects sb ON c.subject_id = sb.id
    JOIN teachers t ON c.teacher_id = t.id
    JOIN users tu ON t.user_id = tu.id
    LEFT JOIN groups gr ON s.group_id = gr.id
    WHERE 1=1
    """
    
    params = {"skip": skip, "limit": limit}
    
    # Aplicar filtros si se proporcionan
    if student_id is not None:
        query += " AND a.student_id = :student_id"
        params["student_id"] = student_id
    
    if course_id is not None:
        query += " AND a.course_id = :course_id"
        params["course_id"] = course_id
    
    if date_from is not None:
        query += " AND a.date >= :date_from"
        params["date_from"] = date_from
    
    if date_to is not None:
        query += " AND a.date <= :date_to"
        params["date_to"] = date_to
    
    if status is not None:
        query += " AND a.status = :status"
        params["status"] = status.value
    
    # Aplicar filtros basados en el rol del usuario
    if not current_user.is_superuser:
        # Si es profesor, solo ve asistencias de sus cursos
        result = db.execute(
            text("SELECT id FROM teachers WHERE user_id = :user_id"),
            {"user_id": current_user.id}
        )
        teacher = result.first()
        
        if teacher:
            query += " AND c.teacher_id = :teacher_id"
            params["teacher_id"] = teacher.id
        else:
            # Si es estudiante, solo ve sus propias asistencias
            result = db.execute(
                text("SELECT id FROM students WHERE user_id = :user_id"),
                {"user_id": current_user.id}
            )
            student = result.first()
            
            if student:
                query += " AND a.student_id = :student_id"
                params["student_id"] = student.id
            else:
                # Si no es profesor ni estudiante, no debería ver asistencias
                return []
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY a.date DESC, u.full_name LIMIT :limit OFFSET :skip"
    
    result = db.execute(text(query), params)
    attendances = result.fetchall()
    
    return [
        AttendanceDetailResponse(
            id=attendance.id,
            student_id=attendance.student_id,
            course_id=attendance.course_id,
            date=attendance.date,
            status=attendance.status,
            notes=attendance.notes,
            student_name=attendance.student_name,
            student_code=attendance.student_code,
            subject_name=attendance.subject_name,
            teacher_name=attendance.teacher_name,
            group_name=attendance.group_name
        )
        for attendance in attendances
    ]

@router.get("/{attendance_id}", response_model=AttendanceDetailResponse)
async def read_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener registro de asistencia por ID con detalles completos"""
    # Verificar permisos (solo administradores, profesor del curso o el propio estudiante)
    if not current_user.is_superuser:
        # Verificar si es profesor del curso
        result = db.execute(
            text("""
            SELECT a.id 
            FROM attendances a
            JOIN courses c ON a.course_id = c.id
            JOIN teachers t ON c.teacher_id = t.id
            WHERE a.id = :attendance_id AND t.user_id = :user_id
            """),
            {"attendance_id": attendance_id, "user_id": current_user.id}
        )
        is_teacher = result.first() is not None
        
        # Verificar si es el estudiante
        result = db.execute(
            text("""
            SELECT a.id 
            FROM attendances a
            JOIN students s ON a.student_id = s.id
            WHERE a.id = :attendance_id AND s.user_id = :user_id
            """),
            {"attendance_id": attendance_id, "user_id": current_user.id}
        )
        is_student = result.first() is not None
        
        if not (is_teacher or is_student):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este registro de asistencia"
            )
    
    # Obtener el registro de asistencia con todos sus detalles
    result = db.execute(
        text("""
        SELECT a.id, a.student_id, a.course_id, a.date, a.status, a.notes,
               CONCAT(u.full_name) as student_name, s.student_code,
               sb.name as subject_name, 
               tu.full_name as teacher_name,
               gr.group_name
        FROM attendances a
        JOIN students s ON a.student_id = s.id
        JOIN users u ON s.user_id = u.id
        JOIN courses c ON a.course_id = c.id
        JOIN subjects sb ON c.subject_id = sb.id
        JOIN teachers t ON c.teacher_id = t.id
        JOIN users tu ON t.user_id = tu.id
        LEFT JOIN groups gr ON s.group_id = gr.id
        WHERE a.id = :attendance_id
        """),
        {"attendance_id": attendance_id}
    )
    
    attendance = result.first()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado"
        )
    
    return AttendanceDetailResponse(
        id=attendance.id,
        student_id=attendance.student_id,
        course_id=attendance.course_id,
        date=attendance.date,
        status=attendance.status,
        notes=attendance.notes,
        student_name=attendance.student_name,
        student_code=attendance.student_code,
        subject_name=attendance.subject_name,
        teacher_name=attendance.teacher_name,
        group_name=attendance.group_name
    )

@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden actualizar asistencias
):
    """Actualizar registro de asistencia (solo profesores)"""
    # Verificar que el registro de asistencia existe
    result = db.execute(
        text("SELECT id, course_id FROM attendances WHERE id = :attendance_id"),
        {"attendance_id": attendance_id}
    )
    attendance = result.first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado"
        )
    
    # Verificar que el profesor tiene permiso para modificar este registro
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": attendance.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este registro de asistencia"
        )
    
    # Construir la consulta SQL para actualizar solo los campos proporcionados
    update_fields = []
    params = {"attendance_id": attendance_id}
    
    if attendance_data.status is not None:
        update_fields.append("status = :status")
        params["status"] = attendance_data.status.value
    
    if attendance_data.notes is not None:
        update_fields.append("notes = :notes")
        params["notes"] = attendance_data.notes
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    
    # Actualizar registro de asistencia usando SQL directo
    query = f"UPDATE attendances SET {', '.join(update_fields)} WHERE id = :attendance_id"
    db.execute(text(query), params)
    db.commit()
    
    # Obtener el registro de asistencia actualizado
    result = db.execute(
        text("""
        SELECT id, student_id, course_id, date, status, notes
        FROM attendances 
        WHERE id = :attendance_id
        """),
        {"attendance_id": attendance_id}
    )
    updated_attendance = result.first()
    
    return AttendanceResponse(
        id=updated_attendance.id,
        student_id=updated_attendance.student_id,
        course_id=updated_attendance.course_id,
        date=updated_attendance.date,
        status=updated_attendance.status,
        notes=updated_attendance.notes
    )

@router.delete("/{attendance_id}", status_code=status.HTTP_200_OK)
async def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_teacher),  # Solo profesores pueden eliminar asistencias
):
    """Eliminar registro de asistencia (solo profesores)"""
    # Verificar que el registro de asistencia existe
    result = db.execute(
        text("SELECT id, course_id FROM attendances WHERE id = :attendance_id"),
        {"attendance_id": attendance_id}
    )
    attendance = result.first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado"
        )
    
    # Verificar que el profesor tiene permiso para eliminar este registro
    # (debe ser el profesor asignado al curso)
    result = db.execute(
        text("""
        SELECT c.id 
        FROM courses c
        JOIN teachers t ON c.teacher_id = t.id
        WHERE c.id = :course_id AND t.user_id = :user_id
        """),
        {"course_id": attendance.course_id, "user_id": current_user.id}
    )
    if not result.first() and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este registro de asistencia"
        )
    
    # Eliminar registro de asistencia usando SQL directo
    db.execute(
        text("DELETE FROM attendances WHERE id = :attendance_id"),
        {"attendance_id": attendance_id}
    )
    db.commit()
    
    return {"message": "Registro de asistencia eliminado correctamente"}


class AttendanceStats(BaseModel):
    total_classes: int
    present_count: int
    absent_count: int
    late_count: int
    excused_count: int
    attendance_rate: float

@router.get("/stats/course/{course_id}", response_model=AttendanceStats)
async def get_course_attendance_stats(
    course_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener estadísticas de asistencia para un curso específico"""
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar permisos (solo administradores, profesor del curso o estudiantes del curso)
    if not current_user.is_superuser:
        # Verificar si es profesor del curso
        result = db.execute(
            text("""
            SELECT c.id 
            FROM courses c
            JOIN teachers t ON c.teacher_id = t.id
            WHERE c.id = :course_id AND t.user_id = :user_id
            """),
            {"course_id": course_id, "user_id": current_user.id}
        )
        is_teacher = result.first() is not None
        
        # Verificar si es estudiante del curso
        result = db.execute(
            text("""
            SELECT c.id 
            FROM courses c
            JOIN students s ON c.group_id = s.group_id
            WHERE c.id = :course_id AND s.user_id = :user_id
            """),
            {"course_id": course_id, "user_id": current_user.id}
        )
        is_student = result.first() is not None
        
        if not (is_teacher or is_student):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver estas estadísticas"
            )
    
    # Construir consulta para obtener estadísticas
    query = """
    SELECT 
        COUNT(*) as total_classes,
        SUM(CASE WHEN status = 'presente' THEN 1 ELSE 0 END) as present_count,
        SUM(CASE WHEN status = 'ausente' THEN 1 ELSE 0 END) as absent_count,
        SUM(CASE WHEN status = 'tarde' THEN 1 ELSE 0 END) as late_count,
        SUM(CASE WHEN status = 'justificado' THEN 1 ELSE 0 END) as excused_count
    FROM attendances
    WHERE course_id = :course_id
    """
    
    params = {"course_id": course_id}
    
    # Aplicar filtros de fecha si se proporcionan
    if date_from is not None:
        query += " AND date >= :date_from"
        params["date_from"] = date_from
    
    if date_to is not None:
        query += " AND date <= :date_to"
        params["date_to"] = date_to
    
    result = db.execute(text(query), params)
    stats = result.first()
    
    # Calcular tasa de asistencia (presentes + justificados) / total
    total_classes = int(stats.total_classes) if stats.total_classes else 0
    present_count = int(stats.present_count) if stats.present_count else 0
    absent_count = int(stats.absent_count) if stats.absent_count else 0
    late_count = int(stats.late_count) if stats.late_count else 0
    excused_count = int(stats.excused_count) if stats.excused_count else 0
    
    attendance_rate = 0.0
    if total_classes > 0:
        attendance_rate = (present_count + excused_count) / total_classes * 100
    
    return AttendanceStats(
        total_classes=total_classes,
        present_count=present_count,
        absent_count=absent_count,
        late_count=late_count,
        excused_count=excused_count,
        attendance_rate=attendance_rate
    )

@router.get("/stats/student/{student_id}/course/{course_id}", response_model=AttendanceStats)
async def get_student_course_attendance_stats(
    student_id: int,
    course_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """Obtener estadísticas de asistencia para un estudiante específico en un curso"""
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
    
    # Verificar que el curso existe
    result = db.execute(
        text("SELECT id FROM courses WHERE id = :course_id"),
        {"course_id": course_id}
    )
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )
    
    # Verificar permisos (solo administradores, profesor del curso o el propio estudiante)
    if not current_user.is_superuser and current_user.id != student.user_id:
        # Verificar si es profesor del curso
        result = db.execute(
            text("""
            SELECT c.id 
            FROM courses c
            JOIN teachers t ON c.teacher_id = t.id
            WHERE c.id = :course_id AND t.user_id = :user_id
            """),
            {"course_id": course_id, "user_id": current_user.id}
        )
        is_teacher = result.first() is not None
        
        if not is_teacher:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver estas estadísticas"
            )
    
    # Construir consulta para obtener estadísticas
    query = """
    SELECT 
        COUNT(*) as total_classes,
        SUM(CASE WHEN status = 'presente' THEN 1 ELSE 0 END) as present_count,
        SUM(CASE WHEN status = 'ausente' THEN 1 ELSE 0 END) as absent_count,
        SUM(CASE WHEN status = 'tarde' THEN 1 ELSE 0 END) as late_count,
        SUM(CASE WHEN status = 'justificado' THEN 1 ELSE 0 END) as excused_count
    FROM attendances
    WHERE course_id = :course_id AND student_id = :student_id
    """
    
    params = {"course_id": course_id, "student_id": student_id}
    
    # Aplicar filtros de fecha si se proporcionan
    if date_from is not None:
        query += " AND date >= :date_from"
        params["date_from"] = date_from
    
    if date_to is not None:
        query += " AND date <= :date_to"
        params["date_to"] = date_to
    
    result = db.execute(text(query), params)
    stats = result.first()
    
    # Calcular tasa de asistencia (presentes + justificados) / total
    total_classes = int(stats.total_classes) if stats.total_classes else 0
    present_count = int(stats.present_count) if stats.present_count else 0
    absent_count = int(stats.absent_count) if stats.absent_count else 0
    late_count = int(stats.late_count) if stats.late_count else 0
    excused_count = int(stats.excused_count) if stats.excused_count else 0
    
    attendance_rate = 0.0
    if total_classes > 0:
        attendance_rate = (present_count + excused_count) / total_classes * 100
    
    return AttendanceStats(
        total_classes=total_classes,
        present_count=present_count,
        absent_count=absent_count,
        late_count=late_count,
        excused_count=excused_count,
        attendance_rate=attendance_rate
    )