# Documentación Técnica: Sistema Smart Academy y Modelo de IA

## 1. Introducción

### 1.1. Propósito del Documento
Este documento proporciona una descripción técnica detallada del sistema Smart Academy, con un enfoque especial en el modelo de Inteligencia Artificial (IA) implementado para la predicción del rendimiento académico de los estudiantes. Su objetivo es servir como referencia para desarrolladores, administradores del sistema, analistas de datos y otras partes interesadas que necesiten comprender la arquitectura, el funcionamiento interno, los componentes de IA del sistema, y los detalles operativos del modelo.

### 1.2. Visión General del Sistema Smart Academy
Smart Academy es una plataforma de gestión académica integral diseñada para optimizar la administración educativa y enriquecer la experiencia de aprendizaje. Su propósito es proporcionar a educadores, estudiantes y administradores las herramientas necesarias para un seguimiento detallado del progreso académico y para la toma de decisiones informadas. El sistema facilita la gestión de perfiles de usuario (con roles definidos como administrador, superusuario, profesor, estudiante y padre), la organización de cursos y asignaturas, y el registro de calificaciones y asistencia. Un componente central es su módulo de Inteligencia Artificial, que analiza datos históricos y actuales (incluyendo datos simulados con tendencias realistas generados por `app/scripts/populate_db.py` y descritos en `Dataset_utilizado.md`) para ofrecer predicciones sobre el desempeño estudiantil. Estas predicciones están diseñadas para permitir intervenciones tempranas y personalizadas, ayudando a identificar estudiantes que podrían necesitar apoyo adicional y a adaptar las estrategias pedagógicas.

## 2. Arquitectura del Sistema

### 2.1. Componentes Principales
El sistema Smart Academy se articula en torno a tres componentes fundamentales que interactúan para ofrecer una solución robusta y escalable:
-   **Backend (API):** Construido con FastAPI en Python, este componente es el cerebro del sistema. Expone un conjunto de APIs RESTful que gestionan toda la lógica de negocio, incluyendo la autenticación y autorización de usuarios basada en roles, la administración de entidades académicas (estudiantes, cursos, calificaciones, asistencia, participación), y la interacción con la base de datos. Crucialmente, el backend también orquesta las operaciones del modelo de IA, desde la recopilación y preprocesamiento de datos para inferencias hasta la entrega de predicciones a los sistemas cliente (como un frontend web o aplicaciones móviles).
-   **Base de Datos (PostgreSQL):** PostgreSQL sirve como el sistema de gestión de base de datos relacional, proporcionando almacenamiento persistente, seguro y eficiente para todos los datos de la aplicación. Esto incluye perfiles de usuario detallados, registros académicos históricos y actuales, y cualquier metadato o configuración del sistema. La integridad y disponibilidad de estos datos son vitales, ya que constituyen la materia prima tanto para las operaciones diarias del sistema como para el entrenamiento y la inferencia del modelo de IA.
-   **Modelo de IA (Servicio de ML):** Más que un simple componente, el modelo de IA (y su lógica circundante, encapsulada en `app/services/ml_service.py`) funciona como un servicio especializado dentro del ecosistema del backend. Es responsable de cargar modelos de predicción previamente entrenados, procesar los datos de entrada necesarios (extraídos de la base de datos a través del backend), realizar inferencias (predicciones) y devolver estos resultados. Su diseño permite que sea actualizado o reentrenado independientemente de la lógica de negocio principal, asegurando flexibilidad y mantenibilidad.

### 2.2. Tecnologías Utilizadas
La selección tecnológica busca un equilibrio entre rendimiento, robustez, y un ecosistema de desarrollo maduro, especialmente para las capacidades de IA:
-   **Lenguaje de Programación (Backend):** Python 3.x, elegido por su amplia adopción en el desarrollo web y científico, su sintaxis clara y la vasta cantidad de librerías disponibles, especialmente para Machine Learning.
-   **Framework Backend:** FastAPI, seleccionado por su alto rendimiento (comparable a NodeJS y Go), su moderna sintaxis basada en type hints de Python que facilita la validación automática de datos y la generación de documentación OpenAPI, y su facilidad para construir APIs robustas.
-   **Base de Datos:** PostgreSQL, un potente sistema de gestión de bases de datos relacionales de código abierto, conocido por su fiabilidad, robustez de características y extensibilidad.
-   **Autenticación:** Tokens JWT (JSON Web Tokens) para la gestión de sesiones seguras y stateless, complementado con un sistema de roles (administrador, superusuario, profesor, estudiante, padre) para un control de acceso granular a las funcionalidades y datos del sistema.
-   **Librerías de IA:** La elección específica dependerá de los algoritmos implementados, pero comúnmente incluirá Pandas para manipulación de datos, NumPy para operaciones numéricas, Scikit-learn para algoritmos de ML clásicos y métricas de evaluación. Para modelos más complejos como redes neuronales, se podrían utilizar TensorFlow o PyTorch. [Especificar librerías concretas una vez definidas].
-   **Servidor Web (para FastAPI):** Uvicorn como servidor ASGI de alto rendimiento, frecuentemente desplegado detrás de un servidor de procesos como Gunicorn en entornos de producción para gestionar workers y mejorar la concurrencia.

### 2.3. Flujo de Datos General
El flujo de datos en Smart Academy está diseñado para asegurar la coherencia y facilitar tanto las operaciones transaccionales como las analíticas del modelo de IA.

**Flujo Operacional y de Captura de Datos:**
1.  **Interacción del Usuario:** Los usuarios (estudiantes, profesores, administradores) interactúan con el sistema a través de una interfaz cliente (ej. una aplicación web o móvil).
2.  **Solicitud a la API:** Las acciones del usuario (ej. registrar una calificación, marcar asistencia, consultar información) se traducen en solicitudes HTTP a los endpoints correspondientes de la API FastAPI.
3.  **Procesamiento en el Backend:** El backend valida la solicitud (incluyendo autenticación y autorización), ejecuta la lógica de negocio pertinente y, si es necesario, interactúa con la base de datos PostgreSQL para crear, leer, actualizar o eliminar registros (operaciones CRUD).
4.  **Respuesta al Cliente:** El backend envía una respuesta HTTP al cliente, confirmando la operación o devolviendo los datos solicitados.

**Flujo de Datos para Predicciones del Modelo de IA:**
1.  **Solicitud de Predicción:** Un cliente (o un proceso interno programado) solicita una predicción a un endpoint específico de la API, por ejemplo, `/api/v1/students/{student_id}/predict_performance`.
2.  **Orquestación por el Backend:** La API FastAPI recibe la solicitud y la dirige al servicio de ML (`app/services/ml_service.py`).
3.  **Recopilación de Features:** El servicio de ML consulta la base de datos PostgreSQL para obtener los datos históricos y actuales necesarios del estudiante (y potencialmente de su contexto) que servirán como features para el modelo. Esto puede implicar la recuperación de calificaciones, asistencia, participación, etc.
4.  **Preprocesamiento de Datos:** Los datos recuperados se someten a las etapas de preprocesamiento definidas (limpieza, transformación, ingeniería de características) para adecuarlos al formato esperado por el modelo entrenado.
5.  **Inferencia del Modelo:** Las features preprocesadas se pasan al modelo de IA cargado en memoria.
6.  **Generación de Predicción:** El modelo procesa las features y genera una predicción (ej. una calificación esperada, una categoría de riesgo).
7.  **Respuesta de la API:** El servicio de ML devuelve la predicción al endpoint de la API, que la formatea (generalmente como JSON) y la envía como respuesta al cliente.

**Flujo de Datos para Entrenamiento/Reentrenamiento del Modelo de IA (Periódico/Bajo Demanda):**
1.  **Extracción de Datos:** Se extrae un conjunto de datos relevante de la base de datos PostgreSQL. Para el entrenamiento inicial o para aumentar el dataset, se pueden utilizar los datos generados por `app/scripts/populate_db.py`.
2.  **Preprocesamiento y Entrenamiento:** Este dataset se preprocesa y se utiliza para entrenar (o reentrenar) el modelo de IA utilizando las librerías y algoritmos seleccionados.
3.  **Evaluación y Versionado:** El modelo resultante se evalúa rigurosamente. Si cumple con los criterios de calidad, se versiona y se guarda como un artefacto (ej. un archivo `.pkl` o `.h5`).
4.  **Despliegue del Modelo:** El nuevo modelo entrenado se despliega, lo que puede implicar reemplazar el modelo anterior en el servicio de ML para que las futuras solicitudes de predicción utilicen la versión actualizada.

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
El modelo de IA se nutre fundamentalmente de los datos almacenados en la base de datos PostgreSQL del sistema. Para el desarrollo inicial, entrenamiento y pruebas exhaustivas, se utiliza un dataset simulado generado por el script `app/scripts/populate_db.py`, cuya estructura y características se detallan en `Dataset_utilizado.md`. Este script está diseñado para crear datos realistas que incluyen tendencias temporales y variaciones individuales, esenciales para entrenar un modelo predictivo robusto.

En un entorno de producción, el modelo se entrenaría y operaría principalmente con los datos operativos reales generados por la actividad diaria en la plataforma Smart Academy. El dataset simulado sigue siendo valioso para escenarios de prueba, benchmarking y para complementar datos reales si fuera necesario (con las debidas precauciones para evitar sesgos).

Las entidades principales que proporcionan datos para el modelo incluyen:
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