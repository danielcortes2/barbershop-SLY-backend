"""
Router de Reservas
Define todos los endpoints de la API para gestionar reservas
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, models
from ..database import get_db

# Crear router con prefijo y tags para documentación
router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"],
    responses={
        404: {"description": "Reserva no encontrada"},
        400: {"description": "Datos inválidos"},
    }
)


@router.post(
    "/",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva reserva",
    description="Crea una nueva reserva en el sistema. Valida que no exista otra reserva confirmada en la misma fecha y hora."
)
async def crear_reserva(
    reserva: schemas.ReservaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva reserva con los siguientes datos:
    
    - **nombre_cliente**: Nombre completo del cliente (mínimo 2 caracteres)
    - **email**: Email válido del cliente
    - **fecha**: Fecha en formato YYYY-MM-DD (no puede ser pasada)
    - **hora**: Hora en formato HH:MM (horario 09:00 - 20:00)
    - **servicio**: Tipo de servicio solicitado
    
    Retorna la reserva creada con ID generado y estado "confirmada"
    """
    try:
        db_reserva = crud.create_reserva(db=db, reserva=reserva)
        return db_reserva
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=schemas.ReservaListResponse,
    summary="Listar reservas",
    description="Obtiene lista de todas las reservas con opciones de filtrado y paginación"
)
async def listar_reservas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    fecha: Optional[str] = Query(None, description="Filtrar por fecha (YYYY-MM-DD)"),
    estado: Optional[str] = Query(None, description="Filtrar por estado (confirmada/cancelada)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de reservas con:
    
    - **skip**: Registros a saltar para paginación (default: 0)
    - **limit**: Máximo de registros a devolver (default: 100, max: 500)
    - **fecha**: Filtro opcional por fecha específica
    - **estado**: Filtro opcional por estado (confirmada/cancelada)
    
    Retorna total de registros y lista de reservas ordenadas por fecha descendente
    """
    reservas = crud.get_reservas(
        db=db,
        skip=skip,
        limit=limit,
        fecha=fecha,
        estado=estado
    )
    
    total = crud.get_reservas_count(
        db=db,
        fecha=fecha,
        estado=estado
    )
    
    return {
        "total": total,
        "reservas": reservas
    }


@router.get(
    "/{reserva_id}",
    response_model=schemas.ReservaResponse,
    summary="Obtener reserva por ID",
    description="Obtiene los detalles de una reserva específica por su ID"
)
async def obtener_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una reserva específica por ID
    
    - **reserva_id**: ID único de la reserva
    
    Retorna todos los detalles de la reserva o error 404 si no existe
    """
    db_reserva = crud.get_reserva(db=db, reserva_id=reserva_id)
    
    if db_reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    return db_reserva


@router.put(
    "/{reserva_id}",
    response_model=schemas.ReservaResponse,
    summary="Actualizar reserva",
    description="Actualiza los datos de una reserva existente. Solo se actualizan los campos proporcionados."
)
async def actualizar_reserva(
    reserva_id: int,
    reserva_update: schemas.ReservaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una reserva existente
    
    - **reserva_id**: ID de la reserva a actualizar
    - Campos opcionales: nombre_cliente, email, fecha, hora, servicio, estado
    
    Solo se actualizan los campos proporcionados en el request.
    Valida que no se generen conflictos de horario al actualizar fecha/hora.
    
    Retorna la reserva actualizada o error 404 si no existe
    """
    try:
        db_reserva = crud.update_reserva(
            db=db,
            reserva_id=reserva_id,
            reserva_update=reserva_update
        )
        
        if db_reserva is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reserva con ID {reserva_id} no encontrada"
            )
        
        return db_reserva
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{reserva_id}",
    response_model=schemas.MessageResponse,
    summary="Eliminar reserva",
    description="Elimina permanentemente una reserva del sistema"
)
async def eliminar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una reserva del sistema permanentemente
    
    - **reserva_id**: ID de la reserva a eliminar
    
    Esta operación es irreversible. Para mantener historial, considere usar
    el endpoint de cancelación en su lugar.
    
    Retorna mensaje de confirmación o error 404 si no existe
    """
    deleted = crud.delete_reserva(db=db, reserva_id=reserva_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    return {
        "message": "Reserva eliminada exitosamente",
        "detail": f"La reserva con ID {reserva_id} ha sido eliminada permanentemente"
    }


@router.patch(
    "/{reserva_id}/cancelar",
    response_model=schemas.ReservaResponse,
    summary="Cancelar reserva",
    description="Cancela una reserva cambiando su estado a 'cancelada' sin eliminarla del sistema"
)
async def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancela una reserva sin eliminarla
    
    - **reserva_id**: ID de la reserva a cancelar
    
    Cambia el estado de la reserva a "cancelada" manteniendo el registro
    en el sistema para historial y estadísticas.
    
    Retorna la reserva con estado actualizado o error 404 si no existe
    """
    db_reserva = crud.cancel_reserva(db=db, reserva_id=reserva_id)
    
    if db_reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reserva_id} no encontrada"
        )
    
    return db_reserva


@router.get(
    "/disponibilidad/{fecha}",
    response_model=List[str],
    summary="Consultar disponibilidad",
    description="Obtiene las horas disponibles para una fecha específica"
)
async def consultar_disponibilidad(
    fecha: str,
    db: Session = Depends(get_db)
):
    """
    Consulta las horas disponibles para una fecha específica
    
    - **fecha**: Fecha a consultar en formato YYYY-MM-DD
    
    Retorna lista de horas disponibles en el horario de atención (09:00 - 20:00)
    """
    # Definir horario de atención (cada 30 minutos)
    horarios_posibles = [
        f"{h:02d}:{m:02d}"
        for h in range(9, 20)
        for m in [0, 30]
    ]
    
    # Obtener reservas confirmadas para esa fecha
    reservas_fecha = crud.get_reservas(
        db=db,
        fecha=fecha,
        estado="confirmada",
        limit=500
    )
    
    # Filtrar horas ocupadas
    horas_ocupadas = {reserva.hora for reserva in reservas_fecha}
    horas_disponibles = [h for h in horarios_posibles if h not in horas_ocupadas]
    
    return horas_disponibles
