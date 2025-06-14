from fastapi import APIRouter

from app.api.api_v1.endpoints import (auth, user, role, student, teacher, 
                                       group, course, subject, period, grade,
                                       attendance, tutor, tuition, notification,
                                       dashboard, predictions) # device - comentado temporalmente

api_router = APIRouter()

# Autenticación y gestión de usuarios
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(user.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(role.router, prefix="/roles", tags=["Roles"])

# Estructura académica
api_router.include_router(group.router, prefix="/groups", tags=["Grupos"])
api_router.include_router(period.router, prefix="/periods", tags=["Periodos"])
api_router.include_router(subject.router, prefix="/subjects", tags=["Materias"])

# Participantes
api_router.include_router(student.router, prefix="/students", tags=["Estudiantes"])
api_router.include_router(teacher.router, prefix="/teachers", tags=["Profesores"])

# Asignaciones y cursos
api_router.include_router(course.router, prefix="/courses", tags=["Cursos"])
api_router.include_router(grade.router, prefix="/grades", tags=["Calificaciones"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Asistencias"])

# Relaciones tutor-estudiante
api_router.include_router(tutor.router, prefix="/tutors", tags=["Tutores"])

# Matrículas y pagos
api_router.include_router(tuition.router, prefix="/tuitions", tags=["Matrículas y Pagos"])

# Notificaciones
api_router.include_router(notification.router, prefix="/notifications", tags=["Notificaciones"])

# Dashboard y estadísticas
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Predicciones académicas
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predicciones"])

# Dispositivos móviles y preferencias de notificaciones - comentado temporalmente
# api_router.include_router(device.router, prefix="/devices", tags=["Dispositivos"])