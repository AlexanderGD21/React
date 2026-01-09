# DigitalEducas

Plataforma educativa con un frontend en React y una API REST en Django.

## Estructura

```text
src/                 # Interfaz React
backend/users/       # Usuarios, verificación y autenticación JWT
backend/courses/     # Cursos, lecciones, cuestionarios y certificados
backend/payments/    # Módulo reservado; no está habilitado todavía
```

## Inicio rápido

### Backend

Requiere Python 3.11+ y PostgreSQL. Desde `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `backend/.env` con las credenciales locales de PostgreSQL y SMTP. Nunca subas este archivo al repositorio. Después ejecuta:

```powershell
python manage.py migrate
python manage.py runserver
```

La API queda en `http://localhost:8000/api/`.

### Frontend

Desde la raíz del repositorio:

```powershell
npm install
npm start
```

La aplicación se abre en `http://localhost:3000` y consulta la API de desarrollo. Si tu API usa otra dirección, crea un archivo `.env.local` con:

```text
REACT_APP_API_URL=http://localhost:8000/api
```

## Endpoints disponibles

- `POST /api/register/`, `POST /api/verify/`
- `POST /api/forgot-password/`, `POST /api/reset-password/`
- `POST /api/token/`, `POST /api/token/refresh/`
- `GET /api/courses/`, `GET /api/courses/:id/`, `GET /api/courses/:id/quiz/`
- `POST /api/courses/:id/submit/` (requiere JWT)

## Seguridad y despliegue

- Configura `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` y `CSRF_TRUSTED_ORIGINS` en producción.
- Los códigos de verificación expiran en 15 minutos por defecto y los endpoints sensibles están limitados por IP.
- Ejecuta `npm test -- --watchAll=false` y `python manage.py check` antes de desplegar.
- El módulo de pagos permanece en el repositorio, pero está deshabilitado hasta definir el proveedor y el flujo de cobro.
