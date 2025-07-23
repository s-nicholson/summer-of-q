# Devographics Features

## Overview

Devographics powers developer surveys like State of JS and State of CSS through multiple integrated applications.

## Key Features

### Authentication

- **Magic Link Login**: Email-based passwordless authentication
- **Anonymous Login**: Take surveys without creating an account
- **Secure Sessions**: Encrypted session management

### Survey System

- **YAML Configuration**: Surveys defined in YAML files (local or GitHub-hosted)
- **Flexible Structure**: Surveys organized by editions, sections, and questions
- **Internationalization**: Multi-language support for global reach

### Data Management

- **Dual Database System**:
  - Private database: User data and raw responses
  - Public database: Processed, anonymized results
- **Redis Caching**: Performance optimization for API responses
- **Incremental Saving**: Survey progress saved as users advance

### User Experience

- **Multi-page Flow**: Surveys divided into manageable sections
- **Custom Components**: Specialized UI for different question types
- **Progress Tracking**: Users can return to complete surveys later

### Results Visualization

- **Data Processing**: Raw data normalized and prepared for visualization
- **Interactive Charts**: Custom visualization components
- **Public Access**: Results published on dedicated websites

### Administration

- **Survey Management**: Tools for creating and monitoring surveys
- **Data Processing**: Normalization and analysis capabilities
- **Export Options**: Data export for further analysis

### Security

- **Data Protection**: Encryption of sensitive information
- **API Security**: Secret keys and token authentication
- **Separation of Concerns**: Personal data isolated from survey responses

### Development

- **Monorepo Structure**: Organized codebase with shared components
- **Flexible Configuration**: Extensive environment variable options
- **Testing Infrastructure**: Unit and end-to-end testing support

### External Integrations

- **Email Services**: SMTP integration for authentication
- **Analytics**: Privacy-focused analytics with Plausible
- **GitHub Integration**: Version-controlled survey definitions
