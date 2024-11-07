.PHONY: applyMigration createMigration runLocal runBuildDocker runDocker runTest

SHELL := /bin/bash

applyMigration:
	source .env.local && \
	poetry run alembic upgrade head

createMigration:
	source .env.local && \
	poetry run alembic revision --autogenerate -m "new migration"


downgradeMigration:
	source .env.local && \
	poetry run alembic downgrade -1

runLocal:
	source .env.local && \
	poetry run gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 -t 600 app.server:app --log-config ./config.local.ini --log-level debug

runTest:
	source .env.local && \
	pytest --cov=app --cov-fail-under=90 -vv tests/