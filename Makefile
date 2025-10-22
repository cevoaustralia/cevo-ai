.PHONY: help build up down clean logs run restart restart-frontend rebuild-frontend

help:
	@echo "Energy Retailer Chatbot - Local Development"
	@echo ""
	@echo "Commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - Show service logs"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  run       - Alias for up"
	@echo "  restart   - Restart all services"
	@echo "  restart-frontend - Restart frontend only"
	@echo "  rebuild-frontend - Rebuild and restart frontend"

build:
	@echo "Building Docker images..."
	docker-compose build --no-cache

up:
	@echo "Starting Energy Retailer Chatbot..."
	@if [ -f .env ]; then \
		echo "Loading environment from .env file"; \
	else \
		if [ -z "$$AWS_BEARER_TOKEN_BEDROCK" ]; then \
			echo "Error: AWS_BEARER_TOKEN_BEDROCK not set and no .env file found"; \
			echo "Either create .env file or run: export AWS_BEARER_TOKEN_BEDROCK='your-api-key'"; \
			exit 1; \
		fi; \
	fi
	docker-compose up -d
	@echo "Services starting..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:2024"

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

restart-frontend:
	docker-compose restart frontend

rebuild-frontend:
	@echo "Rebuilding frontend container..."
	docker-compose build --no-cache frontend
	docker-compose up -d frontend

run: up

clean:
	docker-compose down -v
	docker system prune -f