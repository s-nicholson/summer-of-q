# Devographics Application Interactions

This document explains how the Devographics applications work together and how data flows through the system.

## System Architecture

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

## Key Data Flows

### 1. Survey Definition Flow

```
Survey YAML Files → API → Surveyform
```

- Survey definitions are created as YAML files (local or GitHub-hosted)
- API loads and parses these definitions
- Surveyform requests definitions from API to render questions

### 2. User Response Flow

```
User → Surveyform → API → Private Database
```

- Users authenticate via magic links or anonymous sessions
- Users complete survey questions with incremental saving
- API validates and stores responses in private MongoDB database

### 3. Data Processing Flow

```
Private Database → API (Processing) → Public Database
```

- Raw responses are normalized and anonymized
- Data is aggregated for statistical analysis
- Processed data is stored in public database without personal information

### 4. Results Visualization Flow

```
Public Database → API → Results Application → End User
```

- Results app requests processed data from API
- Data is transformed into visualizations (charts, graphs)
- Users interact with visualizations on public websites

## Communication Methods

- All frontend applications use GraphQL to communicate with API
- Shared code in `/shared` directory provides common utilities
- Redis caching improves performance for frequent queries

## Caching Strategy

- **API Level**: Redis caches common API responses
- **Client Level**: SWR for frontend caching and optimistic updates
- **Static Generation**: Pre-rendered pages for results sites

## Error Handling

- Standardized error format across API endpoints
- Retry logic in frontend applications
- Fallback content when data is unavailable

## Development Considerations

When working on the platform, remember:

- API changes may affect multiple frontend applications
- Shared code updates impact all dependent applications
- Database schema changes may require migrations
- Test changes across the entire application ecosystem
