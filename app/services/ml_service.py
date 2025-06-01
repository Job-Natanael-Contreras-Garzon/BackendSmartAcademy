# app/services/ml_service.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.participation import Participation

class MLService:
    def __init__(self, db: Session):
        self.db = db
        self.model = None
        self.scaler = StandardScaler()
        
    def prepare_data(self, student_id: int = None):
        """
        Prepara datos para entrenamiento o predicción
        """
        # Obtener datos
        query = (
            self.db.query(
                Student.id.label('student_id'),
                Grade.value.label('grade'),
                Attendance.presence.label('attendance'),
                Participation.score.label('participation')
            )
            .join(Grade, Student.id == Grade.student_id)
            .join(Attendance, Student.id == Attendance.student_id)
            .join(Participation, Student.id == Participation.student_id)
        )
        
        if student_id:
            query = query.filter(Student.id == student_id)
            
        results = query.all()
        
        # Convertir a DataFrame
        df = pd.DataFrame([r._asdict() for r in results])
        
        if df.empty:
            return None, None
            
        # Agregación por estudiante
        grouped = df.groupby('student_id').agg({
            'grade': 'mean',
            'attendance': lambda x: (x.sum() / len(x)) * 100,  # Porcentaje de asistencia
            'participation': 'mean'
        }).reset_index()
        
        # Features y target
        X = grouped[['attendance', 'participation']]
        y = grouped['grade']
        
        return X, y
    
    def train_model(self, model_type="random_forest"):
        """
        Entrena el modelo con los datos existentes
        """
        X, y = self.prepare_data()
        
        if X is None or y is None:
            return {"error": "No hay suficientes datos para entrenar el modelo"}
        
        # Escalar características
        X_scaled = self.scaler.fit_transform(X)
        
        # Seleccionar tipo de modelo
        if model_type == "random_forest":
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            self.model = LinearRegression()
            
        # Entrenar modelo
        self.model.fit(X_scaled, y)
        
        return {"message": f"Modelo {model_type} entrenado correctamente"}
    
    def predict_performance(self, student_id: int):
        """
        Predice el rendimiento de un estudiante
        """
        if not self.model:
            self.train_model()
            
        X, _ = self.prepare_data(student_id)
        
        if X is None:
            return {"error": "No hay datos suficientes para este estudiante"}
            
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        
        # Categorizar el rendimiento
        category = "bajo"
        if prediction >= 70:
            category = "alto"
        elif prediction >= 50:
            category = "medio"
            
        return {
            "student_id": student_id,
            "predicted_grade": float(prediction),
            "performance_category": category
        }