# Devographics Project Summary

## Project Overview

Devographics is a monorepo project that runs surveys like State of JS and State of CSS. It consists of multiple applications that work together to collect, process, and display survey data.

## Deployment Strategy & Hosting

The project uses a distributed hosting approach across multiple platforms:

1. **API**: 
   - Hosted on Render.com
   - Serves as the backend for all applications

2. **GraphiQL**: 
   - Hosted on Netlify
   - Provides a GraphQL IDE for testing API queries
   - Available at https://api.devographics.com

3. **Surveyform**: 
   - Hosted on Vercel
   - Next.js TypeScript application for collecting survey responses
   - Available at https://survey.devographics.com

4. **Results**: 
   - Hosted on Netlify
   - Gatsby TypeScript application for displaying survey results
   - Multiple domains for different surveys (e.g., https://2022.stateofjs.com)
   - Also configured for deployment on Render.com

5. **Surveyadmin**:
   - Currently only runs locally
   - Used for survey management and data processing

6. **Static Assets**:
   - Hosted on Netlify
   - Available at https://assets.devographics.com

## Data Persistence

The project uses two main databases for data persistence:

1. **MongoDB**:
   - Hosted on MongoDB Atlas for production
   - Stores both raw and normalized survey data
   - Uses two separate databases:
     - `MONGO_PRIVATE_DB`: Stores private respondent data
     - `MONGO_PUBLIC_DB`: Stores public, processed data
   - For local development, MongoDB runs in Docker (version 5.0.19)
   - Local data is stored in a `.mongo` folder in the monorepo

2. **Redis**:
   - Hosted on Upstash for production
   - Used for caching API query results
   - For local development, Redis runs in Docker with a serverless-redis-http proxy to simulate Upstash's HTTP-based interface

## Local Development Setup

For local development, the project uses:
- Docker Compose to run MongoDB and Redis locally
- A Justfile for common development commands
- Environment variables stored in `.env` files for configuration
- Optional local directories for surveys, locales, and entities data

The project is designed to be flexible, allowing developers to use either local files or remote APIs for development, with appropriate environment variable configuration.
