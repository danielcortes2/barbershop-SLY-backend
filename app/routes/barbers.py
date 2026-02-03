# =====================================================
# RUTAS - Endpoints para Barberos
# =====================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Barber
from app.schemas import BarberCreate, BarberUpdate, BarberResponse

router = APIRouter()

# ==================== OBTENER TODOS LOS BARBEROS ====================
@router.get("/", response_model=List[BarberResponse])
async def get_all_barbers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los barberos con paginación"""
    barbers = db.query(Barber).offset(skip).limit(limit).all()
    return barbers

# ==================== OBTENER BARBERO POR ID ====================
@router.get("/{barber_id}", response_model=BarberResponse)
async def get_barber(barber_id: int, db: Session = Depends(get_db)):
    """Obtener un barbero específico por ID"""
    barber = db.query(Barber).filter(Barber.id == barber_id).first()
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barbero con ID {barber_id} no encontrado"
        )
    return barber

# ==================== CREAR BARBERO ====================
@router.post("/", response_model=BarberResponse, status_code=status.HTTP_201_CREATED)
async def create_barber(barber: BarberCreate, db: Session = Depends(get_db)):
    """Crear un nuevo barbero"""
    # Verificar si el barbero ya existe
    existing_barber = db.query(Barber).filter(Barber.name == barber.name).first()
    if existing_barber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un barbero con el nombre '{barber.name}'"
        )
    
    new_barber = Barber(**barber.dict())
    db.add(new_barber)
    db.commit()
    db.refresh(new_barber)
    return new_barber

# ==================== ACTUALIZAR BARBERO ====================
@router.put("/{barber_id}", response_model=BarberResponse)
async def update_barber(barber_id: int, barber: BarberUpdate, db: Session = Depends(get_db)):
    """Actualizar un barbero existente"""
    db_barber = db.query(Barber).filter(Barber.id == barber_id).first()
    if not db_barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barbero con ID {barber_id} no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = barber.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_barber, field, value)
    
    db.commit()
    db.refresh(db_barber)
    return db_barber

# ==================== ELIMINAR BARBERO ====================
@router.delete("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barber(barber_id: int, db: Session = Depends(get_db)):
    """Eliminar un barbero"""
    db_barber = db.query(Barber).filter(Barber.id == barber_id).first()
    if not db_barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barbero con ID {barber_id} no encontrado"
        )
    
    db.delete(db_barber)
    db.commit()
    return None
