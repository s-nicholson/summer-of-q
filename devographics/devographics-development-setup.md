# Devographics Development Setup

This guide covers setting up a local development environment for the Devographics project.

## Prerequisites

- **Node.js** (v16+)
- **Docker** (for MongoDB and Redis)
- **Git**
- **pnpm** (`npm install -g pnpm`)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Devographics/Monorepo.git
   cd Monorepo
   ```

2. **Set up Docker services**
   Create `docker-compose.yml` in the root directory:
   ```yaml
   version: '3'
   services:
     mongodb:
       image: mongo:5.0.19
       ports:
         - "27017:27017"
       volumes:
         - ./.mongo:/data/db
     
     redis:
       image: redis:alpine
       ports:
         - "6379:6379"
     
     redis-http:
       image: hiett/serverless-redis-http:latest
       environment:
         - REDIS_URL=redis://redis:6379
       ports:
         - "8474:8080"
       depends_on:
         - redis
   ```

3. **Start Docker services**
   ```bash
   docker-compose up -d
   ```

4. **Create environment files**
   See the Environment Configuration section below

5. **Start applications**
   ```bash
   # API
   cd api && pnpm install && pnpm dev
   
   # In a new terminal - Surveyform
   cd surveyform && pnpm install && pnpm dev
   
   # In a new terminal - Results
   cd results && pnpm install && pnpm dev
   ```

## Environment Configuration

Create these environment files with the following essential variables:

### API (.env in /api)
```
MONGO_URI=mongodb://localhost:27017
MONGO_PRIVATE_DB=devographics_private
MONGO_PUBLIC_DB=devographics_public
REDIS_URL=http://localhost:8474
SECRET_KEY=your_secret_key
TOKEN_SECRET=your_token_secret
ENCRYPTION_KEY=your_encryption_key
SURVEYS_DIR=../surveys
LOCALES_DIR=../locales
```

### Surveyform (.env.local in /surveyform)
```
NEXT_PUBLIC_API_URL=http://localhost:4000
NEXT_PUBLIC_ENCRYPTION_KEY=your_encryption_key
NEXT_PUBLIC_SURVEYS_DIR=../surveys
NEXT_PUBLIC_LOCALES_DIR=../locales
```

### Results (.env.development in /results)
```
GATSBY_API_URL=http://localhost:4000
GATSBY_SURVEYS_DIR=../surveys
GATSBY_LOCALES_DIR=../locales
```

## Local Survey Data

Create basic survey and locale files for development:

```bash
# Create survey directory
mkdir -p surveys/state_of_js/2023

# Create locale directory
mkdir -p locales/en-US
```

Create a basic survey definition:
```yaml
# surveys/state_of_js/2023/survey.yml
id: state_of_js
name: State of JavaScript
year: 2023
status: preview
```

Create a basic locale file:
```json
// locales/en-US/common.json
{
  "general": {
    "survey_name": "State of JavaScript 2023"
  }
}
```

## Application URLs

- API: http://localhost:4000
- Surveyform: http://localhost:3000
- Results: http://localhost:8000

## Common Tasks

### Running Tests
```bash
# Unit tests
cd surveyform && pnpm test

# End-to-end tests
cd surveyform && pnpm cypress:open
```

### Building for Production
```bash
cd api && pnpm build
cd surveyform && pnpm build
cd results && pnpm build
```

## Troubleshooting

### MongoDB Issues
- Check Docker status: `docker ps`
- Verify MongoDB logs: `docker logs monorepo_mongodb_1`
- Confirm connection string in environment variables

### Redis Issues
- Check Redis status: `docker ps`
- Test Redis HTTP proxy: `curl http://localhost:8474/ping`
- Check Redis logs: `docker logs monorepo_redis_1`

### API Connection Issues
- Verify API is running: `curl http://localhost:4000`
- Check API environment variables
- Confirm frontend applications use correct API URL
