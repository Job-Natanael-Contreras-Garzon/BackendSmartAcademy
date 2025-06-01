from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, students, courses, predictions, dashboard, users, roles   

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(students.router, prefix="/students", tags=["Estudiantes"])
api_router.include_router(courses.router, prefix="/courses", tags=["Cursos"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predicciones"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])