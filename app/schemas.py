# =====================================================
# SCHEMAS - Pydantic Models para Validación
# =====================================================

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ==================== BARBEROS ====================

class BarberCreate(BaseModel):
    """Esquema para crear un barbero"""
    name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)

class BarberUpdate(BaseModel):
    """Esquema para actualizar un barbero"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)

class BarberResponse(BaseModel):
    """Esquema de respuesta para un barbero"""
    id: int
    name: str
    phone: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== SERVICIOS ====================

class ServiceCreate(BaseModel):
    """Esquema para crear un servicio"""
    name: str = Field(..., min_length=1, max_length=255)
    duration: int = Field(..., gt=0)  # Duración en minutos
    price: float = Field(..., gt=0)

class ServiceUpdate(BaseModel):
    """Esquema para actualizar un servicio"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    duration: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)

class ServiceResponse(BaseModel):
    """Esquema de respuesta para un servicio"""
    id: int
    name: str
    duration: int
    price: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== CITAS ====================

class AppointmentStatus(str, Enum):
    """Estados de citas"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentCreate(BaseModel):
    """Esquema para crear una cita"""
    client_name: str = Field(..., min_length=1, max_length=255)
    client_phone: Optional[str] = Field(None, max_length=20)
    barber_id: int = Field(..., gt=0)
    service_id: int = Field(..., gt=0)
    appointment_date: datetime
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    """Esquema para actualizar una cita"""
    client_name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_phone: Optional[str] = Field(None, max_length=20)
    appointment_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    """Esquema de respuesta para una cita"""
    id: int
    client_name: str
    client_phone: Optional[str]
    barber_id: int
    service_id: int
    appointment_date: datetime
    status: AppointmentStatus
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Incluir relaciones
    barber: Optional[BarberResponse] = None
    service: Optional[ServiceResponse] = None
    
    class Config:
        from_attributes = True
