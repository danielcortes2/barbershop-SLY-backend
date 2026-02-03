# =====================================================
# APLICACIÓN PRINCIPAL - FastAPI App
# =====================================================

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import barbers, services, appointments, auth

# Configurar logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
docs_url = "/docs" if settings.app_env == "development" else None
redoc_url = "/redoc" if settings.app_env == "development" else None

app = FastAPI(
    title="Barbershop API",
    description="API para sistema de reservas de barbería",
    version="1.0.0",
    docs_url=docs_url,
    redoc_url=redoc_url
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de startup
@app.on_event("startup")
async def startup_event():
    """Inicializar la base de datos al iniciar la aplicación"""
    logger.info("🚀 Iniciando aplicación...")
    try:
        init_db()
        logger.info("✓ Aplicación iniciada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al iniciar la aplicación: {e}")
        raise

# Eventos de shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al apagar la aplicación"""
    logger.info("🛑 Apagando aplicación...")

# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar estado de la aplicación"""
    return {"status": "ok", "message": "Barbershop API is running"}

# Incluir rutas
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(barbers.router, prefix="/api/v1/barbers", tags=["Barbers"])
app.include_router(services.router, prefix="/api/v1/services", tags=["Services"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])

# Raíz
@app.get("/", tags=["Info"])
async def root():
    """Información de la API"""
    return {
        "name": "Barbershop API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development"
    )
