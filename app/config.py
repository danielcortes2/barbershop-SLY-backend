"""
Configuración de la aplicación
Gestiona variables de entorno y configuraciones centralizadas
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando variables de entorno
    """
    # Nombre de la aplicación
    app_name: str = "SLY Barbershop API"
    app_version: str = "1.0.0"
    
    # Base de datos
    database_url: str = "sqlite:///./barbershop.db"
    
    # CORS - Orígenes permitidos (separados por comas)
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500"
    
    # Configuración general
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración de la aplicación (cacheada)
    """
    return Settings()
