# Devographics Development Environment Setup

This guide provides instructions for setting up a local development environment for the Devographics project. It covers the necessary prerequisites, configuration steps, and common development workflows.

## Prerequisites

Before starting development on the Devographics project, ensure you have the following installed:

1. **Node.js** - Version 16.x or later recommended
2. **Docker** - For running MongoDB and Redis locally
3. **Git** - For version control
4. **pnpm** - Package manager used by the project (can be installed via `npm install -g pnpm`)

## Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Devographics/Monorepo.git
   cd Monorepo
   ```

2. **Create environment files**:
   Each application requires its own environment configuration. Create the following `.env` files:

   **API (.env file in /api directory)**:
   ```
   # MongoDB Configuration
   MONGO_URI=mongodb://localhost:27017
   MONGO_PRIVATE_DB=devographics_private
   MONGO_PUBLIC_DB=devographics_public
   
   # Redis Configuration
   REDIS_URL=http://localhost:8474
   
   # Authentication
   SECRET_KEY=your_secret_key
   TOKEN_SECRET=your_token_secret
   ENCRYPTION_KEY=your_encryption_key
   
   # Survey Configuration
   # Use either local directory or GitHub path
   SURVEYS_DIR=../surveys
   # GITHUB_PATH_SURVEYS=Devographics/surveys
   
   # Localization
   # Use either local directory or GitHub path
   LOCALES_DIR=../locales
   # GITHUB_PATH_LOCALES=Devographics/locales
   
   # Email Configuration
   SMTP_HOST=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=your_smtp_user
   SMTP_PASS=your_smtp_password
   EMAIL_FROM=surveys@example.com
   ```

   **Surveyform (.env.local file in /surveyform directory)**:
   ```
   # API URL
   NEXT_PUBLIC_API_URL=http://localhost:4000
   
   # Authentication
   NEXT_PUBLIC_ENCRYPTION_KEY=your_encryption_key
   
   # Survey Configuration
   NEXT_PUBLIC_SURVEYS_DIR=../surveys
   # NEXT_PUBLIC_GITHUB_PATH_SURVEYS=Devographics/surveys
   
   # Localization
   NEXT_PUBLIC_LOCALES_DIR=../locales
   # NEXT_PUBLIC_GITHUB_PATH_LOCALES=Devographics/locales
   ```

   **Results (.env.development file in /results directory)**:
   ```
   # API URL
   GATSBY_API_URL=http://localhost:4000
   
   # Survey Configuration
   GATSBY_SURVEYS_DIR=../surveys
   # GATSBY_GITHUB_PATH_SURVEYS=Devographics/surveys
   
   # Localization
   GATSBY_LOCALES_DIR=../locales
   # GATSBY_GITHUB_PATH_LOCALES=Devographics/locales
   ```

3. **Set up Docker services**:
   Create a `docker-compose.yml` file in the root directory:
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

4. **Start the Docker services**:
   ```bash
   docker-compose up -d
   ```

## Setting Up Individual Applications

### API

1. Navigate to the API directory:
   ```bash
   cd api
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

The API will be available at http://localhost:4000.

### Surveyform

1. Navigate to the Surveyform directory:
   ```bash
   cd surveyform
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

The Surveyform application will be available at http://localhost:3000.

### Results

1. Navigate to the Results directory:
   ```bash
   cd results
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

The Results application will be available at http://localhost:8000.

## Working with Survey Data

### Local Survey Definitions

For local development, you can create a `surveys` directory at the root level:

```bash
mkdir -p surveys/state_of_js/2023
```

Create a basic survey definition file:
```yaml
# surveys/state_of_js/2023/survey.yml
id: state_of_js
name: State of JavaScript
year: 2023
status: preview
```

### Local Locale Files

For localization, create a `locales` directory at the root level:

```bash
mkdir -p locales/en-US
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

## Common Development Tasks

### Running Tests

For Surveyform:
```bash
cd surveyform
pnpm test
```

For end-to-end tests:
```bash
cd surveyform
pnpm cypress:open
```

### Building for Production

For API:
```bash
cd api
pnpm build
```

For Surveyform:
```bash
cd surveyform
pnpm build
```

For Results:
```bash
cd results
pnpm build
```

## Troubleshooting

### MongoDB Connection Issues

If you encounter MongoDB connection issues:
1. Ensure Docker containers are running: `docker ps`
2. Check MongoDB logs: `docker logs monorepo_mongodb_1`
3. Verify connection string in environment variables

### Redis Connection Issues

If Redis is not connecting:
1. Check if Redis containers are running: `docker ps`
2. Verify Redis HTTP proxy is working: `curl http://localhost:8474/ping`
3. Check Redis logs: `docker logs monorepo_redis_1`

### API Connection Issues

If frontend applications cannot connect to the API:
1. Ensure API is running: `curl http://localhost:4000`
2. Check API environment variables
3. Verify frontend applications are using the correct API URL

## Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Next.js Documentation](https://nextjs.org/docs)
- [Gatsby Documentation](https://www.gatsbyjs.com/docs/)
