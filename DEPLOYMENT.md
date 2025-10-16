# Energy Retailer Chatbot Deployment Guide

## Architecture Overview

The system implements a 5-agent hierarchy:
1. **Supervisor Agent** - Routes queries to appropriate agents
2. **Current Customer Agent** - Handles existing customer queries
3. **New Connection Customer Agent** - Handles new customer onboarding
4. **Switch Provider Agent** - Handles customer switching
5. **Address Validation Agent** - Validates service availability

## Local Deployment (Docker)

### Prerequisites
- Docker and Docker Compose
- AWS Bedrock API key

### Setup
1. Set environment variable:
```bash
export AWS_BEARER_TOKEN_BEDROCK="your-api-key-here"
```

2. Start services:
```bash
docker-compose up -d
```

3. Access application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:2024

## AWS Cloud Deployment

### Basic Setup (Cheapest Services)
1. Deploy infrastructure:
```bash
aws cloudformation create-stack \
  --stack-name energy-chatbot \
  --template-body file://aws-deploy.yml \
  --parameters ParameterKey=BedrockApiKey,ParameterValue=your-api-key
```

2. Deploy containers to ECS Fargate (cheapest compute option)

### Services Used:
- **ECS Fargate** - Serverless containers (cheapest compute)
- **RDS PostgreSQL t3.micro** - Database (free tier eligible)
- **Application Load Balancer** - Traffic distribution
- **Bedrock Claude 3.5** - AI agents

## Sample Queries

### Current Customer:
- "Why is my bill so high?" (requires customer number)
- "Can you explain my bill?"
- "What's my current usage?"

### New Customer:
- "I want to switch energy providers"
- "Can I get energy at my new address?"
- "How do I sign up for energy?"

## Agent Flow

1. User query → **Supervisor Agent**
2. Supervisor analyzes and routes to:
   - **Current Customer Agent** (if billing/account query)
   - **New Customer Agent** (if switching/new connection)
3. Agents use tools:
   - Database queries for customer data
   - Address validation via MCP server
   - Bedrock Claude 3.5 for responses