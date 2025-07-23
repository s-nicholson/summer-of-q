# Devographics Deployment & Persistence

## Deployment Architecture

Devographics uses a distributed hosting approach:

| Application | Platform | Purpose | URL |
|-------------|----------|---------|-----|
| API | Render.com | Backend for all applications | - |
| GraphiQL | Netlify | GraphQL IDE for API testing | https://api.devographics.com |
| Surveyform | Vercel | Next.js app for collecting responses | https://survey.devographics.com |
| Results | Netlify | Gatsby app for displaying results | https://2022.stateofjs.com (etc.) |
| Static Assets | Netlify | Shared resources | https://assets.devographics.com |

The Surveyadmin application currently runs locally only.

## Data Storage

### MongoDB

- **Hosting**: MongoDB Atlas (production), Docker (development)
- **Databases**:
  - `MONGO_PRIVATE_DB`: Stores respondent data and raw responses
  - `MONGO_PUBLIC_DB`: Stores processed, anonymized data
- **Local Development**: Data stored in `.mongo` folder

### Redis

- **Hosting**: Upstash (production), Docker with serverless-redis-http (development)
- **Purpose**: Caching API query results
- **Configuration**: HTTP-based interface in both environments

## Local Development

- **Docker Compose**: Runs MongoDB and Redis locally
- **Justfile**: Common development commands
- **Environment Variables**: Configuration via `.env` files
- **Data Sources**: Configurable to use local files or remote APIs
