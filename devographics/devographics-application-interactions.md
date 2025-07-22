# Devographics Application Interactions and Data Flow

This document describes how the various applications in the Devographics monorepo interact with each other and how data flows through the system. Understanding these interactions is crucial for developers working on the project.

## System Architecture Overview

The Devographics platform consists of several interconnected applications that work together to create a complete survey ecosystem:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Surveyform    │◄────┤      API        │◄────┤  Results App    │
│  (Next.js App)  │     │  (GraphQL API)  │     │ (Gatsby/Astro/  │
│                 │     │                 │     │    Remix)       │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Private DB     │     │   Public DB     │     │  Surveyadmin    │
│  (MongoDB)      │     │   (MongoDB)     │     │  (Admin Tools)  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Data Flow

### 1. Survey Definition Flow

```
Survey YAML Files → API → Surveyform
```

1. **Survey Definition Creation**:
   - Survey definitions are created as YAML files
   - These files define the structure, questions, and options for each survey
   - They can be stored locally or in a GitHub repository

2. **API Loading**:
   - The API loads these survey definitions on startup
   - It parses the YAML files and creates in-memory representations
   - The definitions are cached for performance

3. **Surveyform Access**:
   - The Surveyform application requests survey definitions from the API
   - It uses these definitions to render the appropriate questions
   - The survey structure determines the user experience

### 2. User Response Flow

```
User → Surveyform → API → Private Database
```

1. **User Authentication**:
   - Users access the Surveyform application
   - They authenticate via magic links or anonymous sessions
   - Session tokens are stored in browser storage

2. **Survey Completion**:
   - Users answer survey questions
   - Responses are saved incrementally as they progress
   - The Surveyform app sends responses to the API

3. **Data Storage**:
   - The API validates incoming responses
   - It stores responses in the private MongoDB database
   - Personal information is encrypted and stored separately

### 3. Data Processing Flow

```
Private Database → API (Processing) → Public Database
```

1. **Data Normalization**:
   - Raw survey responses are processed and normalized
   - Free-form text responses are cleaned and categorized
   - Data is anonymized by removing personal identifiers

2. **Aggregation**:
   - Responses are aggregated to generate statistics
   - Calculations are performed for various metrics
   - Results are prepared for visualization

3. **Public Storage**:
   - Processed, anonymized data is stored in the public database
   - This data is accessible for visualization and analysis
   - No personally identifiable information is included

### 4. Results Visualization Flow

```
Public Database → API → Results Application → End User
```

1. **Data Retrieval**:
   - The Results application queries the API for processed data
   - It requests specific metrics and visualizations
   - The API retrieves data from the public database

2. **Visualization Generation**:
   - The Results app processes the data for visualization
   - It generates charts, graphs, and interactive elements
   - Different visualization components handle different data types

3. **User Interaction**:
   - End users interact with the visualizations
   - They can filter, sort, and explore the data
   - The application responds dynamically to user input

## Key API Endpoints

The API serves as the central hub for all data interactions. Key endpoints include:

### Survey Management

- `GET /surveys`: List all available surveys
- `GET /surveys/:surveyId`: Get details for a specific survey
- `GET /surveys/:surveyId/editions/:editionId`: Get a specific survey edition

### Response Management

- `POST /responses`: Submit a new survey response
- `PATCH /responses/:responseId`: Update an existing response
- `GET /responses/user/:userId`: Get responses for a specific user

### Results and Visualization

- `GET /results/:surveyId/:editionId`: Get processed results for a survey edition
- `GET /results/:surveyId/:editionId/:questionId`: Get results for a specific question

### Authentication

- `POST /auth/login`: Request a magic link login
- `POST /auth/verify`: Verify a magic link token
- `POST /auth/anonymous`: Create an anonymous session

## Inter-Application Communication

### API to Frontend Applications

All frontend applications (Surveyform, Results, Surveyadmin) communicate with the API using GraphQL. The API provides a unified interface for:

1. **Data Queries**: Retrieving survey definitions, responses, and results
2. **Mutations**: Submitting and updating survey responses
3. **Subscriptions**: Real-time updates (where applicable)

### Shared Code

The `/shared` directory contains code used across multiple applications:

1. **API Client**: Shared code for communicating with the API
2. **Types**: Common TypeScript interfaces and types
3. **Utilities**: Helper functions used across applications
4. **Components**: Reusable UI components

## Caching Strategy

To improve performance, the system implements several caching mechanisms:

1. **Redis Cache**:
   - API responses are cached in Redis
   - Common queries benefit from faster response times
   - Cache invalidation occurs when data changes

2. **Client-Side Caching**:
   - Frontend applications use SWR for client-side caching
   - Reduces unnecessary API calls
   - Provides optimistic UI updates

3. **Static Generation**:
   - Results sites use static generation where possible
   - Pre-rendered pages improve load times
   - Dynamic data is fetched client-side as needed

## Error Handling and Resilience

The system includes several mechanisms for handling errors and ensuring resilience:

1. **API Error Responses**:
   - Standardized error format across all endpoints
   - Detailed error messages for debugging
   - Error codes for programmatic handling

2. **Retry Logic**:
   - Frontend applications implement retry logic for failed requests
   - Exponential backoff prevents overwhelming the API
   - Users are notified of persistent issues

3. **Fallback Content**:
   - Applications provide fallback content when data is unavailable
   - Graceful degradation ensures usability even with partial data

## Development Considerations

When developing for the Devographics platform, consider these interaction points:

1. **API Changes**:
   - Changes to the API may affect multiple frontend applications
   - GraphQL schema changes should be carefully coordinated
   - Consider backward compatibility for existing clients

2. **Shared Code Updates**:
   - Updates to shared code affect all applications
   - Test changes across all dependent applications
   - Consider versioning for breaking changes

3. **Database Schema Evolution**:
   - Changes to database schemas may require migration scripts
   - Consider data integrity across the private and public databases
   - Test with representative data volumes

## Monitoring and Observability

The system includes several monitoring points:

1. **API Metrics**:
   - Request counts and response times
   - Error rates and types
   - Resource utilization

2. **User Journey Tracking**:
   - Survey completion rates
   - Drop-off points
   - Time spent on questions

3. **System Health**:
   - Database connection status
   - Cache hit/miss rates
   - External service dependencies
