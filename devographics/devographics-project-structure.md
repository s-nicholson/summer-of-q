# Devographics Project Structure

## Monorepo Overview

The Devographics project is organized as a monorepo containing multiple interconnected applications that work together to create, distribute, and visualize developer survey data. This document provides an overview of the repository structure and the purpose of each application.

## Applications

### Core Applications

1. **API** (`/api`)
   - GraphQL API backend that serves all applications
   - Handles data processing, authentication, and database operations
   - Built with Node.js and Apollo Server

2. **Surveyform** (`/surveyform`)
   - Next.js application for collecting survey responses
   - Handles user authentication and survey submission
   - Features progressive form saving and multi-language support
   - Includes Cypress tests for end-to-end testing

3. **Results** (`/results`)
   - Gatsby application for visualizing survey results
   - Displays interactive charts and data visualizations
   - Powers sites like stateofjs.com and stateofcss.com

4. **Surveyadmin** (`/surveyadmin`)
   - Admin interface for managing surveys
   - Tools for monitoring survey completion and data processing
   - Primarily used by survey administrators

### Additional Applications

5. **Results-Astro** (`/results-astro`)
   - Newer implementation of the results application using Astro framework
   - Provides improved performance and build times
   - Currently in development/transition phase

6. **Results-Remix** (`/results-remix`)
   - Alternative implementation of the results application using Remix framework
   - Offers server-side rendering capabilities
   - Currently in development/evaluation phase

7. **GraphiQL** (`/graphiql`)
   - GraphQL IDE for testing API queries
   - Provides documentation and exploration of the GraphQL schema

8. **Charts** (`/charts`)
   - Shared chart components used across result applications
   - Visualization libraries and custom chart implementations

9. **Capture** (`/capture`)
   - Tool for generating screenshots and images of survey results
   - Used for social media sharing and promotional materials

10. **Homepage** (`/homepage`)
    - Main Devographics project homepage
    - Built with Astro framework
    - Entry point for users to discover surveys

11. **Dot_com** (`/dot_com`)
    - Website for the Devographics organization
    - Contains information about the project and team

12. **Jobs** (`/jobs`)
    - Background processing tasks
    - Handles data processing, email sending, and other asynchronous operations

## Shared Code

The `/shared` directory contains common code used across multiple applications:

- `/shared/components` - Reusable React components
- `/shared/types` - TypeScript type definitions
- `/shared/i18n` - Internationalization utilities
- `/shared/redis` - Redis client and caching utilities
- `/shared/mongo` - MongoDB connection and utilities
- `/shared/constants` - Shared constants and configuration
- `/shared/helpers` - Utility functions
- `/shared/icons` - Shared icon components
- `/shared/templates` - Email and document templates
- `/shared/permissions` - User permission handling
- `/shared/encrypt-email` - Email encryption utilities
- `/shared/fetch` - Data fetching utilities
- `/shared/swr-graphql` - SWR hooks for GraphQL
- `/shared/react-i18n` - React internationalization components
- `/shared/debug` - Debugging utilities

## Development Environment

### Local Setup Requirements

1. **Node.js** - Required for all applications
2. **Docker** - For running MongoDB and Redis locally
3. **MongoDB** - Version 5.0.19 recommended (via Docker)
4. **Redis** - With serverless-redis-http proxy to simulate Upstash

### Environment Variables

Each application requires specific environment variables for configuration. Common variables include:

- Database connections: `MONGO_PRIVATE_DB`, `MONGO_PUBLIC_DB`
- Redis configuration: `REDIS_URL`
- Authentication: `SECRET_KEY`, `TOKEN_SECRET`, `ENCRYPTION_KEY`
- Email: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`
- Survey configuration: `SURVEYS_DIR` or `GITHUB_PATH_SURVEYS`
- Localization: `LOCALES_DIR` or `GITHUB_PATH_LOCALES`

### Development Workflow

1. Clone the repository
2. Set up environment variables for the applications you want to work on
3. Start the required services (MongoDB, Redis) using Docker
4. Install dependencies for the specific application(s)
5. Run the application in development mode

## Application Interactions

The Devographics system works through these key interactions:

1. **Survey Creation**:
   - Survey definitions are created as YAML files
   - These can be stored locally or in a GitHub repository
   - The API loads these definitions and makes them available

2. **Survey Taking**:
   - Users access the Surveyform application
   - Authentication happens via magic links or anonymous sessions
   - Responses are saved incrementally to MongoDB

3. **Data Processing**:
   - Raw responses are processed and normalized
   - Personal information is separated from survey data
   - Aggregated results are stored in the public database

4. **Results Visualization**:
   - The Results application (or its Astro/Remix variants) fetches processed data
   - Data is displayed through interactive visualizations
   - Results are published on survey-specific domains

## Testing Strategy

The project uses multiple testing approaches:

- **Unit Tests**: Jest for testing individual components and functions
- **End-to-End Tests**: Cypress for testing the survey-taking experience
- **Integration Tests**: Testing API endpoints and data flows
- **Visual Testing**: For ensuring consistent UI across applications

## Architecture Considerations

The Devographics platform is designed with these architectural principles:

1. **Separation of Concerns**:
   - Each application has a specific purpose
   - Shared code is extracted to the `/shared` directory

2. **Data Privacy**:
   - Personal data is stored separately from survey responses
   - Data is anonymized for public consumption

3. **Scalability**:
   - Distributed hosting across multiple platforms
   - Caching for improved performance

4. **Flexibility**:
   - Support for multiple frontend frameworks (Gatsby, Next.js, Astro, Remix)
   - Configurable data sources (local or remote)
