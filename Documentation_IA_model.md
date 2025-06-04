# Documentación Técnica: Sistema Smart Academy y Modelo de IA

## 1. Introducción

### 1.1. Propósito del Documento
Este documento proporciona una descripción técnica detallada del sistema Smart Academy, con un enfoque especial en el modelo de Inteligencia Artificial (IA) implementado para la predicción del rendimiento académico de los estudiantes. Su objetivo es servir como referencia para desarrolladores, administradores del sistema, analistas de datos y otras partes interesadas que necesiten comprender la arquitectura, el funcionamiento interno, los componentes de IA del sistema, y los detalles operativos del modelo.

### 1.2. Visión General del Sistema Smart Academy
Smart Academy es una plataforma de gestión académica diseñada para [Describir brevemente el propósito principal de Smart Academy, ej: optimizar la administración educativa, mejorar la experiencia de aprendizaje, etc.]. El sistema integra diversas funcionalidades, incluyendo gestión de usuarios, cursos, calificaciones, y un módulo de IA que ofrece predicciones sobre el desempeño estudiantil para facilitar intervenciones tempranas y personalizadas. Este módulo de IA utiliza datos históricos y simulados (descritos en `Dataset_utilizado.md`) para generar dichas predicciones.

## 2. Arquitectura del Sistema

### 2.1. Componentes Principales
El sistema Smart Academy se compone de los siguientes elementos clave:
-   **Backend (API):** Desarrollado en FastAPI (Python), maneja la lógica de negocio, la gestión de datos y la comunicación con la base de datos y los clientes (frontend, aplicaciones móviles, etc.).
-   **Base de Datos:** Se utiliza PostgreSQL para el almacenamiento persistente de todos los datos de la aplicación, incluyendo perfiles de usuario, información académica, y datos relevantes para el modelo de IA.
-   **Modelo de IA:** Un componente integrado dentro del backend que procesa datos históricos y actuales para generar predicciones. Su lógica reside en servicios específicos y utiliza modelos entrenados.

### 2.2. Tecnologías Utilizadas
-   **Lenguaje de Programación (Backend):** Python 3.x
-   **Framework Backend:** FastAPI
-   **Base de Datos:** PostgreSQL
-   **Autenticación:** Tokens JWT (JSON Web Tokens) y sistema de roles (administrador, superusuario, profesor, estudiante, padre).
-   **Librerías de IA:** [Especificar librerías, ej: Scikit-learn, TensorFlow, PyTorch, Pandas, NumPy]
-   **Servidor Web (para FastAPI):** Uvicorn con Gunicorn (o similar)

### 2.3. Flujo de Datos General
[Describir brevemente o insertar un diagrama simple del flujo de datos. Ej: Cliente -> API (FastAPI) -> Lógica de Negocio / Modelo de IA -> Base de Datos (PostgreSQL) -> API -> Cliente. Detallar cómo el modelo de IA interactúa con la base de datos para obtener features y cómo se exponen las predicciones a través de la API.]

## 3. Modelo de Inteligencia Artificial: Predicción de Rendimiento Académico

### 3.1. Objetivo del Modelo
El principal objetivo del modelo de IA es predecir el rendimiento académico futuro de los estudiantes. Esto puede incluir:
-   Predicción de calificaciones en futuras asignaturas o periodos.
-   Identificación de estudiantes en riesgo de bajo rendimiento o deserción.
-   [Otros objetivos específicos del modelo]

Estas predicciones están diseñadas para ayudar a educadores y administradores a tomar decisiones proactivas y ofrecer apoyo personalizado.

### 3.2. Tipo de Modelo y Algoritmo
-   **Tipo de Problema:** [Especificar, ej: Clasificación (para categorías de riesgo) o Regresión (para predecir calificaciones numéricas)]
-   **Algoritmo(s) Seleccionado(s):** [Especificar el algoritmo o algoritmos utilizados, ej: Random Forest, Gradient Boosting, Redes Neuronales (LSTM, FeedForward), Regresión Logística, SVM, etc. Justificar brevemente la elección si es posible.]

### 3.3. Datos Utilizados

#### 3.3.1. Fuentes de Datos
El modelo se entrena y opera utilizando el dataset simulado descrito en `Dataset_utilizado.md`. Este dataset incluye información detallada sobre:
-   Usuarios (estudiantes, profesores)
-   Cursos y Asignaturas
-   Periodos Académicos
-   Calificaciones Históricas
-   Registros de Asistencia
-   Registros de Participación

#### 3.3.2. Características (Features) Relevantes
Las características seleccionadas para el entrenamiento del modelo incluyen (pero no se limitan a):
-   **Historial Académico:** Calificaciones previas, promedio general, calificaciones por asignatura/área.
-   **Comportamiento del Estudiante:** Porcentaje de asistencia, frecuencia y calidad de participación.
-   **Información Demográfica del Estudiante:** [Especificar si se usa, ej: edad, género (considerar implicaciones éticas)].
-   **Información del Curso/Contexto:** Nivel del curso, tipo de asignatura, profesor (si es relevante y no introduce sesgo).
-   **Tendencias Temporales:** Evolución del rendimiento a lo largo de diferentes periodos académicos.
-   [Listar otras características específicas utilizadas]

#### 3.3.3. Variable Objetivo (Target)
La variable objetivo que el modelo predice es:
-   [Especificar la variable objetivo, ej: Calificación final en una asignatura específica para el próximo periodo, probabilidad de obtener una calificación por debajo de X, categoría de riesgo (alto, medio, bajo)].

### 3.4. Preprocesamiento de Datos

#### 3.4.1. Limpieza de Datos
-   Manejo de valores faltantes: [Especificar estrategia, ej: imputación (media, mediana, moda), eliminación de registros/columnas].
-   Detección y tratamiento de outliers: [Especificar estrategia, ej: eliminación, transformación, capping].
-   Validación de consistencia de datos.

#### 3.4.2. Transformación de Características
-   **Encoding de Variables Categóricas:** [Especificar método, ej: One-Hot Encoding, Label Encoding, Target Encoding].
-   **Escalado/Normalización de Variables Numéricas:** [Especificar método, ej: StandardScaler, MinMaxScaler] para algoritmos sensibles a la escala.
-   **Ingeniería de Características (Feature Engineering):** Creación de nuevas características a partir de las existentes (ej: promedios móviles de calificaciones, tasas de cambio en asistencia). [Describir las nuevas características creadas].

#### 3.4.3. División del Dataset
El dataset se divide en los siguientes conjuntos para el entrenamiento y evaluación del modelo:
-   **Conjunto de Entrenamiento (Training Set):** [Especificar porcentaje, ej: 70-80%] - Utilizado para entrenar el modelo.
-   **Conjunto de Validación (Validation Set):** [Especificar porcentaje, ej: 10-15%] - Utilizado para ajustar hiperparámetros y evitar overfitting durante el entrenamiento.
-   **Conjunto de Prueba (Test Set):** [Especificar porcentaje, ej: 10-15%] - Utilizado para evaluar el rendimiento final del modelo en datos no vistos.
-   **Estrategia de División:** [Especificar, ej: Aleatoria, Estratificada (si hay desbalance de clases), Basada en tiempo (para series temporales)].

### 3.5. Entrenamiento del Modelo

#### 3.5.1. Librerías/Frameworks
-   [Especificar las librerías principales, ej: Scikit-learn para modelos clásicos, TensorFlow/Keras o PyTorch para redes neuronales].

#### 3.5.2. Proceso de Entrenamiento
-   [Describir el proceso. Ej: Se entrena el algoritmo X utilizando el conjunto de entrenamiento. Se utiliza el conjunto de Validación para monitorear el rendimiento y aplicar técnicas como Early Stopping si es una red neuronal].
-   **Función de Pérdida (Loss Function):** [Especificar la función de pérdida utilizada, ej: Mean Squared Error para regresión, Cross-Entropy para clasificación].
-   **Optimizador (Optimizer):** [Especificar si aplica, ej: Adam, SGD para redes neuronales].

#### 3.5.3. Optimización de Hiperparámetros
-   [Describir el método, ej: Grid Search, Random Search, Bayesian Optimization].
-   [Listar los principales hiperparámetros ajustados y sus rangos de búsqueda/valores óptimos encontrados].

### 3.6. Evaluación del Modelo

#### 3.6.1. Métricas de Evaluación
Se utilizan las siguientes métricas para evaluar el rendimiento del modelo:
-   **Para problemas de Clasificación:**
    -   Accuracy (Exactitud)
    -   Precision (Precisión)
    -   Recall (Sensibilidad)
    -   F1-Score
    -   AUC-ROC (Área bajo la curva ROC)
    -   Matriz de Confusión
-   **Para problemas de Regresión:**
    -   Mean Absolute Error (MAE)
    -   Mean Squared Error (MSE)
    -   Root Mean Squared Error (RMSE)
    -   R-squared (Coeficiente de Determinación)
-   [Especificar las métricas primarias utilizadas para la selección del modelo].

#### 3.6.2. Resultados y Validación
-   [Presentar los resultados obtenidos en el conjunto de prueba para las métricas seleccionadas].
-   [Discutir la validez de los resultados y la capacidad de generalización del modelo].
-   **Técnicas de Validación Cruzada (Cross-Validation):** [Especificar si se usó y qué tipo, ej: K-Fold Cross-Validation, para asegurar la robustez del modelo].

### 3.7. Implementación, Despliegue y Ciclo de Vida del Modelo (MLOps)

#### 3.7.1. API Endpoints para Predicciones
El modelo de IA es accesible a través de los siguientes endpoints de la API:
-   `GET /api/v1/students/{student_id}/predict_performance`: Obtiene la predicción de rendimiento para un estudiante específico.
    -   **Request:** `student_id` (Path parameter).
    -   **Response:** [Describir la estructura de la respuesta JSON, ej: `{ "student_id": "...", "prediction": { "score": 0.85, "risk_level": "low" }, "timestamp": "..." }`].
-   `GET /api/v1/dashboard/prediction_stats`: Obtiene estadísticas agregadas sobre las predicciones (potencialmente para administradores o profesores).
    -   **Response:** [Describir la estructura de la respuesta JSON].
-   [Listar otros endpoints relevantes si existen].

#### 3.7.2. Ubicación del Código y Artefactos del Modelo
-   El código fuente relacionado con el modelo de IA (preprocesamiento, entrenamiento, predicción) se encuentra principalmente en:
    -   `app/services/ml_service.py` (o la ruta correspondiente donde reside la lógica del modelo).
    -   `app/scripts/populate_db.py` (para la generación de datos de entrenamiento/prueba).
-   Los artefactos del modelo (modelos serializados/guardados) se almacenan en:
    -   [Ej: `models/trained_model.pkl` o `models/my_model.h5`, especificar convención de nombrado y versionado si existe].

#### 3.7.3. Monitoreo y Reentrenamiento

##### 3.7.3.1. Estrategia de Monitoreo
-   [Describir cómo se monitorea el rendimiento del modelo en producción, ej: seguimiento de la desviación de las predicciones (prediction drift), degradación de las métricas clave con nuevos datos, monitoreo de la calidad de los datos de entrada].
-   [Herramientas o dashboards utilizados para el monitoreo, ej: Grafana, Prometheus, logs estructurados].

##### 3.7.3.2. Criterios y Proceso de Reentrenamiento
-   **Criterios para el Reentrenamiento:**
    -   Degradación del rendimiento del modelo por debajo de un umbral predefinido en métricas clave.
    -   Disponibilidad de una cantidad significativa de nuevos datos etiquetados.
    -   Detección de cambios significativos en la distribución de los datos de entrada (data drift) o en la relación entre características y la variable objetivo (concept drift).
    -   Programación periódica (ej: cada semestre académico, anualmente) como medida proactiva.
    -   Actualizaciones en la lógica de negocio o en los objetivos que el modelo debe cumplir.
-   **Proceso de Reentrenamiento:**
    -   [Describir el pipeline de reentrenamiento automatizado o manual, ej: recolección y versionado de nuevos datos, re-ejecución del pipeline de preprocesamiento y entrenamiento, evaluación exhaustiva del nuevo modelo candidato (comparándolo con el modelo en producción), y despliegue controlado (ej: canary, shadow mode) de la nueva versión del modelo si supera a la actual. Considerar el versionado de datos, código y modelos].

## 4. Consideraciones Éticas y Limitaciones

### 4.1. Sesgos Potenciales en los Datos y el Modelo
-   **Sesgos en los Datos:** El dataset simulado, aunque diseñado para ser realista, podría no capturar todas las diversidades y complejidades del mundo real, o podría inadvertidamente codificar sesgos si los parámetros de simulación no son cuidadosamente balanceados. [Discutir sesgos potenciales relacionados con género, nivel socioeconómico (si se simula), características del grupo mayoritario vs minoritario, etc.].
-   **Sesgos Algorítmicos:** El algoritmo elegido podría aprender y potencialmente amplificar sesgos presentes en los datos de entrenamiento.
-   **Mitigación:** [Describir las medidas tomadas o planeadas para identificar, medir y mitigar sesgos, ej: análisis de equidad (fairness analysis) utilizando métricas específicas por subgrupos, técnicas de preprocesamiento (re-muestreo, re-ponderación), algoritmos conscientes del sesgo (in-processing), o post-procesamiento de predicciones. Importancia de la transparencia y la revisión humana].

### 4.2. Limitaciones del Modelo Actual
-   El modelo se basa en datos simulados, lo que puede no reflejar perfectamente escenarios del mundo real hasta que se valide y reentrene con datos reales.
-   Las predicciones son probabilísticas y no determinísticas; deben interpretarse con cautela y no como verdades absolutas.
-   La precisión del modelo puede variar para diferentes subgrupos de estudiantes.
-   [Otras limitaciones específicas del modelo o del enfoque adoptado, ej: dependencia de la calidad de los datos de entrada, no considera factores externos no medidos].

### 4.3. Interpretación y Uso Responsable de las Predicciones
-   Las predicciones deben ser utilizadas como una herramienta de apoyo para la toma de decisiones por parte de educadores y personal cualificado, y no como el único factor determinante para acciones críticas (ej: asignación de recursos, intervenciones disciplinarias).
-   Es crucial que los usuarios finales (profesores, administradores) reciban capacitación sobre cómo interpretar las predicciones, comprendiendo su naturaleza probabilística y sus limitaciones.
-   **Explicabilidad del Modelo (XAI):** [Considerar y describir si se han implementado o se planean implementar técnicas para explicar las predicciones del modelo (ej: SHAP, LIME) para aumentar la transparencia y la confianza].

## 5. Futuras Mejoras

Esta sección debe cubrir tanto el sistema general como el modelo de IA.

-   **Sistema General:**
    -   [Especificar mejoras planeadas para el sistema, ej: nuevas funcionalidades, mejoras de UI/UX, optimizaciones de rendimiento del backend].
-   **Modelo de IA:**
    -   Incorporación y validación con datos reales una vez que el sistema esté en producción y se recopilen suficientes datos.
    -   Exploración de algoritmos de IA más avanzados o arquitecturas de modelos (ej: modelos de series temporales más sofisticados, GNNs si se modelan interacciones).
    -   Mejora continua de la interpretabilidad y explicabilidad del modelo.
    -   Integración de más fuentes de datos relevantes (ej: interacciones con la plataforma de e-learning, datos socioemocionales si están disponibles y se manejan éticamente).
    -   Desarrollo de un sistema de feedback robusto para que los usuarios puedan reportar la precisión y utilidad de las predicciones, alimentando el ciclo de mejora.
    -   Automatización completa y robusta del pipeline de MLOps (monitoreo continuo, alertas, reentrenamiento automatizado, versionado, despliegue seguro).
    -   Investigación continua sobre técnicas de mitigación de sesgos y promoción de la equidad.

## 6. Apéndice (Opcional)

-   Diagramas de arquitectura detallados del sistema.
-   Diagramas detallados del flujo de datos del modelo.
-   Ejemplos de código clave para el preprocesamiento, entrenamiento o predicción.
-   Resultados detallados de la evaluación del modelo, incluyendo análisis por subgrupos.
-   Glosario de términos técnicos.