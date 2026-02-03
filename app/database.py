# =====================================================
# BASE DE DATOS - SQLAlchemy Configuration
# =====================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.database_url,
    echo=settings.app_env == "development",
    pool_pre_ping=True,  # Verificar conexión antes de usarla
    pool_size=10,
    max_overflow=20
)

# Crear SessionLocal para transacciones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Dependencia para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar la base de datos (crear tablas si no existen)"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise
