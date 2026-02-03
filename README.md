# 💈 SLY Barbershop - Backend API

API REST completa para gestión de reservas de barbería, desarrollada con FastAPI y Python.

## 🚀 Características

- ✅ **API REST completa** con FastAPI
- ✅ **CRUD completo** para reservas (Create, Read, Update, Delete)
- ✅ **Validación de datos** con Pydantic
- ✅ **Prevención de duplicados** - No permite reservas en la misma fecha/hora
- ✅ **Base de datos** SQLite (desarrollo) / PostgreSQL (producción)
- ✅ **ORM SQLAlchemy** para gestión de base de datos
- ✅ **CORS configurado** para integración con frontend
- ✅ **Documentación automática** con Swagger UI
- ✅ **Manejo de errores** centralizado
- ✅ **Código tipado** y bien documentado
- ✅ **Variables de entorno** con python-dotenv

## 📋 Requisitos

- Python 3.10 o superior
- Poetry (gestor de dependencias de Python)

## 🛠️ Instalación

### 1. Instalar Poetry (si no lo tienes)

```bash
# En Linux/Mac/WSL
curl -sSL https://install.python-poetry.org | python3 -

# O usando pip
pip install poetry
```

### 2. Clonar o navegar al directorio del proyecto

```bash
cd barbershop-SLY-backend
```

### 3. Instalar dependencias con Poetry

```bash
# Poetry crea automáticamente el entorno virtual e instala las dependencias
poetry install
```

### 4. Configurar variables de entorno

El archivo `.env` ya está configurado con valores por defecto para desarrollo. Puedes modificarlo según tus necesidades:

```env
DATABASE_URL=sqlite:///./barbershop.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DEBUG=True
```

## ▶️ Ejecutar el servidor

```bash
# Usando Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O activar el shell de Poetry y ejecutar directamente
poetry shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
barbershop-SLY-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── config.py            # Configuración y variables de entorno
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy (tablas)
│   ├── schemas.py           # Schemas Pydantic (validación)
│   ├── crud.py              # Operaciones CRUD
│   └── routers/
│       ├── __init__.py
│       └── reservas.py      # Endpoints de reservas
├── .env                     # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🔌 API Endpoints

### Status

- `GET /` - Información de la API
- `GET /health` - Health check

### Reservas

- `POST /api/reservas/` - Crear nueva reserva
- `GET /api/reservas/` - Listar todas las reservas (con filtros)
- `GET /api/reservas/{id}` - Obtener reserva por ID
- `PUT /api/reservas/{id}` - Actualizar reserva
- `DELETE /api/reservas/{id}` - Eliminar reserva
- `PATCH /api/reservas/{id}/cancelar` - Cancelar reserva
- `GET /api/reservas/disponibilidad/{fecha}` - Consultar disponibilidad

## 📝 Ejemplos de Uso

### Crear una reserva

```bash
curl -X POST "http://localhost:8000/api/reservas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_cliente": "Juan Pérez",
    "email": "juan@email.com",
    "fecha": "2026-02-15",
    "hora": "14:30",
    "servicio": "Corte de pelo"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre_cliente": "Juan Pérez",
  "email": "juan@email.com",
  "fecha": "2026-02-15",
  "hora": "14:30",
  "servicio": "Corte de pelo",
  "estado": "confirmada",
  "created_at": "2026-02-03T10:30:00"
}
```

### Listar reservas

```bash
curl "http://localhost:8000/api/reservas/"
```

**Respuesta:**
```json
{
  "total": 5,
  "reservas": [
    {
      "id": 1,
      "nombre_cliente": "Juan Pérez",
      "email": "juan@email.com",
      "fecha": "2026-02-15",
      "hora": "14:30",
      "servicio": "Corte de pelo",
      "estado": "confirmada",
      "created_at": "2026-02-03T10:30:00"
    }
  ]
}
```

### Obtener reserva por ID

```bash
curl "http://localhost:8000/api/reservas/1"
```

### Actualizar reserva

```bash
curl -X PUT "http://localhost:8000/api/reservas/1" \
  -H "Content-Type: application/json" \
  -d '{
    "hora": "15:00",
    "servicio": "Corte + Barba"
  }'
```

### Cancelar reserva

```bash
curl -X PATCH "http://localhost:8000/api/reservas/1/cancelar"
```

### Eliminar reserva

```bash
curl -X DELETE "http://localhost:8000/api/reservas/1"
```

### Consultar disponibilidad

```bash
curl "http://localhost:8000/api/reservas/disponibilidad/2026-02-15"
```

**Respuesta:**
```json
[
  "09:00", "09:30", "10:00", "10:30", 
  "11:00", "11:30", "12:00", "12:30",
  "15:00", "15:30", "16:00", "16:30"
]
```

## 🔍 Validaciones

La API implementa las siguientes validaciones:

- ✅ **Email válido** - Formato de email correcto
- ✅ **Fecha futura** - No permite reservas en fechas pasadas
- ✅ **Horario laboral** - Solo permite reservas de 09:00 a 20:00
- ✅ **Formato de fecha** - YYYY-MM-DD
- ✅ **Formato de hora** - HH:MM (24 horas)
- ✅ **Sin duplicados** - Previene reservas en la misma fecha/hora
- ✅ **Campos obligatorios** - Valida presencia de datos requeridos
- ✅ **Longitud de campos** - Límites de caracteres

## 🗄️ Base de Datos

### SQLite (Desarrollo)

Por defecto, se usa SQLite que crea un archivo `barbershop.db` localmente. No requiere instalación adicional.

### PostgreSQL (Producción)

Para usar PostgreSQL en producción:

1. Instalar PostgreSQL
2. Crear base de datos:
   ```sql
   CREATE DATABASE barbershop_db;
   ```

3. Instalar driver con Poetry:
   ```bash
   poetry add psycopg2-binary
   ```

4. Actualizar `.env`:
   ```env
   DATABASE_URL=postgresql://usuario:password@localhost:5432/barbershop_db
   ```

### Modelo de Datos: Reserva

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (autoincremental) |
| nombre_cliente | String(100) | Nombre del cliente |
| email | String(100) | Email del cliente |
| fecha | String(10) | Fecha (YYYY-MM-DD) |
| hora | String(5) | Hora (HH:MM) |
| servicio | String(100) | Tipo de servicio |
| estado | Enum | confirmada / cancelada |
| created_at | DateTime | Timestamp de creación |

## 🌐 Integración con Frontend

El backend está configurado con CORS para permitir requests desde:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5500`
- `http://127.0.0.1:5500`

### Ejemplo con JavaScript (Fetch)

```javascript
// Crear reserva
async function crearReserva(datos) {
  const response = await fetch('http://localhost:8000/api/reservas/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.message);
  }
  
  return await response.json();
}

// Listar reservas
async function obtenerReservas() {
  const response = await fetch('http://localhost:8000/api/reservas/');
  return await response.json();
}

// Uso
const nuevaReserva = await crearReserva({
  nombre_cliente: "María García",
  email: "maria@email.com",
  fecha: "2026-02-15",
  hora: "10:00",
  servicio: "Corte de pelo"
});
```

### Ejemplo con Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

// Crear reserva
const crearReserva = async (datos) => {
  const response = await api.post('/reservas/', datos);
  return response.data;
};

// Listar reservas
const obtenerReservas = async () => {
  const response = await api.get('/reservas/');
  return response.data;
};
```

## 🐛 Debugging

Para ver logs detallados:

```bash
poetry run uvicorn app.main:app --reload --log-level debug
```

## 🧪 Testing

Para agregar y ejecutar tests:

```bash
# Agregar dependencias de testing (ya incluidas en dev)
poetry add --group dev pytest pytest-asyncio httpx

# Ejecutar tests
poetry run pytest
```

Para probar la API manualmente, puedes usar:

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman** o **Insomnia**: Importar endpoints
3. **curl**: Ejemplos en este README
4. **Python requests**:

```python
import requests

response = requests.post(
    'http://localhost:8000/api/reservas/',
    json={
        'nombre_cliente': 'Test User',
        'email': 'test@email.com',
        'fecha': '2026-02-15',
        'hora': '10:00',
        'servicio': 'Corte'
    }
)
print(response.json())
```

## 📦 Dependencias Principales

- **FastAPI** (^0.109.0) - Framework web moderno y rápido
- **Uvicorn** (^0.27.0) - Servidor ASGI de alto rendimiento
- **SQLAlchemy** (^2.0.25) - ORM para Python
- **Pydantic** (^2.5.3) - Validación de datos
- **python-dotenv** (^1.0.0) - Gestión de variables de entorno

Gestión de dependencias con **Poetry** para entornos reproducibles y resolución de conflictos.

## 🚀 Despliegue en Producción

### Consideraciones

1. **Cambiar a PostgreSQL** en lugar de SQLite
2. **Configurar `DEBUG=False`** en `.env`
3. **Usar secrets seguros** para credenciales
4. **Configurar HTTPS** con certificados SSL
5. **Actualizar CORS_ORIGINS** con dominios de producción

### Ejemplo con Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Copiar archivos de configuración
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias sin crear entorno virtual (usar el de Docker)
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY ./app ./app
COPY .env .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Ejemplo con Gunicorn + Uvicorn Workers

```bash
poetry add gunicorn
poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📄 Licencia

Este proyecto es de uso privado para SLY Barbershop.

## 👨‍💻 Soporte

Para preguntas o problemas:
1. Revisar la documentación en `/docs`
2. Consultar los logs del servidor
3. Verificar configuración de `.env`

---

**Desarrollado con ❤️ usando FastAPI y Python**
