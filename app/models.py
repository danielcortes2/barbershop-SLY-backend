"""
Modelos SQLAlchemy para la base de datos
Define la estructura de las tablas
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class EstadoReserva(str, enum.Enum):
    """
    Estados posibles de una reserva
    """
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"


class Reserva(Base):
    """
    Modelo de reserva de barbería
    Representa una cita/reserva en el sistema
    """
    __tablename__ = "reservas"
    
    # ID único autoincrementable
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del cliente
    nombre_cliente = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, index=True)
    
    # Datos de la reserva
    fecha = Column(String(10), nullable=False, index=True)  # Formato: YYYY-MM-DD
    hora = Column(String(5), nullable=False, index=True)    # Formato: HH:MM
    servicio = Column(String(100), nullable=False)
    
    # Estado de la reserva
    estado = Column(
        Enum(EstadoReserva),
        nullable=False,
        default=EstadoReserva.CONFIRMADA,
        index=True
    )
    
    # Timestamp de creación
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self):
        return f"<Reserva {self.id}: {self.nombre_cliente} - {self.fecha} {self.hora}>"
