# app/services/ml_service.py
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, List, Any, Tuple, Optional

from app.models.student import Student
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.participation import Participation
from app.models.course import Course

class MLService:
    def __init__(self, db: Session):
        self.db = db
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models"
        self.history_path = "prediction_history"
        
        # Crear directorios si no existen
        os.makedirs(self.model_path, exist_ok=True)
        os.makedirs(self.history_path, exist_ok=True)
        
    def prepare_data_advanced(self, student_id: int = None, course_id: int = None):
        """
        Prepara datos avanzados para entrenamiento o predicción con más características
        """
        # Extraer datos con SQL para más flexibilidad
        query = text("""
        SELECT 
            s.id AS student_id, 
            s.first_name,
            s.last_name,
            c.id AS course_id,
            c.name AS course_name,
            g.period,
            g.value AS grade,
            g.date_recorded,
            COALESCE(
                (SELECT AVG(a.present::int) 
                FROM attendances a 
                WHERE a.student_id = s.id AND a.course_id = c.id),
                0
            ) * 100 AS attendance_rate,
            COALESCE(
                (SELECT AVG(p.score) 
                FROM participations p 
                WHERE p.student_id = s.id AND p.course_id = c.id),
                0
            ) AS participation_score
        FROM 
            students s
        INNER JOIN 
            grades g ON s.id = g.student_id
        INNER JOIN 
            courses c ON g.course_id = c.id
        """)
        
        params = {}
        
        if student_id:
            query = text(query.text + " WHERE s.id = :student_id")
            params["student_id"] = student_id
            
            if course_id:
                query = text(query.text + " AND c.id = :course_id")
                params["course_id"] = course_id
        elif course_id:
            query = text(query.text + " WHERE c.id = :course_id")
            params["course_id"] = course_id
            
        query = text(query.text + " ORDER BY s.id, c.id, g.period")
        
        # Ejecutar consulta
        result = self.db.execute(query, params)
        data = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        if data.empty:
            return None, None, None
        
        # Crear características adicionales
        data = self._create_features(data)
        
        # Dividir en características y objetivo para cada estudiante o curso
        features_list = []
        targets_list = []
        metadata_list = []
        
        for (student_id, course_id), group in data.groupby(['student_id', 'course_id']):
            if len(group) < 2:  # Necesitamos al menos 2 periodos para hacer predicciones
                continue
                
            # Ordenar por periodo
            group = group.sort_values('period_num')
            
            # Crear características para el último periodo conocido
            last_row = group.iloc[-1]
            features = {
                'attendance_rate': last_row['attendance_rate'],
                'participation_score': last_row['participation_score'],
                'avg_grade': group['grade'].mean(),
                'grade_trend': group['grade_trend'].iloc[-1],
                'previous_grade': last_row['grade'],
                'attendance_trend': group['attendance_trend'].iloc[-1],
                'participation_trend': group['participation_trend'].iloc[-1],
            }
            
            # Objetivo: próxima calificación esperada
            target = last_row['grade']
            
            # Metadatos para interpretación
            metadata = {
                'student_id': int(student_id),
                'student_name': f"{last_row['first_name']} {last_row['last_name']}",
                'course_id': int(course_id),
                'course_name': last_row['course_name'],
                'last_period': last_row['period'],
                'last_grade': float(last_row['grade']),
            }
            
            features_list.append(features)
            targets_list.append(target)
            metadata_list.append(metadata)
        
        if not features_list:
            return None, None, None
            
        X = pd.DataFrame(features_list)
        y = pd.Series(targets_list)
        metadata = pd.DataFrame(metadata_list)
        
        return X, y, metadata
    
    def _create_features(self, data):
        """
        Crea características adicionales para el análisis
        """
        if data.empty:
            return data
            
        # Convertir periodo a valor numérico para análisis de tendencias
        periods = data['period'].unique()
        period_map = {period: i+1 for i, period in enumerate(sorted(periods))}
        data['period_num'] = data['period'].map(period_map)
        
        # Calcular tendencias para cada estudiante y curso
        trend_data = []
        
        for (student_id, course_id), group in data.groupby(['student_id', 'course_id']):
            group = group.sort_values('period_num')
            
            if len(group) >= 2:
                # Tendencias de calificaciones
                group['grade_trend'] = self._calculate_trend(group['period_num'], group['grade'])
                
                # Tendencias de asistencia
                group['attendance_trend'] = self._calculate_trend(group['period_num'], group['attendance_rate'])
                
                # Tendencias de participación
                group['participation_trend'] = self._calculate_trend(group['period_num'], group['participation_score'])
            else:
                # Si solo hay un periodo, no hay tendencia
                group['grade_trend'] = 0
                group['attendance_trend'] = 0
                group['participation_trend'] = 0
                
            trend_data.append(group)
        
        if trend_data:
            return pd.concat(trend_data)
        return data
    
    def _calculate_trend(self, x, y):
        """
        Calcula la tendencia (pendiente) de una serie de valores
        """
        if len(x) < 2:
            return 0
            
        x_vals = np.array(x)
        y_vals = np.array(y)
        
        # Calcular pendiente con regresión lineal simple
        slope = np.polyfit(x_vals, y_vals, 1)[0]
        return slope
        
    def prepare_data(self, student_id: int = None):
        """
        Prepara datos para entrenamiento o predicción (método legacy)
        """
        # Obtener datos
        query = (
            self.db.query(
                Student.id.label('student_id'),
                Grade.value.label('grade'),
                Attendance.present.label('attendance'),
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
        Entrena el modelo con los datos existentes (método legacy)
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
        
    def advanced_train_model(self, model_type="random_forest"):
        """
        Entrena un modelo avanzado con mayor precisión y validación
        """
        # Obtener datos avanzados
        X, y, metadata = self.prepare_data_advanced()
        
        if X is None or y is None:
            return {"error": "No hay suficientes datos para entrenar el modelo"}
            
        # Crear pipeline de preprocesamiento y modelado
        if model_type == "random_forest":
            model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        elif model_type == "gradient_boosting":
            model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
        else:
            model = LinearRegression()
        
        # Crear pipeline con escalado integrado
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        # División de datos para entrenamiento y validación
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entrenar modelo
        pipeline.fit(X_train, y_train)
        
        # Evaluar modelo
        train_score = pipeline.score(X_train, y_train)
        test_score = pipeline.score(X_test, y_test)
        y_pred = pipeline.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Guardar modelo
        self.model = pipeline
        model_file = f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.pkl"
        model_path = os.path.join(self.model_path, model_file)
        joblib.dump(pipeline, model_path)
        
        # Información sobre importancia de características (para Random Forest y Gradient Boosting)
        feature_importance = None
        if model_type in ["random_forest", "gradient_boosting"]:
            feature_importance = dict(zip(X.columns, model.feature_importances_))
        
        return {
            "message": f"Modelo {model_type} entrenado exitosamente",
            "model_file": model_file,
            "metrics": {
                "train_r2": float(train_score),
                "test_r2": float(test_score),
                "rmse": float(rmse)
            },
            "feature_importance": feature_importance
        }
    
    def predict_performance(self, student_id: int):
        """
        Método legacy para predecir el rendimiento de un estudiante
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
        
    def predict_advanced(self, student_id: int, course_id: int = None):
        """
        Método avanzado para predecir el rendimiento de un estudiante
        Proporciona análisis más detallado, incluyendo factores de riesgo y recomendaciones
        """
        # Verificar si hay un modelo disponible, o cargarlo si existe
        if not self.model:
            try:
                # Intentar cargar el modelo más reciente si existe
                model_files = [f for f in os.listdir(self.model_path) if f.endswith('.pkl')]
                if model_files:
                    # Ordenar por fecha y seleccionar el más reciente
                    model_files.sort()
                    latest_model = model_files[-1]
                    model_path = os.path.join(self.model_path, latest_model)
                    self.model = joblib.load(model_path)
                else:
                    # Si no existe, entrenar un nuevo modelo
                    result = self.advanced_train_model()
                    if "error" in result:
                        return result
            except Exception as e:
                # Si hay error al cargar, entrenar un nuevo modelo
                return self.advanced_train_model()
                
        # Preparar datos para la predicción
        X, _, metadata = self.prepare_data_advanced(student_id, course_id)
        
        if X is None or X.empty:
            # Intentar con método legacy como fallback
            legacy_result = self.predict_performance(student_id)
            if "error" in legacy_result:
                return {"error": "No hay datos suficientes para realizar predicciones para este estudiante"}
            return legacy_result
            
        # Hacer predicciones para cada curso del estudiante
        predictions = []
        courses = metadata['course_id'].unique()
        
        for course_id in courses:
            # Filtrar datos para el curso actual
            course_idx = metadata['course_id'] == course_id
            if not any(course_idx):
                continue
                
            # Metadatos del curso y estudiante
            course_meta = metadata[course_idx].iloc[0]
            features = X[course_idx]
            
            # Predicción
            try:
                predicted_grade = float(self.model.predict(features)[0])
                
                # Analizar factores de riesgo
                risk_factors = []
                risk_level = "Bajo"
                
                # Factor: Asistencia baja
                attendance_rate = features['attendance_rate'].values[0]
                if attendance_rate < 70:
                    risk_factors.append("Asistencia muy baja (menos del 70%)")
                    risk_level = "Alto"
                elif attendance_rate < 85:
                    risk_factors.append("Asistencia por debajo del promedio")
                    if risk_level != "Alto":
                        risk_level = "Medio"
                
                # Factor: Participación baja
                participation = features['participation_score'].values[0]
                if participation < 4:
                    risk_factors.append("Participación muy baja")
                    risk_level = "Alto"
                elif participation < 6:
                    risk_factors.append("Participación por debajo del promedio")
                    if risk_level != "Alto":
                        risk_level = "Medio"
                    
                # Factor: Tendencia negativa en calificaciones
                grade_trend = features['grade_trend'].values[0]
                if grade_trend < -0.5:
                    risk_factors.append("Tendencia fuertemente negativa en calificaciones")
                    risk_level = "Alto"
                elif grade_trend < -0.2:
                    risk_factors.append("Calificaciones en descenso")
                    if risk_level != "Alto":
                        risk_level = "Medio"
                        
                # Calcular diferencia con rendimiento actual
                current_grade = float(course_meta['last_grade'])
                grade_difference = predicted_grade - current_grade
                trend_direction = "mantener" if abs(grade_difference) < 0.5 else "subir" if grade_difference > 0 else "bajar"
                
                # Determinar categoría de rendimiento
                if predicted_grade >= 8.5:
                    performance_category = "Excelente"
                elif predicted_grade >= 7.0:
                    performance_category = "Bueno"
                elif predicted_grade >= 5.0:
                    performance_category = "Aceptable"
                else:
                    performance_category = "Bajo"
                    if risk_level != "Alto":
                        risk_level = "Medio"
                
                # Generar recomendaciones personalizadas
                recommendations = []
                if "Asistencia" in ''.join(risk_factors):
                    recommendations.append("Mejorar la asistencia a clases")
                if "Participación" in ''.join(risk_factors):
                    recommendations.append("Incrementar la participación en el aula")
                if "calificaciones" in ''.join(risk_factors).lower():
                    recommendations.append("Reforzar los temas donde hay dificultades")
                if predicted_grade < 5.0:
                    recommendations.append("Programar tutorías de refuerzo")
                
                # Si no hay riesgos específicos pero el rendimiento es bajo
                if not risk_factors and predicted_grade < 7.0:
                    recommendations.append("Revisar estrategias de estudio")
                
                # Si el desempeño es bueno pero aún puede mejorar
                if not risk_factors and predicted_grade >= 7.0 and predicted_grade < 9.0:
                    recommendations.append("Continuar con el buen desempeño. Considera participar en actividades adicionales")
                
                # Agregar la predicción a la lista
                predictions.append({
                    "student_id": int(course_meta['student_id']),
                    "student_name": course_meta['student_name'],
                    "course_id": int(course_meta['course_id']),
                    "course_name": course_meta['course_name'],
                    "current_grade": current_grade,
                    "predicted_grade": round(predicted_grade, 1),
                    "grade_difference": round(grade_difference, 1),
                    "trend_direction": trend_direction,
                    "performance_category": performance_category,
                    "risk_level": risk_level,
                    "risk_factors": risk_factors,
                    "recommendations": recommendations,
                    "attendance_rate": round(float(attendance_rate), 1),
                    "participation_score": round(float(participation), 1)
                })
                
            except Exception as e:
                # Si hay error en la predicción para este curso, continuar con el siguiente
                print(f"Error en predicción para curso {course_id}: {e}")
                continue
        
        # Si no se pudo predecir ningún curso
        if not predictions:
            return {"error": "No se pudieron realizar predicciones para este estudiante", "details": "Datos insuficientes"}
        
        # Si se solicitó un curso específico pero no hay predicciones para él
        if course_id is not None and not any(p["course_id"] == course_id for p in predictions):
            return {"error": f"No se pudo realizar la predicción para el curso {course_id}", "details": "Datos insuficientes"}
        
        # Si se solicitó un curso específico, filtrar solo ese curso
        if course_id is not None:
            predictions = [p for p in predictions if p["course_id"] == course_id]
        
        # Guardar predicciones en historial (opcional)
        try:
            filename = f"prediction_student_{student_id}_{datetime.now().strftime('%Y%m%d%H%M')}.json"
            filepath = os.path.join(self.history_path, filename)
            with open(filepath, 'w') as f:
                import json
                json.dump(predictions, f)
        except Exception as e:
            # Si falla el guardado, no afecta a la respuesta
            pass
            
        return {
            "student_id": student_id,
            "prediction_count": len(predictions),
            "predictions": predictions,
            "prediction_date": datetime.now().isoformat()
        }