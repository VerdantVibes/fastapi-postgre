import subprocess
import uvicorn
import os
import logging
from app.config import Environment


def alembic_upgrade():
    cmd = "alembic upgrade head"
    subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def run_server():
    config = uvicorn.Config(
        "app.server:app",
        host="0.0.0.0",
        port=8000,
        log_config="./config.ini",
        loop="uvloop",
    )

    if os.getenv("ENVIRONMENT") == Environment.DEVELOPMENT.value:
        config.log_level = logging.DEBUG
        config.reload = False

    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    alembic_upgrade()
    run_server()
