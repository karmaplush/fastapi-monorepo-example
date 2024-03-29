# FastAPI Monorepo with Local Development in Docker Compose Template

* One PostgreSQL Database (for now)
* One Service as FastAPI (for now) with SQLAlchemy 2, Pydantic 2, Alembic.

## Setup

* Clone the repository.
* Run `docker compose up` for local development.

**General forkflow logic**

* `docker-compose.yml` in the root for local development, `docker-compose.prod.yml` for production.
* Service-specific `local.Dockerfile` for local development, and a `Dockerfile` for production builds.

## Local Development with FastAPI

1. **Create virtual environment:** Place `.venv` within the service directory (`api/.venv`).
2. **Environment variables:** Create a `.env` file in the service directory (`api/.env`).
3. **Apply changes:** If the `.env` file is modified, restart Docker Compose (`Ctrl+C` and then `docker-compose up`) to ensure changes take effect.

### Installing New Modules (using `loguru` as an example)

1. **Activate virtual environment:** `cd api; source .venv/bin/activate`
2. **Install module:** `pip install loguru`
3. **Rebuild image:**  `cd ..; docker compose build --no-cache api`
4. **Start containers:** `docker compose up`

### Alembic Migrations within Docker Compose

1. **Environment variables:** Ensure the database connection string is in the `api` service's `.env` file (refer to `settings.py` for the correct environment variable name).
2. **Generate migration:** `docker compose run --rm api alembic revision --autogenerate -m "New migration message"`
3. **Apply migrations:** `docker compose run --rm api alembic upgrade head`
4. **Downgrade (last migration):** `docker compose run --rm api alembic downgrade -1`
5. **List migrations:** `docker compose run --rm api alembic history`
6. **Downgrade (by ID):** `docker compose run --rm api alembic downgrade <revision_id>`
7. **Reset all migrations:** `docker compose run --rm api alembic downgrade base`
