# Job Tracker API

API REST para llevar seguimiento del proceso de búsqueda de empleo: empresas, vacantes publicadas por esas empresas, y aplicaciones enviadas a esas vacantes, con control de estatus (aplicado → entrevista → oferta / rechazado).

Construida con **FastAPI**, **SQLAlchemy 2.0** y **PostgreSQL**, con una arquitectura por capas (modelos → repositorios → servicios → esquemas → rutas) y una suite de 57 tests automatizados.

## Demo en vivo

**API desplegada:** [Demo en vivo](https://job-tracker-api-qugs.onrender.com)

**Documentación interactiva (Swagger UI):** [Probar la API](https://job-tracker-api-qugs.onrender.com/docs)

> Nota: está desplegada en el plan gratuito de Render, así que si nadie la ha usado en los últimos 15 minutos, la primera petición puede tardar hasta un minuto en responder mientras el servicio "despierta". Es normal.

## Tecnologías

- **FastAPI** — framework web y generación automática de documentación OpenAPI
- **SQLAlchemy 2.0** — ORM
- **Pydantic v2** — validación de datos y schemas
- **Alembic** — migraciones de base de datos versionadas
- **PostgreSQL** — base de datos relacional
- **pytest** — testing
- **Ruff** — linter para mantener estilo de código, imports ordenados y docstrings consistentes
- **Docker Compose** — entorno de base de datos local
- **Render + Neon** — hosting de la API y de la base de datos en producción

## Estructura del proyecto

job-tracker-api/
├── app/
│   ├── models/               # Modelos de SQLAlchemy (Empresa, Vacante, Aplicacion)
│   ├── repositories/         # Acceso a datos (una clase por entidad + base genérica)
│   ├── services/             # Lógica de negocio y reglas de validación
│   ├── routes/               # Endpoints HTTP (FastAPI routers)
│   ├── schemas/              # Schemas de Pydantic (request/response)
│   ├── database.py           # Configuración de conexión y sesión de SQLAlchemy
│   ├── exception_handlers.py # Traducción de excepciones de dominio a respuestas HTTP
│   └── logging_config.py
├── alembic/                  # Migraciones versionadas del esquema
├── tests/                    # Suite de tests (servicios, rutas, end-to-end)
├── main.py                   # Punto de entrada de la aplicación
├── docker-compose.yml        # Postgres local para desarrollo
├── requirements.txt          # Dependencias del proyecto
└── .env.example              # Plantilla de variables de entorno

## Modelo de datos y reglas de negocio

Empresa 1───N Vacante 1───N Aplicacion

- Una **Empresa** tiene muchas **Vacantes**. El nombre de la empresa debe ser único.
- Una **Vacante** pertenece a una Empresa y tiene muchas **Aplicaciones**.
- Una **Aplicación** avanza por un flujo de estatus controlado:

  ```
  aplicado ──► entrevista ──► oferta
       │            │
       └──► rechazado ◄──────┘
  ```

  Cualquier transición fuera de ese flujo (por ejemplo, saltar directo de "aplicado" a "oferta", o intentar mover una aplicación ya "rechazada") es rechazada por la API.

- **Eliminación en cascada:** borrar una vacante elimina automáticamente todas sus aplicaciones asociadas (a nivel de base de datos, mediante `ON DELETE CASCADE`).

## Instalación y ejecución local

### Requisitos

- Python 3.14+
- Docker y Docker Compose (para la base de datos local)

### Pasos

1. Clona el repositorio e instala las dependencias:

   ```bash
   git clone https://github.com/jaflores9891-glitch/job-tracker-api.git
   cd job-tracker-api
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Levanta PostgreSQL con Docker:

   ```bash
   docker-compose up -d
   ```

3. Crea la base de datos separada para tests (el contenedor solo crea `job_tracker` por defecto):

   ```bash
   docker exec -it job_tracker_db psql -U jobtracker -d job_tracker -c "CREATE DATABASE job_tracker_test;"
   ```

4. Copia el archivo de variables de entorno y ajústalo si es necesario:

   ```bash
   cp .env.example .env
   ```

   Con Docker Compose, los valores por defecto ya funcionan (`jobtracker` / `jobtracker123` / `job_tracker`).

5. Aplica las migraciones:

   ```bash
   alembic upgrade head
   ```

6. Levanta el servidor de desarrollo:

   ```bash
   uvicorn main:app --reload
   ```

   La API queda disponible en `http://localhost:8000`, y la documentación interactiva en `http://localhost:8000/docs`.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Cadena de conexión a la base de datos principal |
| `TEST_DATABASE_URL` | Cadena de conexión a la base de datos usada para tests (distinta de la principal) |

## Endpoints principales

| Recurso | Método y ruta | Descripción |
|---|---|---|
| Empresas | `POST /empresas/` | Crear empresa |
| | `GET /empresas/` | Listar empresas |
| | `GET /empresas/{id}` | Obtener empresa por id |
| | `PATCH /empresas/{id}` | Actualizar empresa |
| | `DELETE /empresas/{id}` | Eliminar empresa |
| Vacantes | `POST /vacantes/` | Crear vacante |
| | `GET /vacantes/empresa/{empresa_id}` | Listar vacantes de una empresa |
| | `GET /vacantes/{id}` | Obtener vacante por id |
| | `PATCH /vacantes/{id}` | Actualizar vacante |
| | `DELETE /vacantes/{id}` | Eliminar vacante (borra sus aplicaciones en cascada) |
| Aplicaciones | `POST /aplicaciones/` | Registrar una aplicación a una vacante |
| | `GET /aplicaciones/vacante/{vacante_id}` | Listar aplicaciones de una vacante |
| | `GET /aplicaciones/?estatus={estatus}` | Listar aplicaciones filtradas por estatus |
| | `GET /aplicaciones/{id}` | Obtener aplicación por id |
| | `PATCH /aplicaciones/{id}/estatus` | Cambiar el estatus de una aplicación |
| | `DELETE /aplicaciones/{id}` | Eliminar aplicación |

La documentación completa, con los schemas de request/response y la posibilidad de probar cada endpoint, está en `/docs` (Swagger UI) tanto en local como en la [demo en vivo](https://job-tracker-api-qugs.onrender.com/docs).

## Tests

El proyecto cuenta con más de 60 tests automatizados, organizados en tres niveles:

- **Servicios** — lógica de negocio de cada entidad, incluyendo validaciones y transiciones de estatus
- **Rutas** — comportamiento de cada endpoint HTTP, incluyendo casos de error (404, 409, 422)
- **End-to-end** — el flujo completo de negocio a través de la API real, de principio a fin

Correr toda la suite:

```bash
pytest -v
```

Correr con reporte de cobertura:

```bash
pytest --cov=app
```

## Calidad de código

El proyecto usa [Ruff](https://docs.astral.sh/ruff/) para linting, con las siguientes reglas activas: `E` (pycodestyle), `F` (pyflakes), `I` (orden de imports) y `D` (docstrings, convención Google). Los tests y las migraciones autogeneradas de Alembic están exentos de la regla de docstrings.

Correr el linter:

```bash
ruff check .
```

Todo el código de `app/` (modelos, repositorios, servicios y rutas) tiene docstrings siguiendo la convención de Google.

## Despliegue

- **API:** desplegada en [Render](https://render.com) (plan gratuito), corriendo `alembic upgrade head` en cada arranque para mantener el esquema actualizado.
- **Base de datos:** [Neon](https://neon.com) (Postgres serverless), separada del entorno de desarrollo local.

## Autor

**Jesu Flores**
