# Devographics Project Structure

## Monorepo Overview

The Devographics project is organized as a monorepo containing multiple applications that work together to create, distribute, and visualize developer survey data.

## Core Applications

| Application | Directory | Purpose | Technology |
|-------------|-----------|---------|------------|
| API | `/api` | GraphQL backend serving all applications | Node.js, Apollo Server |
| Surveyform | `/surveyform` | Collects survey responses | Next.js |
| Results | `/results` | Visualizes survey results | Gatsby |
| Surveyadmin | `/surveyadmin` | Admin interface for survey management | React |

## Additional Applications

| Application | Directory | Purpose |
|-------------|-----------|---------|
| Results-Astro | `/results-astro` | Alternative results app with improved performance |
| Results-Remix | `/results-remix` | Alternative results app with server-side rendering |
| GraphiQL | `/graphiql` | GraphQL IDE for API testing |
| Charts | `/charts` | Shared visualization components |
| Capture | `/capture` | Screenshot generation for social media |
| Homepage | `/homepage` | Main Devographics project site |
| Dot_com | `/dot_com` | Devographics organization website |
| Jobs | `/jobs` | Background processing tasks |

## Shared Code

The `/shared` directory contains common code used across applications:

- Components, types, and utilities
- Database and caching utilities
- Internationalization helpers
- Authentication and permission handling
- Data fetching and API clients

## Development Environment

### Requirements

- Node.js
- Docker (for MongoDB and Redis)
- Environment variables for configuration

### Key Environment Variables

Common configuration variables include:

- Database: `MONGO_PRIVATE_DB`, `MONGO_PUBLIC_DB`, `REDIS_URL`
- Authentication: `SECRET_KEY`, `TOKEN_SECRET`, `ENCRYPTION_KEY`
- Survey data: `SURVEYS_DIR` or `GITHUB_PATH_SURVEYS`
- Localization: `LOCALES_DIR` or `GITHUB_PATH_LOCALES`

### Development Workflow

1. Clone repository
2. Configure environment variables
3. Start required services with Docker
4. Install dependencies
5. Run applications in development mode

## Testing

- Unit tests with Jest
- End-to-end tests with Cypress
- Integration tests for API endpoints
- Visual testing for UI components
