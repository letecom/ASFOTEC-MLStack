.PHONY: up down logs

up:
	docker compose -f infra/docker/docker-compose.dev.yml up -d --build

down:
	docker compose -f infra/docker/docker-compose.dev.yml down

logs:
	docker compose -f infra/docker/docker-compose.dev.yml logs -f
