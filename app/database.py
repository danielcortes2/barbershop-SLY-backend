"""
Configuración de la base de datos SQLAlchemy
Gestiona la conexión y sesiones de base de datos
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# Crear motor de base de datos
# Para SQLite: añadir check_same_thread=False permite uso en múltiples threads
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de dependencia para obtener sesiones de base de datos
    Garantiza que la sesión se cierre después de cada request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
