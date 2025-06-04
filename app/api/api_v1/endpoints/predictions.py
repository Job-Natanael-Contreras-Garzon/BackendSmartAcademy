# app/api/api_v1/endpoints/predictions.py
from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config.database import get_db
from app.core.security import get_current_active_user
from app.services.ml_service import MLService

router = APIRouter()

@router.post("/train")
def train_model(
    model_type: str = "random_forest",
    advanced: bool = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Entrena el modelo de Machine Learning.
    
    - **model_type**: Tipo de modelo a entrenar (random_forest, linear_regression, gradient_boosting)
    - **advanced**: Si es True, utiliza el método avanzado de entrenamiento con más características
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        
    ml_service = MLService(db)
    
    if advanced:
        result = ml_service.advanced_train_model(model_type)
    else:
        result = ml_service.train_model(model_type)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.get("/student/{student_id}")
def predict_student_performance(
    student_id: int,
    course_id: Optional[int] = None,
    advanced: bool = True,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Predice el rendimiento de un estudiante.
    
    - **student_id**: ID del estudiante para predecir rendimiento
    - **course_id**: ID del curso (opcional), si se especifica, solo predice para este curso
    - **advanced**: Si es True, utiliza el método avanzado de predicción con más factores
    """
    ml_service = MLService(db)
    
    if advanced:
        result = ml_service.predict_advanced(student_id, course_id)
    else:
        result = ml_service.predict_performance(student_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.get("/dashboard/stats")
def get_prediction_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene estadísticas generales para el dashboard de predicciones.
    
    Devuelve métricas agregadas como distribuciones de rendimiento, factores de riesgo comunes,
    y tendencias generales.
    """
    # Verificar que el usuario tiene permisos (profesores o admin)
    if not (current_user.is_superuser or current_user.role == "teacher"):
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para acceder a las estadísticas de predicciones"
        )
        
    # Inicializar servicio ML
    ml_service = MLService(db)
    
    # Esta es una implementación básica que analizará varias predicciones
    # y devolverá estadísticas agregadas
    try:
        import os
        import json
        import pandas as pd
        from collections import Counter
        
        # Buscar archivos de predicciones guardados
        prediction_files = []
        if os.path.exists(ml_service.history_path):
            prediction_files = [f for f in os.listdir(ml_service.history_path) if f.endswith('.json')]
        
        # Si no hay predicciones guardadas, devolver estadísticas simuladas
        if not prediction_files:
            return {
                "message": "No hay suficientes predicciones guardadas para generar estadísticas",
                "suggestion": "Realiza predicciones para varios estudiantes primero"
            }
        
        # Cargar y combinar predicciones
        all_predictions = []
        for file in prediction_files[-10:]:  # Usar las 10 predicciones más recientes
            try:
                with open(os.path.join(ml_service.history_path, file), 'r') as f:
                    preds = json.load(f)
                    if isinstance(preds, list):
                        all_predictions.extend(preds)
            except Exception as e:
                continue
        
        if not all_predictions:
            return {
                "message": "No se pudieron cargar predicciones guardadas",
                "suggestion": "Realiza nuevas predicciones"
            }
            
        # Convertir a DataFrame para análisis
        df = pd.DataFrame(all_predictions)
        
        # Estadísticas de rendimiento
        performance_dist = df['performance_category'].value_counts().to_dict()
        risk_levels = df['risk_level'].value_counts().to_dict()
        
        # Factores de riesgo comunes
        risk_factors = [factor for sublist in df['risk_factors'].tolist() for factor in sublist]
        common_risks = Counter(risk_factors).most_common(5)
        
        # Asistencia vs rendimiento
        attendance_corr = df[['attendance_rate', 'predicted_grade']].corr().iloc[0, 1]
        
        # Participación vs rendimiento
        participation_corr = df[['participation_score', 'predicted_grade']].corr().iloc[0, 1]
        
        return {
            "total_predictions": len(df),
            "unique_students": df['student_id'].nunique(),
            "performance_distribution": performance_dist,
            "risk_level_distribution": risk_levels,
            "common_risk_factors": common_risks,
            "correlations": {
                "attendance_performance": round(float(attendance_corr), 2),
                "participation_performance": round(float(participation_corr), 2)
            }
        }
        
    except Exception as e:
        return {
            "message": "Error al generar estadísticas",
            "error": str(e)
        }

@router.get("/at-risk")
def get_at_risk_students(
    risk_level: str = "Alto",
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
) -> Any:
    """
    Obtiene lista de estudiantes en riesgo según predicciones previas.
    
    - **risk_level**: Nivel de riesgo a filtrar (Alto, Medio, Bajo)
    - **limit**: Número máximo de estudiantes a devolver
    """
    # Verificar permisos
    if not (current_user.is_superuser or current_user.role == "teacher"):
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para acceder a esta información"
        )
        
    ml_service = MLService(db)
    
    try:
        import os
        import json
        import pandas as pd
        
        # Buscar archivos de predicciones guardados
        prediction_files = []
        if os.path.exists(ml_service.history_path):
            prediction_files = [f for f in os.listdir(ml_service.history_path) if f.endswith('.json')]
        
        if not prediction_files:
            # Si no hay predicciones, realizar simulación con consulta directa
            # Iniciar predicciones para algunos estudiantes
            query = text("""
                SELECT s.id FROM students s
                ORDER BY s.id
                LIMIT :limit
            """)
            students = db.execute(query, {"limit": 5}).fetchall()
            
            for student in students:
                try:
                    ml_service.predict_advanced(student.id)
                except:
                    pass
                    
            # Intentar cargar nuevamente
            if os.path.exists(ml_service.history_path):
                prediction_files = [f for f in os.listdir(ml_service.history_path) if f.endswith('.json')]
        
        # Si aún no hay archivos, devolver mensaje
        if not prediction_files:
            return {
                "message": "No hay predicciones disponibles",
                "at_risk_students": []
            }
        
        # Cargar y combinar predicciones
        all_predictions = []
        for file in prediction_files[-20:]:  # Usar las 20 predicciones más recientes
            try:
                with open(os.path.join(ml_service.history_path, file), 'r') as f:
                    preds = json.load(f)
                    if isinstance(preds, list):
                        all_predictions.extend(preds)
            except Exception as e:
                continue
        
        if not all_predictions:
            return {
                "message": "No se pudieron cargar predicciones",
                "at_risk_students": []
            }
            
        # Filtrar por nivel de riesgo
        df = pd.DataFrame(all_predictions)
        at_risk = df[df['risk_level'] == risk_level]
        
        # Eliminar duplicados (mantener la predicción más reciente por estudiante)
        at_risk = at_risk.sort_values('course_name').drop_duplicates(['student_id', 'course_id'], keep='first')
        
        # Limitar número de resultados
        at_risk = at_risk.head(limit)
        
        # Convertir a lista de diccionarios
        result = at_risk.to_dict(orient='records')
        
        return {
            "risk_level": risk_level,
            "count": len(result),
            "at_risk_students": result
        }
        
    except Exception as e:
        return {
            "message": "Error al buscar estudiantes en riesgo",
            "error": str(e),
            "at_risk_students": []
        }