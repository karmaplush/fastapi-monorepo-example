# FastAPI Monorepo with local dev in compose template

- One DB (PostgreSQL)
- One service as FastAPI (for now)

Just clone it and use `docker compose up` command

General:
- `docker-compose.yml` in root for local development, `docker-compose.prod.yml` - for production.
- `local.Dockerfile` in service for local development, `Dockerfile` - for production.

How to work with FastAPI in local dev:
- Place `.venv` in service directory (`api/.venv`)
- Place `.env` in service directory (`api/.env`)
- If content of `.env` was changed - `Ctrl + C` in compose terminal window and re-launch it for applying changes.

How to deal with migrations via docker compose + alembic:
- Don't forget to create `.env` in api service and put DB string in it (look at `settings.py` for correct ENV name)
- Create migration: `docker-compose run --rm api alembic revision --autogenerate -m "New migration message"`
- Apply migrations manualy: `docker-compose run --rm api alembic upgrade head`
- Cancel last migration: `docker-compose run --rm api alembic downgrade -1`
- Get migrations and their IDs `docker-compose run --rm api alembic history`
- Cancel migration by ID `docker-compose run --rm alembic downgrade <revision_id>`
- How to cancel all migrations `docker-compose run --rm alembic downgrade base`
