from setuptools import setup, find_packages

setup(
    name="backend_smart_academy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.37",
        "psycopg2-binary==2.9.9",
        "alembic==1.13.1",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "python-multipart==0.0.9",
        "python-dotenv==1.0.1",
        "pydantic==2.6.4",
        "pydantic-settings==2.2.1",
        "scikit-learn==1.4.1.post1",
        "pandas==2.2.1",
        "numpy==1.26.4"
    ],
)