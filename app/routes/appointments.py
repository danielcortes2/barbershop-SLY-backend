# =====================================================
# RUTAS - Endpoints para Citas
# =====================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Appointment, Barber, Service
from app.schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter()

# ==================== OBTENER TODAS LAS CITAS ====================
@router.get("/", response_model=List[AppointmentResponse])
async def get_all_appointments(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Obtener todas las citas con paginación y filtro opcional por estado"""
    query = db.query(Appointment)
    
    if status_filter:
        query = query.filter(Appointment.status == status_filter)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments

# ==================== OBTENER CITA POR ID ====================
@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Obtener una cita específica por ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cita con ID {appointment_id} no encontrada"
        )
    return appointment

# ==================== CREAR CITA ====================
@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita"""
    
    # Verificar que el barbero existe
    barber = db.query(Barber).filter(Barber.id == appointment.barber_id).first()
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barbero con ID {appointment.barber_id} no encontrado"
        )
    
    # Verificar que el servicio existe
    service = db.query(Service).filter(Service.id == appointment.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {appointment.service_id} no encontrado"
        )
    
    # Verificar que no existe otra cita en la misma fecha/hora para el mismo barbero
    existing_appointment = db.query(Appointment).filter(
        Appointment.barber_id == appointment.barber_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.status != "cancelled"
    ).first()
    
    if existing_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El barbero ya tiene una cita en esa fecha y hora"
        )
    
    new_appointment = Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

# ==================== ACTUALIZAR CITA ====================
@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una cita existente"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cita con ID {appointment_id} no encontrada"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = appointment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# ==================== ELIMINAR CITA ====================
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Eliminar una cita (soft delete mediante cancelación)"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cita con ID {appointment_id} no encontrada"
        )
    
    # En lugar de eliminar, marcamos como cancelada
    db_appointment.status = "cancelled"
    db.commit()
    return None

# ==================== OBTENER CITAS DE UN BARBERO ====================
@router.get("/barber/{barber_id}", response_model=List[AppointmentResponse])
async def get_barber_appointments(barber_id: int, db: Session = Depends(get_db)):
    """Obtener todas las citas de un barbero específico"""
    # Verificar que el barbero existe
    barber = db.query(Barber).filter(Barber.id == barber_id).first()
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barbero con ID {barber_id} no encontrado"
        )
    
    appointments = db.query(Appointment).filter(
        Appointment.barber_id == barber_id
    ).all()
    return appointments
