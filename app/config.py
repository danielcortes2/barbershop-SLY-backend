# =====================================================
# CONFIGURACION - FastAPI Application
# =====================================================

from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus
import os

class Settings(BaseSettings):
    """Configuracion de la aplicacion desde variables de entorno"""
    
    # Database
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    database_engine: str = "mysql"  # "mysql" o "postgresql"
    
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
        """Construir URL de conexion a la base de datos"""
        password = quote_plus(self.db_password)
        if self.database_engine == "postgresql":
            return f"postgresql+psycopg2://{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return f"mysql+pymysql://{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"

settings = Settings()
