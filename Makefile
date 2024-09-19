.PHONY: runBuildDocker runDocker

SHELL := /bin/bash

runBuildLocalDocker:
	docker compose -f docker-compose.local.yml up -d --build

runLocalDocker:
	docker compose -f docker-compose.local.yml up -d

runBuildDevDocker:
	docker compose -f docker-compose.dev.yml up -d --build

runDevDocker:
	docker compose -f docker-compose.dev.yml up -d
