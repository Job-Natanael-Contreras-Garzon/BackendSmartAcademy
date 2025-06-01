# app/api/api_v1/endpoints/predictions.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_active_user
from app.services.ml_service import MLService

router = APIRouter()

@router.post("/train")
def train_model(
    model_type: str = "random_forest",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Entrena el modelo de Machine Learning.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        
    ml_service = MLService(db)
    result = ml_service.train_model(model_type)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.get("/student/{student_id}")
def predict_student_performance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Predice el rendimiento de un estudiante.
    """
    ml_service = MLService(db)
    result = ml_service.predict_performance(student_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result