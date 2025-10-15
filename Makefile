.PHONY: help build up down test test-unit test-functional test-integration clean logs install-deps run test-env restart restart-frontend rebuild-frontend

help:
	@echo "Energy Retailer Chatbot - Local Development"
	@echo ""
	@echo "Commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  test      - Run all tests"
	@echo "  test-unit - Run unit tests only"
	@echo "  test-func - Run functional tests only"
	@echo "  test-int  - Run integration tests only"
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

test: test-env install-deps
	@echo "Waiting for services to be ready..."
	@sleep 10
	cd backend && python -m pytest tests/ -v

test-unit: install-deps
	cd backend && python -m pytest tests/test_unit.py -v

test-func: test-env install-deps
	@sleep 10
	cd backend && python -m pytest tests/test_functional.py -v

test-int: test-env install-deps
	@sleep 15
	cd backend && python -m pytest tests/test_integration.py -v

logs:
	docker-compose logs -f

install-deps:
	@echo "Installing Python dependencies..."
	pip install -r backend/requirements.txt

test-env:
	@echo "Starting test environment..."
	docker-compose -f docker-compose.test.yml up -d

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
	docker-compose -f docker-compose.test.yml down -v
	docker system prune -f