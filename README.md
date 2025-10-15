# Cevo AI - Energy Retailer Chatbot

Intelligent energy management platform with agentic workflow chatbot system.

## Features

- **Agentic Workflow**: 5-agent hierarchy (Supervisor, Current Customer, New Customer, Switch Provider, Address Validation)
- **Modern UI**: Material-UI React frontend with responsive design
- **Context Management**: Persistent conversation context across chat sessions
- **AWS Bedrock Integration**: Claude 3 Haiku model with fallback mechanisms
- **Full Stack**: FastAPI backend, PostgreSQL database, Docker containerization

## Quick Start

### Prerequisites
- Docker and Docker Compose
- AWS Bedrock API key

### Setup

1. **Clone and navigate**:
   ```bash
   git clone <repository>
   cd cevo-ai
   ```

2. **Configure environment**:
   ```bash
   # Create .env file with your AWS Bedrock API key
   echo "AWS_BEARER_TOKEN_BEDROCK=your-api-key-here" > .env
   ```

3. **Start services**:
   ```bash
   make up
   ```

4. **Access application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:2024

## Development Commands

```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start all services
make down          # Stop all services
make logs          # View service logs
make restart       # Restart all services
make clean         # Clean up containers and volumes

# Frontend specific
make restart-frontend   # Restart frontend only
make rebuild-frontend   # Rebuild and restart frontend

# Testing
make test          # Run all tests
make test-unit     # Unit tests only
make test-func     # Functional tests only
make test-int      # Integration tests only
```

## Architecture

### Services
- **Frontend**: React + Material-UI (Port 3000)
- **Backend**: FastAPI + Python (Port 2024)
- **Database**: PostgreSQL (Port 5432)

### Agent System
- **Supervisor Agent**: Routes queries to specialized agents
- **Current Customer Agent**: Handles billing/account queries
- **New Customer Agent**: Manages new connections/switching
- **Context Manager**: Maintains conversation state

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_BEARER_TOKEN_BEDROCK` | AWS Bedrock API key | Yes |
| `DB_HOST` | Database host | Auto-set |
| `DB_NAME` | Database name | Auto-set |
| `DB_USER` | Database user | Auto-set |
| `DB_PASSWORD` | Database password | Auto-set |

## Troubleshooting

**Services not starting?**
```bash
make logs  # Check service logs
make clean && make build && make up  # Fresh rebuild
```

**Frontend changes not reflecting?**
```bash
make rebuild-frontend  # Rebuild frontend container
```

**Database issues?**
```bash
make down
docker volume rm cevo-ai_postgres_data
make up  # Fresh database
```