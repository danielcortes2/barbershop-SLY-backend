# =====================================================
# CONFIGURACIÓN - FastAPI Application
# =====================================================

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""
    
    # Database
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    
    # Application
    app_env: str = "development"
    app_port: int = 3001
    app_host: str = "0.0.0.0"
    
    # Admin
    admin_password: str
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parsear CORS origins desde string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def database_url(self) -> str:
        """Construir URL de conexión a la base de datos"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
