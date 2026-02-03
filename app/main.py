"""
Aplicación principal FastAPI
Configura la aplicación, middlewares, CORS y manejo de errores
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from .config import get_settings
from .database import engine, Base
from .routers import reservas

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener configuración
settings = get_settings()

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API REST para gestión de reservas de barbería SLY.
    
    ## Funcionalidades
    
    * **Crear reservas** - Agenda una nueva cita
    * **Consultar reservas** - Lista todas las reservas o busca por ID
    * **Actualizar reservas** - Modifica datos de una reserva existente
    * **Cancelar reservas** - Cambia el estado a cancelada
    * **Eliminar reservas** - Elimina permanentemente una reserva
    * **Consultar disponibilidad** - Verifica horarios disponibles
    
    ## Validaciones
    
    * No permite reservas duplicadas en la misma fecha y hora
    * Valida formatos de fecha y email
    * Restringe horario de atención (09:00 - 20:00)
    * Previene reservas en fechas pasadas
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejadores de errores globales
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de Pydantic
    Retorna respuesta JSON clara con detalles del error
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    logger.warning(f"Error de validación: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Los datos proporcionados no son válidos",
            "detail": errors
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Maneja errores de base de datos
    """
    logger.error(f"Error de base de datos: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "Error al procesar la operación en la base de datos",
            "detail": "Por favor intente nuevamente. Si el problema persiste, contacte al administrador."
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Maneja errores generales no capturados
    """
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Ha ocurrido un error inesperado",
            "detail": str(exc) if settings.debug else "Por favor contacte al administrador."
        }
    )


# Incluir routers
app.include_router(reservas.router, prefix="/api")


# Endpoints de estado
@app.get("/", tags=["Status"])
async def root():
    """
    Endpoint raíz - Verifica que la API esté funcionando
    """
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health", tags=["Status"])
async def health_check():
    """
    Health check endpoint - Para monitoreo
    """
    return {
        "status": "healthy",
        "version": settings.app_version
    }


# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para loguear todas las requests
    """
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response


# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """
    Acciones al iniciar la aplicación
    """
    logger.info(f"Iniciando {settings.app_name} v{settings.app_version}")
    logger.info(f"Documentación disponible en: /docs")
    logger.info(f"CORS habilitado para: {origins}")


# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """
    Acciones al cerrar la aplicación
    """
    logger.info(f"Cerrando {settings.app_name}")
