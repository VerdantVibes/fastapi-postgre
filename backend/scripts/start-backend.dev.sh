#!/bin/bash
alembic upgrade head
poetry run gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 -t 600 app.server:app --log-config ./config.ini --log-level debug