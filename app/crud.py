"""
Operaciones CRUD (Create, Read, Update, Delete) para Reservas
Contiene la lógica de negocio para interactuar con la base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from . import models, schemas


def get_reserva(db: Session, reserva_id: int) -> Optional[models.Reserva]:
    """
    Obtiene una reserva por ID
    
    Args:
        db: Sesión de base de datos
        reserva_id: ID de la reserva
    
    Returns:
        Objeto Reserva o None si no existe
    """
    return db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()


def get_reservas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    fecha: Optional[str] = None,
    estado: Optional[str] = None
) -> List[models.Reserva]:
    """
    Obtiene lista de reservas con filtros opcionales
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a devolver
        fecha: Filtrar por fecha específica (YYYY-MM-DD)
        estado: Filtrar por estado (confirmada/cancelada)
    
    Returns:
        Lista de objetos Reserva
    """
    query = db.query(models.Reserva)
    
    # Aplicar filtros si están presentes
    if fecha:
        query = query.filter(models.Reserva.fecha == fecha)
    if estado:
        query = query.filter(models.Reserva.estado == estado)
    
    # Ordenar por fecha y hora (más recientes primero)
    query = query.order_by(
        models.Reserva.fecha.desc(),
        models.Reserva.hora.desc()
    )
    
    return query.offset(skip).limit(limit).all()


def get_reservas_count(
    db: Session,
    fecha: Optional[str] = None,
    estado: Optional[str] = None
) -> int:
    """
    Cuenta el total de reservas con filtros opcionales
    
    Args:
        db: Sesión de base de datos
        fecha: Filtrar por fecha específica
        estado: Filtrar por estado
    
    Returns:
        Número total de reservas
    """
    query = db.query(models.Reserva)
    
    if fecha:
        query = query.filter(models.Reserva.fecha == fecha)
    if estado:
        query = query.filter(models.Reserva.estado == estado)
    
    return query.count()


def check_reserva_duplicada(
    db: Session,
    fecha: str,
    hora: str,
    reserva_id: Optional[int] = None
) -> bool:
    """
    Verifica si ya existe una reserva en la misma fecha y hora
    
    Args:
        db: Sesión de base de datos
        fecha: Fecha de la reserva (YYYY-MM-DD)
        hora: Hora de la reserva (HH:MM)
        reserva_id: ID de reserva a excluir (para actualizaciones)
    
    Returns:
        True si existe una reserva duplicada, False si no
    """
    query = db.query(models.Reserva).filter(
        and_(
            models.Reserva.fecha == fecha,
            models.Reserva.hora == hora,
            models.Reserva.estado == models.EstadoReserva.CONFIRMADA
        )
    )
    
    # Excluir la reserva actual si estamos actualizando
    if reserva_id:
        query = query.filter(models.Reserva.id != reserva_id)
    
    return query.first() is not None


def create_reserva(db: Session, reserva: schemas.ReservaCreate) -> models.Reserva:
    """
    Crea una nueva reserva
    
    Args:
        db: Sesión de base de datos
        reserva: Datos de la reserva a crear
    
    Returns:
        Objeto Reserva creado
    
    Raises:
        ValueError: Si ya existe una reserva en la misma fecha y hora
    """
    # Verificar duplicados
    if check_reserva_duplicada(db, reserva.fecha, reserva.hora):
        raise ValueError(
            f"Ya existe una reserva confirmada para el {reserva.fecha} a las {reserva.hora}"
        )
    
    # Crear nueva reserva
    db_reserva = models.Reserva(
        nombre_cliente=reserva.nombre_cliente,
        email=reserva.email,
        fecha=reserva.fecha,
        hora=reserva.hora,
        servicio=reserva.servicio,
        estado=models.EstadoReserva.CONFIRMADA
    )
    
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva


def update_reserva(
    db: Session,
    reserva_id: int,
    reserva_update: schemas.ReservaUpdate
) -> Optional[models.Reserva]:
    """
    Actualiza una reserva existente
    
    Args:
        db: Sesión de base de datos
        reserva_id: ID de la reserva a actualizar
        reserva_update: Datos a actualizar
    
    Returns:
        Objeto Reserva actualizado o None si no existe
    
    Raises:
        ValueError: Si la actualización genera un duplicado
    """
    db_reserva = get_reserva(db, reserva_id)
    
    if not db_reserva:
        return None
    
    # Preparar datos para actualizar
    update_data = reserva_update.model_dump(exclude_unset=True)
    
    # Si se actualiza fecha u hora, verificar duplicados
    nueva_fecha = update_data.get('fecha', db_reserva.fecha)
    nueva_hora = update_data.get('hora', db_reserva.hora)
    
    if ('fecha' in update_data or 'hora' in update_data):
        if check_reserva_duplicada(db, nueva_fecha, nueva_hora, reserva_id):
            raise ValueError(
                f"Ya existe una reserva confirmada para el {nueva_fecha} a las {nueva_hora}"
            )
    
    # Aplicar actualizaciones
    for field, value in update_data.items():
        setattr(db_reserva, field, value)
    
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva


def delete_reserva(db: Session, reserva_id: int) -> bool:
    """
    Elimina una reserva permanentemente
    
    Args:
        db: Sesión de base de datos
        reserva_id: ID de la reserva a eliminar
    
    Returns:
        True si se eliminó, False si no existía
    """
    db_reserva = get_reserva(db, reserva_id)
    
    if not db_reserva:
        return False
    
    db.delete(db_reserva)
    db.commit()
    
    return True


def cancel_reserva(db: Session, reserva_id: int) -> Optional[models.Reserva]:
    """
    Cancela una reserva (cambia estado a CANCELADA)
    
    Args:
        db: Sesión de base de datos
        reserva_id: ID de la reserva a cancelar
    
    Returns:
        Objeto Reserva cancelado o None si no existe
    """
    db_reserva = get_reserva(db, reserva_id)
    
    if not db_reserva:
        return None
    
    db_reserva.estado = models.EstadoReserva.CANCELADA
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva
