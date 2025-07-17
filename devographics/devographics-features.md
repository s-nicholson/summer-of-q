# Devographics Application Features

## Overview

Devographics is a comprehensive survey platform that powers developer surveys like State of JS, State of CSS, and other technology-focused surveys. The platform consists of multiple applications working together to create, distribute, and visualize survey data.

## Authentication System

The application uses a passwordless authentication system:

1. **Magic Link Authentication**:
   - Users authenticate via email-based magic links
   - Implementation is in `/surveyform/src/lib/account/magicLogin`
   - Uses SMTP for email delivery (configurable via environment variables)
   - Emails are sent through services like AWS SES (configured via SMTP settings)

2. **Anonymous Login**:
   - Allows users to take surveys without creating an account
   - Implementation in `/surveyform/src/lib/account/anonymousLogin`
   - Useful for increasing survey participation rates

3. **Session Management**:
   - Session handling in `/surveyform/src/lib/account/session`
   - Uses encryption keys for security (configured via ENCRYPTION_KEY env variable)

## Survey Configuration

Surveys are defined using a structured approach:

1. **YAML-Based Configuration**:
   - Survey definitions are stored as YAML files in a separate repository
   - Can be loaded from GitHub or local filesystem
   - Configured via environment variables (SURVEYS_DIR or GITHUB_PATH_SURVEYS)

2. **Survey Structure**:
   - Each survey has multiple editions (e.g., State of JS 2022, State of JS 2023)
   - Editions contain sections, which contain questions
   - Questions can have various types and configurations

3. **Survey Identification**:
   - Surveys are identified by a combination of surveyId and editionId
   - URL slugs are mapped to these IDs (e.g., "state-of-js" and "2023" map to specific IDs)

4. **Internationalization**:
   - Survey questions and UI elements are internationalized
   - Locale files are stored in separate repositories
   - Can be loaded from GitHub or local filesystem
   - Configured via environment variables (LOCALES_DIR or GITHUB_PATH_LOCALES)

## Data Collection and Storage

1. **Database Structure**:
   - MongoDB for primary data storage
   - Two separate databases:
     - Private database (MONGO_PRIVATE_DB): Stores user data and raw survey responses
     - Public database: Stores processed, anonymized survey results

2. **Data Processing**:
   - Raw survey responses are normalized and processed
   - Personal information is separated from survey data
   - Data is aggregated for visualization in the results application

3. **Caching**:
   - Redis is used for caching API responses
   - Improves performance for frequently accessed data
   - Can be disabled for development (DISABLE_CACHE env variable)

## Survey Taking Experience

1. **Multi-page Survey Flow**:
   - Surveys are divided into sections for better user experience
   - Progress is saved as users move through the survey

2. **Response Saving**:
   - Responses are saved incrementally as users progress
   - Users can return to complete surveys later

3. **Custom Components**:
   - Specialized UI components for different question types
   - Support for various input methods (multiple choice, text, rating, etc.)

## Results Visualization

1. **Data Processing Pipeline**:
   - Raw survey data is processed and normalized
   - Results are aggregated and prepared for visualization

2. **Visualization Components**:
   - Custom chart components for different data types
   - Interactive visualizations for exploring survey results

3. **Public Access**:
   - Results are published on dedicated websites (e.g., stateofjs.com)
   - Data is presented in an accessible, interactive format

## Administration

1. **Survey Management**:
   - Admin interface for managing surveys (surveyadmin application)
   - Tools for monitoring survey completion rates

2. **Data Processing**:
   - Tools for normalizing and processing survey data
   - Capabilities for exporting and analyzing results

## Security Features

1. **Data Protection**:
   - Encryption of sensitive data (using ENCRYPTION_KEY)
   - Separation of personal data from survey responses

2. **API Security**:
   - Secret keys for API access (SECRET_KEY)
   - Token-based authentication (TOKEN_SECRET)

3. **Email Security**:
   - Secure email delivery for authentication links
   - SMTP with TLS/SSL support

## Development and Extensibility

1. **Monorepo Structure**:
   - Organized as a monorepo with multiple applications
   - Shared code and components between applications

2. **Configuration Options**:
   - Extensive environment variable configuration
   - Support for both local and remote data sources

3. **Testing Infrastructure**:
   - Jest for unit testing
   - Cypress and Playwright for end-to-end testing

## Integration with External Services

1. **Email Services**:
   - Integration with email providers via SMTP
   - Support for services like EmailOctopus for newsletters

2. **Analytics**:
   - Integration with Plausible for privacy-focused analytics

3. **GitHub Integration**:
   - Loading survey configurations and locales from GitHub repositories
   - Version control for survey definitions
