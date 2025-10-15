# Local Deployment Guide

## Prerequisites
- Docker and Docker Compose
- AWS Bedrock API key
- Python 3.11+ (for testing)
- Node.js 18+ (for frontend tests)

## Quick Start

1. **Set API Key**
```bash
export AWS_BEARER_TOKEN_BEDROCK="your-bedrock-api-key"
```

2. **Deploy with Make**
```bash
make run
```

3. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:2024

## Testing

### Run All Tests
```bash
make test
```

### Run Specific Test Types
```bash
make test-unit      # Unit tests only
make test-func      # Functional tests only
make test-int       # Integration tests only
```

### Frontend Tests
```bash
npm test
```

## Available Commands

```bash
make help           # Show all commands
make build          # Build Docker images
make up             # Start services
make down           # Stop services
make logs           # View logs
make clean          # Clean up containers
```

## Sample Usage

1. **Current Customer:**
   - Navigate to Energy Assistant
   - Enter Customer Number: `12345`
   - Query: "Why is my bill so high?"
   - Upload bill PDF (optional)

2. **New Customer:**
   - Navigate to Energy Assistant
   - Enter Address: "123 Collins St, Melbourne VIC"
   - Query: "I want to switch providers"
   - Upload current bill for switching (optional)

## Troubleshooting

- **API Key Error**: Ensure AWS_BEARER_TOKEN_BEDROCK is exported
- **Service Not Ready**: Wait 10-15 seconds after `make up`
- **Test Failures**: Run `make logs` to check service status