"""
Schemas Pydantic para validación de datos
Define la estructura de requests y responses de la API
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date
from typing import Optional
import re


class ReservaBase(BaseModel):
    """
    Schema base con campos comunes de Reserva
    """
    nombre_cliente: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del cliente",
        examples=["Juan Pérez"]
    )
    email: EmailStr = Field(
        ...,
        description="Email del cliente",
        examples=["juan.perez@email.com"]
    )
    fecha: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Fecha de la reserva en formato YYYY-MM-DD",
        examples=["2026-02-15"]
    )
    hora: str = Field(
        ...,
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        description="Hora de la reserva en formato HH:MM (24h)",
        examples=["14:30"]
    )
    servicio: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Tipo de servicio solicitado",
        examples=["Corte de pelo", "Corte + Barba", "Afeitado"]
    )
    
    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        """
        Valida que la fecha sea válida y no esté en el pasado
        """
        try:
            fecha_obj = datetime.strptime(v, "%Y-%m-%d").date()
            if fecha_obj < date.today():
                raise ValueError("La fecha no puede ser anterior a hoy")
            return v
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            raise e
    
    @field_validator('hora')
    @classmethod
    def validar_hora(cls, v: str) -> str:
        """
        Valida que la hora esté en horario laboral (9:00 - 20:00)
        """
        hora_int = int(v.split(':')[0])
        if hora_int < 9 or hora_int >= 20:
            raise ValueError("Horario de atención: 09:00 - 20:00")
        return v


class ReservaCreate(ReservaBase):
    """
    Schema para crear una nueva reserva
    """
    pass


class ReservaUpdate(BaseModel):
    """
    Schema para actualizar una reserva
    Todos los campos son opcionales
    """
    nombre_cliente: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        examples=["Juan Pérez"]
    )
    email: Optional[EmailStr] = Field(
        None,
        examples=["juan.perez@email.com"]
    )
    fecha: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2026-02-15"]
    )
    hora: Optional[str] = Field(
        None,
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["14:30"]
    )
    servicio: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        examples=["Corte de pelo"]
    )
    estado: Optional[str] = Field(
        None,
        pattern=r"^(confirmada|cancelada)$",
        examples=["confirmada"]
    )
    
    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v: Optional[str]) -> Optional[str]:
        """
        Valida que la fecha sea válida y no esté en el pasado
        """
        if v is None:
            return v
        try:
            fecha_obj = datetime.strptime(v, "%Y-%m-%d").date()
            if fecha_obj < date.today():
                raise ValueError("La fecha no puede ser anterior a hoy")
            return v
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            raise e
    
    @field_validator('hora')
    @classmethod
    def validar_hora(cls, v: Optional[str]) -> Optional[str]:
        """
        Valida que la hora esté en horario laboral
        """
        if v is None:
            return v
        hora_int = int(v.split(':')[0])
        if hora_int < 9 or hora_int >= 20:
            raise ValueError("Horario de atención: 09:00 - 20:00")
        return v


class ReservaResponse(ReservaBase):
    """
    Schema de respuesta para una reserva
    Incluye campos generados por el sistema
    """
    id: int = Field(..., description="ID único de la reserva")
    estado: str = Field(..., description="Estado de la reserva")
    created_at: datetime = Field(..., description="Fecha y hora de creación")
    
    class Config:
        from_attributes = True  # Permite crear desde modelos ORM


class ReservaListResponse(BaseModel):
    """
    Schema de respuesta para listado de reservas
    """
    total: int = Field(..., description="Total de reservas")
    reservas: list[ReservaResponse] = Field(..., description="Lista de reservas")


class MessageResponse(BaseModel):
    """
    Schema para mensajes de respuesta simples
    """
    message: str = Field(..., description="Mensaje de respuesta")
    detail: Optional[str] = Field(None, description="Detalles adicionales")


class ErrorResponse(BaseModel):
    """
    Schema para respuestas de error
    """
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
