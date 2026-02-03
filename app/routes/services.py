# =====================================================
# RUTAS - Endpoints para Servicios
# =====================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Service
from app.schemas import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter()

# ==================== OBTENER TODOS LOS SERVICIOS ====================
@router.get("/", response_model=List[ServiceResponse])
async def get_all_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los servicios con paginación"""
    services = db.query(Service).offset(skip).limit(limit).all()
    return services

# ==================== OBTENER SERVICIO POR ID ====================
@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Obtener un servicio específico por ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {service_id} no encontrado"
        )
    return service

# ==================== CREAR SERVICIO ====================
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Crear un nuevo servicio"""
    # Verificar si el servicio ya existe
    existing_service = db.query(Service).filter(Service.name == service.name).first()
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un servicio con el nombre '{service.name}'"
        )
    
    new_service = Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# ==================== ACTUALIZAR SERVICIO ====================
@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)):
    """Actualizar un servicio existente"""
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {service_id} no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = service.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_service, field, value)
    
    db.commit()
    db.refresh(db_service)
    return db_service

# ==================== ELIMINAR SERVICIO ====================
@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Eliminar un servicio"""
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {service_id} no encontrado"
        )
    
    db.delete(db_service)
    db.commit()
    return None
