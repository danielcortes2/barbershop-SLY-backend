# Backend con FastAPI, SQLAlchemy y Alembic

## 📋 Resumen

Se ha migrado el backend de **Node.js/SQLite** a **Python 3.11/FastAPI** con:
- ✅ **FastAPI** - Framework web moderno y rápido
- ✅ **SQLAlchemy 2.0** - ORM para base de datos
- ✅ **Alembic** - Sistema de migraciones para control de versiones de BD
- ✅ **MySQL** - Base de datos relacional persistente

## 🏗️ Estructura del Proyecto

```
barbershop-SLY-backend/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuración desde variables de entorno
│   ├── database.py               # Conexión a BD y dependencias
│   ├── models.py                 # Modelos SQLAlchemy (Barber, Service, Appointment)
│   ├── schemas.py                # Esquemas Pydantic para validación
│   └── routes/                   # Endpoints de la API
│       ├── __init__.py
│       ├── barbers.py           # CRUD de barberos
│       ├── services.py          # CRUD de servicios
│       └── appointments.py      # CRUD de citas
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py # Primera migración
│   ├── env.py                    # Configuración de Alembic
│   ├── script.py.mako            # Template para nuevas migraciones
│   └── __init__.py
├── main.py                        # Aplicación FastAPI principal
├── requirements.txt               # Dependencias Python
├── alembic.ini                    # Configuración de Alembic
├── .env.example                   # Ejemplo de variables de entorno
└── Dockerfile                     # Docker para el backend
```

## 🗄️ Modelos de Datos

### 1. **Barber** (Barbero)
```python
- id: int (PK)
- name: str (UNIQUE)
- phone: str
- created_at: datetime
- appointments: List[Appointment] (relación)
```

### 2. **Service** (Servicio)
```python
- id: int (PK)
- name: str (UNIQUE)
- duration: int (minutos)
- price: Decimal(10,2)
- created_at: datetime
- appointments: List[Appointment] (relación)
```

### 3. **Appointment** (Cita)
```python
- id: int (PK)
- client_name: str
- client_phone: str
- barber_id: int (FK -> Barber)
- service_id: int (FK -> Service)
- appointment_date: datetime (UNIQUE por barbero)
- status: Enum(pending, confirmed, completed, cancelled)
- notes: text
- created_at: datetime
- updated_at: datetime
```

## 🔧 Comandos de Alembic

### Crear una nueva migración (auto-generada)
```bash
cd barbershop-SLY-backend
alembic revision --autogenerate -m "Descripción del cambio"
```

### Crear migración manual
```bash
alembic revision -m "Nombre de la migración"
```

### Aplicar migraciones
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade 001_initial_schema

# Aplicar N migraciones
alembic upgrade +2
```

### Ver estado de migraciones
```bash
# Ver historial de migraciones aplicadas
alembic history

# Ver migraciones pendientes
alembic current
```

### Revertir migraciones
```bash
# Revertir la última migración
alembic downgrade -1

# Revertir a una migración específica
alembic downgrade 001_initial_schema
```

## 🚀 Iniciar con Docker

### 1. Asegurar que existe `.env`
```bash
cp .env.example .env
```

### 2. Iniciar los contenedores
```bash
docker-compose up -d
```

El Dockerfile ejecutará automáticamente:
1. `alembic upgrade head` - Aplicar todas las migraciones
2. Iniciar `uvicorn` con el servidor FastAPI

### 3. Ver logs
```bash
docker-compose logs -f backend
```

### 4. Probar la API
- Docs interactivos: http://localhost:3001/docs
- Redoc: http://localhost:3001/redoc
- Health check: http://localhost:3001/health

## 📚 Endpoints Disponibles

### Barberos
- `GET /api/v1/barbers` - Obtener todos
- `GET /api/v1/barbers/{id}` - Obtener uno
- `POST /api/v1/barbers` - Crear
- `PUT /api/v1/barbers/{id}` - Actualizar
- `DELETE /api/v1/barbers/{id}` - Eliminar

### Servicios
- `GET /api/v1/services` - Obtener todos
- `GET /api/v1/services/{id}` - Obtener uno
- `POST /api/v1/services` - Crear
- `PUT /api/v1/services/{id}` - Actualizar
- `DELETE /api/v1/services/{id}` - Eliminar

### Citas
- `GET /api/v1/appointments` - Obtener todas
- `GET /api/v1/appointments/{id}` - Obtener una
- `GET /api/v1/appointments/barber/{barber_id}` - Citas de un barbero
- `POST /api/v1/appointments` - Crear
- `PUT /api/v1/appointments/{id}` - Actualizar
- `DELETE /api/v1/appointments/{id}` - Cancelar (soft delete)

## 📝 Estructura de una Migración

```python
"""Descripción de cambios

Revision ID: 002_add_field_x
Revises: 001_initial_schema
Create Date: 2024-02-03
"""

from alembic import op
import sqlalchemy as sa

revision = '002_add_field_x'
down_revision = '001_initial_schema'

def upgrade() -> None:
    """Cambios a aplicar"""
    op.add_column('appointments', sa.Column('new_field', sa.String(255)))

def downgrade() -> None:
    """Cambios a revertir"""
    op.drop_column('appointments', 'new_field')
```

## 🔄 Ciclo de Desarrollo

1. **Modificar modelo** en `app/models.py`
2. **Crear migración automática**:
   ```bash
   alembic revision --autogenerate -m "Cambio en modelo X"
   ```
3. **Revisar migración** en `alembic/versions/`
4. **Aplicar migración**:
   ```bash
   alembic upgrade head
   ```
5. **Probar cambios** en la API

## ⚠️ Notas Importantes

1. **Alembic automático** detecta cambios en modelos que cumplan:
   - Añadir/remover columnas
   - Cambios en tipos de datos
   - Cambios en restricciones
   - NO detecta cambios en comentarios

2. **Migraciones manuales** recomendadas para:
   - Migración de datos
   - Cambios complejos de esquema
   - Operaciones personalizadas

3. **Base de datos persistente**:
   - Los datos se guardan en volumen Docker `barbershop-mysql-data`
   - No se pierden al hacer `docker-compose down`
   - Usar `docker volume rm barbershop_barbershop-mysql-data` para limpiar

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
```bash
# Asegurar que .env está en la raíz del backend
# Y que Dockerfile ejecuta desde la raíz correcta
```

### Migración rechazada
```bash
# Ver estado actual
alembic current

# Ver si hay cambios sin aplicar
alembic history
```

### Erro de conexión a MySQL
```bash
# Verificar que MySQL está levantado
docker-compose logs mysql

# Reiniciar contenedores
docker-compose down && docker-compose up -d
```
