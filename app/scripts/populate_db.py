import logging
import random
from datetime import datetime, timedelta
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings # For DATABASE_URL
from sqlalchemy.orm import sessionmaker # For SessionLocal
from app.db.base import Base
from faker import Faker

# Configuración de la base de datos local para este script
DATABASE_URL = settings.get_database_url()
engine = create_engine(DATABASE_URL) # El engine que necesita Base.metadata
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # El SessionLocal que usa el script

# Configurar el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants for Data Generation ---
NUM_TEACHERS = 5
NUM_STUDENTS = 50
NUM_COURSES = 8
NUM_ACADEMIC_PERIODS = 4  # e.g., Semesters or Quarters
RECORDS_PER_PERIOD = 10   # e.g., weekly records for attendance/participation, or multiple grades
START_DATE = datetime(2023, 1, 15)

# Probabilities and ranges for generating realistic data
ATTENDANCE_BASE_PROBABILITY_RANGE = (0.75, 0.95) # Base likelihood of a student attending
PARTICIPATION_BASE_SCORE_RANGE = (5, 9) # Base participation score out of 10
GRADE_BASE_RANGE = (50, 90) # Base grade range out of 100
TREND_STRENGTH_RANGE = (-0.15, 0.15) # How strongly a trend affects values per period (e.g., -0.1 means 10% decline per period from base)
RANDOM_VARIATION_PERCENTAGE = 0.10 # +/- 10% random noise

# Importamos configuraciones y modelos
from app.core.config import settings
from app.models.user import User, RoleEnum, GenderEnum
from app.models.role import Role # Added Role model import
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.participation import Participation
from app.core.security import get_password_hash

# Conectar directamente a la base de datos usando la configuración del proyecto
SQLALCHEMY_DATABASE_URL = settings.get_database_url()

# SQLAlchemy expects postgresql:// but many providers use postgres://
if SQLALCHEMY_DATABASE_URL.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicializar Faker
fake = Faker()


def create_roles(db):
    """Crear roles básicos si no existen."""
    logger.info("Verificando/creando roles básicos...")
    required_roles = [
        (RoleEnum.STUDENT, "Acceso de estudiante"),
        (RoleEnum.TEACHER, "Acceso de profesor"),
        (RoleEnum.PARENT, "Acceso de padre/tutor"),
        (RoleEnum.ADMINISTRATOR, "Acceso de administrador del sistema")
    ]
    for role_enum, desc in required_roles:
        role_name = role_enum.value
        existing_role = db.query(Role).filter(Role.name == role_enum).first()
        if not existing_role:
            new_role = Role(name=role_enum, description=desc)
            db.add(new_role)
            logger.info(f"Rol '{role_name}' creado.")
        else:
            logger.info(f"Rol '{role_name}' ya existe.")
    db.commit()
    logger.info("Roles básicos verificados/creados.")

def create_teachers(db, num_teachers=5):
    """Crear profesores"""
    logger.info(f"Creando {num_teachers} profesores...")
    teachers = []
    
    for i in range(num_teachers):
        gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
        first_name = fake.first_name_male() if gender == GenderEnum.MALE else fake.first_name_female()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@smartacademy.com"
        
        teacher = User(
            email=email,
            hashed_password=get_password_hash("password123"),
            full_name=f"{first_name} {last_name}",
            phone=fake.phone_number(),
            direction=fake.address(),
            birth_date=fake.date_of_birth(minimum_age=25, maximum_age=65).strftime("%Y-%m-%d"),
            gender=gender,
            # role=RoleEnum.TEACHER, # Replaced by M2M relationship
            is_active=True,
            is_superuser=False
        )
        
        # Assign Role
        teacher_role = db.query(Role).filter(Role.name == RoleEnum.TEACHER).first()
        if teacher_role:
            teacher.roles.append(teacher_role)
        else:
            logger.error(f"Rol TEACHER no encontrado. Asegúrese de que create_roles se haya ejecutado.")
            # Considerar si se debe detener el script o manejar este error de otra forma

        db.add(teacher)
        teachers.append(teacher)
    
    db.commit()
    logger.info(f"Profesores creados exitosamente")
    return teachers

def create_courses(db, num_courses=8):
    """Crear cursos"""
    logger.info(f"Creando {num_courses} cursos...")
    courses = []
    
    course_names = [
        "Matemáticas", "Física", "Química", "Biología", 
        "Historia", "Literatura", "Programación", "Inglés",
        "Estadística", "Economía", "Arte", "Educación Física"
    ]
    
    for i in range(min(num_courses, len(course_names))):
        course = Course(
            name=course_names[i],
            description=fake.paragraph(),
            credits=random.choice([3, 4, 5])
        )
        
        db.add(course)
        courses.append(course)
    
    db.commit()
    logger.info(f"Cursos creados exitosamente")
    return courses

def create_students(db, num_students=20):
    """Crear estudiantes"""
    logger.info(f"Creando {num_students} estudiantes...")
    students = []
    
    # Primero creamos usuarios estudiantes
    for i in range(num_students):
        gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
        first_name = fake.first_name_male() if gender == GenderEnum.MALE else fake.first_name_female()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@student.smartacademy.com"
        
        user = User(
            email=email,
            hashed_password=get_password_hash("student123"),
            full_name=f"{first_name} {last_name}",
            phone=fake.phone_number(),
            direction=fake.address(),
            birth_date=fake.date_of_birth(minimum_age=14, maximum_age=20).strftime("%Y-%m-%d"),
            gender=gender,
            # role=RoleEnum.STUDENT, # Replaced by M2M relationship
            is_active=True,
            is_superuser=False
        )
        
        # Assign Role to User
        student_role = db.query(Role).filter(Role.name == RoleEnum.STUDENT).first()
        if student_role:
            user.roles.append(student_role)
        else:
            logger.error(f"Rol STUDENT no encontrado. Asegúrese de que create_roles se haya ejecutado.")

        db.add(user)
        
        # Ahora creamos el registro de estudiante
        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=datetime.strptime(user.birth_date, "%Y-%m-%d").date() if user.birth_date else fake.date_of_birth(minimum_age=14, maximum_age=20),
            address=user.direction or fake.address(),
            phone=user.phone or fake.phone_number()
        )
        
        db.add(student)
        students.append(student)
    
    db.commit()
    logger.info(f"Estudiantes creados exitosamente")
    return students

def create_grades(db, students, courses):
    """Crear calificaciones para simular historiales académicos con tendencias."""
    logger.info(f"Creando calificaciones para {len(students)} estudiantes en {len(courses)} cursos...")

    days_per_period = 90 # Aproximadamente 3 meses por periodo académico

    for student in students:
        student_base_performance = random.uniform(GRADE_BASE_RANGE[0], GRADE_BASE_RANGE[1])
        # Tendencia general del estudiante (puede ser diferente por curso si se desea más complejidad)
        student_overall_trend_strength = random.uniform(TREND_STRENGTH_RANGE[0], TREND_STRENGTH_RANGE[1])

        for course in courses:
            # No todos los estudiantes están en todos los cursos o tienen calificaciones
            if random.random() < 0.9:  # 90% de probabilidad de tener calificaciones en este curso
                
                current_date = START_DATE
                
                for period_idx in range(NUM_ACADEMIC_PERIODS):
                    period_name = f"Periodo-{period_idx + 1}-{START_DATE.year + (START_DATE.month + period_idx * (days_per_period // 30) -1) // 12 }"
                    
                    # Aplicar tendencia general del estudiante al rendimiento base para este periodo
                    # El efecto de la tendencia se acumula con cada periodo
                    period_base_grade = student_base_performance * (1 + student_overall_trend_strength * period_idx)
                    period_base_grade = max(0, min(100, period_base_grade)) # Asegurar que esté entre 0 y 100

                    for record_num in range(RECORDS_PER_PERIOD):
                        # Calcular la calificación para este registro específico
                        # Añadir variación aleatoria
                        variation = period_base_grade * RANDOM_VARIATION_PERCENTAGE * random.uniform(-1, 1)
                        current_grade_value = period_base_grade + variation
                        current_grade_value = round(max(0, min(100, current_grade_value)), 1)

                        # Distribuir las fechas de los registros dentro del periodo
                        record_date = current_date + timedelta(days=(record_num * (days_per_period // RECORDS_PER_PERIOD)))
                        # Añadir un pequeño jitter a la fecha para que no sean todas iguales si RECORDS_PER_PERIOD es alto
                        record_date += timedelta(days=random.randint(-2,2))
                        record_date = min(record_date, START_DATE + timedelta(days=(period_idx + 1) * days_per_period -1) ) # No exceder el fin del periodo

                        grade = Grade(
                            student_id=student.id,
                            course_id=course.id,
                            period=period_name,
                            value=current_grade_value,
                            date_recorded=record_date
                        )
                        db.add(grade)
                    
                    current_date += timedelta(days=days_per_period)
    
    db.commit()
    logger.info(f"Calificaciones creadas exitosamente")

def create_attendance(db, students, courses):
    """Crear registros de asistencia para simular historiales con tendencias."""
    logger.info(f"Creando registros de asistencia para {len(students)} estudiantes en {len(courses)} cursos...")

    days_per_period = 90 # Aproximadamente 3 meses por periodo académico
    # Asumimos que RECORDS_PER_PERIOD son los puntos de control de asistencia por periodo
    # Si queremos simular asistencia diaria, RECORDS_PER_PERIOD debería ser ~60 (días lectivos en 3 meses)
    # y la lógica de fechas necesitaría saltar fines de semana.
    # Por simplicidad, distribuiremos RECORDS_PER_PERIOD equitativamente.

    for student in students:
        student_base_attendance_prob = random.uniform(ATTENDANCE_BASE_PROBABILITY_RANGE[0],
                                                      ATTENDANCE_BASE_PROBABILITY_RANGE[1])
        student_attendance_trend = random.uniform(TREND_STRENGTH_RANGE[0], TREND_STRENGTH_RANGE[1])

        for course in courses:
            if random.random() < 0.9:  # 90% de probabilidad de tener registros de asistencia en este curso
                
                current_period_start_date = START_DATE
                
                for period_idx in range(NUM_ACADEMIC_PERIODS):
                    # Probabilidad de asistencia para este estudiante, en este curso, para este periodo
                    # La tendencia afecta la probabilidad base
                    current_period_attendance_prob = student_base_attendance_prob * (1 + student_attendance_trend * period_idx)
                    # Aplicar una pequeña variación aleatoria específica del curso/periodo si se desea
                    current_period_attendance_prob *= (1 + RANDOM_VARIATION_PERCENTAGE * random.uniform(-0.5, 0.5))
                    current_period_attendance_prob = max(0.1, min(1.0, current_period_attendance_prob)) # Asegurar entre 10% y 100%

                    for record_num in range(RECORDS_PER_PERIOD):
                        # Calcular la fecha para este registro de asistencia
                        # Distribuir las fechas de los registros dentro del periodo
                        days_into_period = record_num * (days_per_period // RECORDS_PER_PERIOD)
                        record_date = current_period_start_date + timedelta(days=days_into_period)
                        
                        # Asegurarse de que la fecha no exceda el fin del periodo actual
                        # y añadir un pequeño jitter para evitar superposiciones exactas si es necesario
                        record_date += timedelta(days=random.randint(-1,1))
                        max_date_for_record = current_period_start_date + timedelta(days=days_per_period - 1)
                        record_date = min(record_date, max_date_for_record)
                        record_date = max(record_date, current_period_start_date) # No antes del inicio del periodo
                        
                        # Saltar fines de semana si estamos modelando días lectivos específicos
                        # Para simplificar, no lo haremos aquí, asumiendo que RECORDS_PER_PERIOD
                        # ya considera solo "días de contacto" o "semanas".
                        # Si se quisiera modelar días exactos, se necesitaría un bucle que avance día a día
                        # y cuente solo días lectivos hasta RECORDS_PER_PERIOD.

                        present = random.random() < current_period_attendance_prob
                        
                        attendance = Attendance(
                            student_id=student.id,
                            date=record_date,
                            present=present,
                            course_id=course.id
                        )
                        db.add(attendance)
                    
                    current_period_start_date += timedelta(days=days_per_period)
    
    db.commit()
    logger.info(f"Registros de asistencia creados exitosamente")

def create_participation(db, students, courses):
    """Crear registros de participación para simular historiales con tendencias."""
    logger.info(f"Creando registros de participación para {len(students)} estudiantes en {len(courses)} cursos...")

    days_per_period = 90 # Aproximadamente 3 meses por periodo académico

    for student in students:
        student_base_participation_score = random.uniform(PARTICIPATION_BASE_SCORE_RANGE[0],
                                                          PARTICIPATION_BASE_SCORE_RANGE[1])
        student_participation_trend = random.uniform(TREND_STRENGTH_RANGE[0], TREND_STRENGTH_RANGE[1])

        for course in courses:
            if random.random() < 0.9:  # 90% de probabilidad de tener registros de participación en este curso
                
                current_period_start_date = START_DATE
                
                for period_idx in range(NUM_ACADEMIC_PERIODS):
                    period_name = f"Periodo-{period_idx + 1}-{START_DATE.year + (START_DATE.month + period_idx * (days_per_period // 30) -1) // 12 }"
                    
                    # Puntuación de participación base para este estudiante, en este curso, para este periodo
                    current_period_base_score = student_base_participation_score * (1 + student_participation_trend * period_idx)
                    # Aplicar una pequeña variación aleatoria específica del curso/periodo
                    current_period_base_score *= (1 + RANDOM_VARIATION_PERCENTAGE * random.uniform(-0.5, 0.5))
                    current_period_base_score = max(0, min(10, current_period_base_score)) # Asegurar entre 0 y 10

                    for record_num in range(RECORDS_PER_PERIOD):
                        # Calcular la puntuación para este registro específico
                        variation = current_period_base_score * RANDOM_VARIATION_PERCENTAGE * random.uniform(-1, 1) # Variación sobre la base del periodo
                        current_score_value = current_period_base_score + variation
                        current_score_value = round(max(0, min(10, current_score_value)), 1)

                        # Distribuir las fechas de los registros dentro del periodo
                        days_into_period = record_num * (days_per_period // RECORDS_PER_PERIOD)
                        record_date = current_period_start_date + timedelta(days=days_into_period)
                        record_date += timedelta(days=random.randint(-2,2)) # Jitter
                        max_date_for_record = current_period_start_date + timedelta(days=days_per_period - 1)
                        record_date = min(record_date, max_date_for_record)
                        record_date = max(record_date, current_period_start_date)

                        participation = Participation(
                            student_id=student.id,
                            course_id=course.id,
                            date=record_date,
                            score=current_score_value,
                            period=period_name # Añadimos el periodo para consistencia si es necesario
                        )
                        db.add(participation)
                    
                    current_period_start_date += timedelta(days=days_per_period)
    
    db.commit()
    logger.info(f"Registros de participación creados exitosamente")

def populate_db():
    """Poblar la base de datos con datos de ejemplo"""
    logger.info("Iniciando población de la base de datos...")
    # Asegurar que todas las tablas estén creadas/actualizadas según los modelos
    try:
        logger.info("Verificando/Creando estructura de tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Estructura de tablas verificada/creada.")
    except Exception as e_create_tables:
        logger.error(f"Error crítico al intentar crear/verificar tablas: {e_create_tables}")
        logger.error("Por favor, asegúrese de que la conexión a la base de datos sea correcta y los modelos sean válidos.")
        return # No continuar si las tablas no se pueden preparar
    
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos y consultar al usuario
        student_count = db.query(Student).count()
        course_count = db.query(Course).count()
        
        if student_count > 0 or course_count > 0:
            logger.warning(f"La base de datos ya contiene datos: {student_count} estudiantes, {course_count} cursos.")
            while True:
                choice = input("Opciones: (a)gregar más datos, (l)impiar y repoblar todo, (c)ancelar: ").lower()
                if choice == 'a':
                    logger.info("Se agregarán más datos a los existentes.")
                    break
                elif choice == 'l':
                    logger.info("Limpiando la base de datos (eliminando todas las tablas)...")
                    # Cerrar la sesión actual antes de drop_all para liberar conexiones
                    db.close()
                    try:
                        Base.metadata.drop_all(bind=engine)
                        logger.info("Tablas eliminadas.")
                        logger.info("Creando todas las tablas nuevamente...")
                        Base.metadata.create_all(bind=engine)
                        logger.info("Tablas creadas nuevamente.")
                    except Exception as e_drop_create:
                        logger.error(f"Error durante la limpieza y recreación de tablas: {e_drop_create}")
                        return # No se puede continuar si la limpieza/recreación falla
                    # Reabrir sesión para la población, ya que la anterior se cerró
                    db = SessionLocal()
                    # Reset counts as we are starting fresh for the subsequent logic
                    student_count = 0 
                    course_count = 0
                    logger.info("Base de datos limpiada y lista para repoblar.")
                    break
                elif choice == 'c':
                    logger.info("Operación cancelada por el usuario.")
                    db.close() # Asegurarse de cerrar la sesión si se cancela aquí
                    return
                else:
                    logger.warning("Opción no válida. Por favor, elija 'a', 'l', o 'c'.")
        else: # No data found, proceed to populate
            logger.info("La base de datos parece estar vacía o no contiene estudiantes/cursos. Se procederá a poblar.")
        
        # Crear roles básicos primero
        create_roles(db)

        # Crear datos básicos
        teachers = create_teachers(db, num_teachers=NUM_TEACHERS)
        courses = create_courses(db, num_courses=NUM_COURSES)
        students = create_students(db, num_students=NUM_STUDENTS)
        
        # Crear datos para análisis y predicción
        create_grades(db, students, courses)
        create_attendance(db, students, courses)
        create_participation(db, students, courses)
        
        logger.info("Base de datos poblada exitosamente con datos de ejemplo")
    except Exception as e:
        db.rollback()
        logger.error(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Iniciando script de población de datos")
    populate_db()
    logger.info("Proceso completado")
