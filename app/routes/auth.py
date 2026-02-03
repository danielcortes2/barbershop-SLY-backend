# =====================================================
# RUTAS - Endpoints para Autenticación
# =====================================================

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.config import settings
from datetime import datetime, timedelta
import secrets

router = APIRouter()

# Almacenamiento simple de sesiones (en producción usar JWT o Redis)
active_sessions = {}

class LoginRequest(BaseModel):
    """Esquema para login"""
    password: str

class LoginResponse(BaseModel):
    """Esquema de respuesta de login"""
    token: str
    message: str

# Contraseña del admin desde variables de entorno
ADMIN_PASSWORD = settings.admin_password

# ==================== LOGIN ====================
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Autenticar como admin"""
    
    if request.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    # Generar token único
    token = secrets.token_urlsafe(32)
    
    # Guardar sesión con expiración de 8 horas
    active_sessions[token] = {
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(hours=8)
    }
    
    return {
        "token": token,
        "message": "Autenticación exitosa"
    }

# ==================== VERIFICAR SESIÓN ====================
@router.get("/verify")
async def verify_session(token: str):
    """Verificar si la sesión es válida"""
    
    if token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    session = active_sessions[token]
    
    if datetime.utcnow() > session["expires_at"]:
        del active_sessions[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    
    return {"valid": True, "message": "Token válido"}

# ==================== LOGOUT ====================
@router.post("/logout")
async def logout(token: str):
    """Cerrar sesión"""
    
    if token in active_sessions:
        del active_sessions[token]
    
    return {"message": "Sesión cerrada"}
