# C-A-D-E API Documentation

## Base URL

```
http://localhost:8000
```

## API Endpoints

### System Endpoints

#### GET /
Get API information

**Response:**
```json
{
  "name": "C-A-D-E API",
  "version": "1.0.0",
  "description": "Community Application Development Environment",
  "status": "operational"
}
```

#### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

### Agent Endpoints

#### GET /agents
List all agents

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_1",
      "name": "My Agent",
      "description": "An AI agent",
      "category": "Autonomous Agents",
      "framework": "LangChain",
      "language": "Python",
      "code": "# Agent code here"
    }
  ]
}
```

#### POST /agents
Create a new agent

**Request Body:**
```json
{
  "id": "agent_1",
  "name": "My Agent",
  "description": "An AI agent",
  "category": "Autonomous Agents",
  "framework": "LangChain",
  "language": "Python",
  "code": "# Agent code here"
}
```

**Response:**
```json
{
  "message": "Agent created",
  "agent": { /* agent object */ }
}
```

#### GET /agents/{agent_id}
Get agent details

**Parameters:**
- `agent_id` (path): Agent ID

**Response:**
```json
{
  "agent": {
    "id": "agent_1",
    "name": "My Agent",
    "description": "An AI agent",
    "category": "Autonomous Agents",
    "framework": "LangChain",
    "language": "Python",
    "code": "# Agent code here"
  }
}
```

**Error Response (404):**
```json
{
  "detail": "Agent not found"
}
```

#### PUT /agents/{agent_id}
Update an agent

**Parameters:**
- `agent_id` (path): Agent ID

**Request Body:**
```json
{
  "id": "agent_1",
  "name": "Updated Agent",
  "description": "Updated description",
  "category": "Code Generation",
  "framework": "OpenAI",
  "language": "Python",
  "code": "# Updated code"
}
```

**Response:**
```json
{
  "message": "Agent updated",
  "agent": { /* updated agent object */ }
}
```

#### DELETE /agents/{agent_id}
Delete an agent

**Parameters:**
- `agent_id` (path): Agent ID

**Response:**
```json
{
  "message": "Agent deleted"
}
```

#### POST /agents/execute
Execute an agent

**Request Body:**
```json
{
  "agent_id": "agent_1",
  "input_data": {
    "key": "value",
    "param": "test"
  }
}
```

**Response:**
```json
{
  "message": "Agent executed",
  "agent_id": "agent_1",
  "status": "success",
  "output": "Execution result"
}
```

### Project Endpoints

#### GET /projects
List all projects

**Response:**
```json
{
  "projects": [
    {
      "id": "project_1",
      "name": "My Project",
      "description": "Project description",
      "agents": ["agent_1", "agent_2"]
    }
  ]
}
```

#### POST /projects
Create a new project

**Request Body:**
```json
{
  "id": "project_1",
  "name": "My Project",
  "description": "Project description",
  "agents": []
}
```

**Response:**
```json
{
  "message": "Project created",
  "project": { /* project object */ }
}
```

#### GET /projects/{project_id}
Get project details

**Parameters:**
- `project_id` (path): Project ID

**Response:**
```json
{
  "project": {
    "id": "project_1",
    "name": "My Project",
    "description": "Project description",
    "agents": ["agent_1", "agent_2"]
  }
}
```

### Metadata Endpoints

#### GET /categories
Get available agent categories

**Response:**
```json
{
  "categories": [
    "Autonomous Agents",
    "Code Generation",
    "Data Analysis",
    "Web Automation",
    "NLP & Chat",
    "Workflow Automation",
    "Research & Development",
    "Testing & QA"
  ]
}
```

#### GET /frameworks
Get supported AI frameworks

**Response:**
```json
{
  "frameworks": [
    "LangChain",
    "AutoGPT",
    "CrewAI",
    "OpenAI",
    "Anthropic Claude",
    "HuggingFace",
    "Custom"
  ]
}
```

## Data Models

### Agent Model

```typescript
{
  id: string;
  name: string;
  description: string;
  category: string;
  framework: string;
  language: string;
  code?: string;
}
```

### Project Model

```typescript
{
  id: string;
  name: string;
  description: string;
  agents: string[];
}
```

### AgentExecution Model

```typescript
{
  agent_id: string;
  input_data: {
    [key: string]: any;
  };
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Authentication

Currently, the API does not require authentication. This will be added in future versions.

## Rate Limiting

No rate limiting is currently enforced. This will be added in production deployments.

## CORS

The API allows all origins for development. Configure appropriately for production.

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Examples

### Create and Execute an Agent

```bash
# Create an agent
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test_agent",
    "name": "Test Agent",
    "description": "A test agent",
    "category": "Code Generation",
    "framework": "OpenAI",
    "language": "Python",
    "code": "print(\"Hello World\")"
  }'

# Execute the agent
curl -X POST http://localhost:8000/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "test_agent",
    "input_data": {
      "message": "test"
    }
  }'
```

### List All Agents

```bash
curl http://localhost:8000/agents
```

### Get Agent Details

```bash
curl http://localhost:8000/agents/test_agent
```

### Delete an Agent

```bash
curl -X DELETE http://localhost:8000/agents/test_agent
```
