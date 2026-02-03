# =====================================================
# MODELOS - SQLAlchemy Models
# =====================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class Barber(Base):
    """Modelo para los barberos"""
    __tablename__ = "barbers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    appointments = relationship("Appointment", back_populates="barber", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Barber(id={self.id}, name={self.name})>"

class Service(Base):
    """Modelo para los servicios"""
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    duration = Column(Integer, nullable=False)  # Duración en minutos
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    appointments = relationship("Appointment", back_populates="service", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name}, duration={self.duration}min, price=${self.price})>"

class AppointmentStatus(str, enum.Enum):
    """Estados posibles de una cita"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Appointment(Base):
    """Modelo para las citas"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False, index=True)
    client_phone = Column(String(20))
    barber_id = Column(Integer, ForeignKey("barbers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    barber = relationship("Barber", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    
    # Restricción de unicidad: un barbero no puede tener dos citas a la misma hora
    __table_args__ = (
        UniqueConstraint('barber_id', 'appointment_date', name='unique_barber_appointment_date'),
    )
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, client={self.client_name}, date={self.appointment_date}, status={self.status})>"
