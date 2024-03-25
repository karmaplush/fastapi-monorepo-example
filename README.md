# FastAPI Monorepo with local dev in compose template

Just clone it and use `docker compose up` command

How to work in local dev:
- Place `.venv` in service directory (`api/.venv`)
- Place `.env` in service directory (`api/.env`)
- If content of `.env` was changed - `Ctrl + C` in compose terminal window and re-launch it for applying changes.
- `docker-compose.yml` in root for local development, `docker-compose.prod.yml` - for production.
- `local.Dockerfile` in service for local development, `Dockerfile` - for production.
