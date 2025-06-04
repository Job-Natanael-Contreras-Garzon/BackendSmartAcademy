# Documentación del Dataset Simulado para Smart Academy

## 1. Introducción

El sistema Smart Academy utiliza un dataset **simulado** para el entrenamiento de sus modelos de predicción de rendimiento académico y para poblar la base de datos con datos de prueba realistas. Este dataset es generado mediante el script `app/scripts/populate_db.py`.

El objetivo de la simulación es crear un conjunto de datos que refleje patrones y tendencias que podrían encontrarse en un entorno académico real, permitiendo así un entrenamiento y evaluación más robustos de los modelos de Machine Learning.

## 2. Entidades y Atributos Principales Generados

El script `populate_db.py` genera las siguientes entidades principales con sus respectivos atributos:

### 2.1. Usuarios (`User`)
- **Tipos**: Estudiantes, Profesores, Administradores, Padres.
- **Atributos Comunes**:
    - `id`: Identificador único.
    - `email`: Correo electrónico (único).
    - `full_name`: Nombre completo.
    - `phone`: Número de teléfono.
    - `direction`: Dirección.
    - `birth_date`: Fecha de nacimiento.
    - `gender`: Género ("male", "female", "other").
    - `role`: Rol del usuario ("student", "teacher", "administrator", "parent").
    - `is_active`: Booleano, indica si el usuario está activo.
    - `is_superuser`: Booleano, indica si es superusuario.
- **Notas**: Se generan múltiples usuarios para cada rol, con datos ficticios pero coherentes.

### 2.2. Cursos (`Course`)
- **Atributos**:
    - `id`: Identificador único.
    - `name`: Nombre del curso (ej. "Matemáticas Avanzadas").
    - `description`: Descripción del curso.
    - `teacher_id`: ID del profesor asignado.
    - `period_id`: ID del periodo académico al que pertenece.
    - `grade`: Grado al que pertenece el curso (ej. "5to").
    - `level`: Nivel educativo (ej. "secondary").
- **Notas**: Se crean diversos cursos asignados a diferentes profesores y periodos.

### 2.3. Periodos Académicos (`AcademicPeriod`)
- **Atributos**:
    - `id`: Identificador único.
    - `name`: Nombre del periodo (ej. "2024-Trimestre 1", "2024-2025").
    - `start_date`: Fecha de inicio del periodo.
    - `end_date`: Fecha de fin del periodo.
    - `status`: Estado del periodo (ej. "activo", "finalizado", "planificado").
- **Notas**: Se generan múltiples periodos académicos para simular la progresión temporal.

### 2.4. Asignaturas (`Subject`)
- **Atributos**:
    - `id`: Identificador único.
    - `name`: Nombre de la asignatura (ej. "Álgebra Lineal").
    - `description`: Descripción.
    - `course_id`: ID del curso al que pertenece la asignatura.
- **Notas**: Cada curso puede tener varias asignaturas.

### 2.5. Calificaciones (`Grade`)
- **Atributos**:
    - `id`: Identificador único.
    - `student_id`: ID del estudiante.
    - `subject_id`: ID de la asignatura (o `course_id` dependiendo de la granularidad).
    - `period`: Nombre o ID del periodo académico.
    - `value`: Valor numérico de la calificación.
    - `date_recorded`: Fecha en que se registró la calificación.
    - `subcriteria_scores` (opcional): Calificaciones detalladas por subcriterios si aplica.
- **Lógica de Simulación**:
    - Se asigna una **calificación base** a cada estudiante para cada asignatura/curso.
    - Se introducen **tendencias temporales** (positivas o negativas) en las calificaciones a lo largo de los diferentes periodos académicos para simular la mejora o el declive del rendimiento.
    - Se añade **variación aleatoria** a cada calificación para hacerla más realista.
    - Las fechas se generan cronológicamente dentro de cada periodo.

### 2.6. Asistencia (`Attendance`)
- **Atributos**:
    - `id`: Identificador único.
    - `student_id`: ID del estudiante.
    - `course_id`: ID del curso.
    - `date`: Fecha del registro de asistencia.
    - `status`: Estado de la asistencia ("presente", "ausente", "tarde", "justificado").
    - `notes`: Notas adicionales.
- **Lógica de Simulación**:
    - Se asigna una **probabilidad base de asistencia** a cada estudiante.
    - Se pueden simular **tendencias** en la asistencia a lo largo del tiempo.
    - Se añade **variación aleatoria** a los registros diarios.

### 2.7. Participación (`Participation`)
- **Atributos**:
    - `id`: Identificador único.
    - `student_id`: ID del estudiante.
    - `course_id`: ID del curso.
    - `date`: Fecha del registro de participación.
    - `score`: Puntuación de la participación (ej. de 1 a 5).
    - `description`: Descripción de la participación.
    - `period`: Nombre o ID del periodo académico en que ocurrió la participación.
- **Lógica de Simulación**:
    - Se asigna un **nivel base de participación** a cada estudiante.
    - Se pueden simular **tendencias** en la participación.
    - Se añade **variación aleatoria**.

## 3. Lógica de Generación de Datos y Realismo

El script `populate_db.py` fue mejorado para generar datos más realistas mediante:

- **Constantes Configurables**: El script utiliza constantes para controlar:
    - `NUM_STUDENTS`, `NUM_TEACHERS`, `NUM_COURSES`, etc.
    - `NUM_ACADEMIC_PERIODS`: Número de periodos a simular.
    - `RECORDS_PER_PERIOD`: Cantidad de registros (calificaciones, asistencias) por estudiante por periodo.
    - `START_DATE`: Fecha de inicio para la generación de datos cronológicos.
    - `GRADE_BASE_MIN/MAX`, `ATTENDANCE_PROB_BASE_MIN/MAX`: Rangos para los valores base.
    - `TREND_STRENGTH_MIN/MAX`: Magnitud de las tendencias simuladas.
    - `RANDOM_VARIATION_FACTOR`: Nivel de aleatoriedad añadido.

- **Simulación de Rendimiento Individual y Tendencias**:
    - A cada estudiante se le asigna un **perfil de rendimiento base** (ej. estudiante de alto, medio o bajo rendimiento inicial).
    - Este perfil base influye en sus calificaciones, asistencia y participación iniciales.
    - Se aplican **tendencias** a estos indicadores a lo largo de los `NUM_ACADEMIC_PERIODS`. Un estudiante puede mejorar, empeorar o mantener su rendimiento.
    - Las fechas de los registros son **cronológicas** y se distribuyen dentro de los periodos académicos definidos.

- **Relaciones entre Entidades**:
    - Los estudiantes se inscriben en cursos.
    - Los profesores se asignan a cursos.
    - Las calificaciones, asistencias y participaciones se vinculan a estudiantes, cursos/asignaturas y periodos.

## 4. Uso del Dataset

Este dataset simulado se utiliza para:
- **Poblar la base de datos** para pruebas funcionales de la aplicación Smart Academy.
- **Entrenar los modelos de Machine Learning** para la predicción del rendimiento académico. Las tendencias y variaciones introducidas permiten que los modelos aprendan patrones más complejos.
- **Evaluar la efectividad de los modelos** en un entorno controlado antes de su despliegue con datos reales.

## 5. Limitaciones

Si bien se busca el realismo, es importante recordar que es un dataset **simulado**. No captura todas las complejidades y matices de los datos académicos reales. Sin embargo, proporciona una base sólida para el desarrollo y la prueba del sistema Smart Academy y sus componentes de ML.