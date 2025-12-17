# ===========================================
# ThePaper Graph - Makefile
# ===========================================

.PHONY: help up down build logs shell migrate makemigrations test clean

# Default target
help:
	@echo "ThePaper Graph - Available Commands"
	@echo "===================================="
	@echo "  make up           - Start all services"
	@echo "  make up-build     - Build and start all services"
	@echo "  make down         - Stop all services"
	@echo "  make build        - Build all images"
	@echo "  make logs         - View logs (all services)"
	@echo "  make logs-backend - View backend logs"
	@echo "  make logs-celery  - View celery logs"
	@echo "  make shell        - Open Django shell"
	@echo "  make bash         - Open bash in backend container"
	@echo "  make migrate      - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make clean        - Remove containers and volumes"
	@echo "  make ps           - Show running containers"

# Start services
up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

up-build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Stop services
down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

# Build images
build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build

# View logs
logs:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

logs-backend:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f backend

logs-celery:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f celery

# Shell access
shell:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend python manage.py shell

bash:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend bash

# Database operations
migrate:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend python manage.py migrate

makemigrations:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend python manage.py makemigrations

# Cleanup
clean:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v --remove-orphans

# Status
ps:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml ps

