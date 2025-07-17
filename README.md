# Summer of Q

This project is a series of tasks and experiments designed to explore and demonstrate the capabilities of Amazon Q Developer. Each subdirectory contains a different project or experiment that showcases various aspects of AI-assisted development.

## Projects

- [**leave-tracker**](./leave-tracker/README.md) - A command-line tool for tracking annual leave allowance with interactive setup and natural date formatting
- [**conways-game-of-life**](./conways-game-of-life/README.md) - A Go implementation of Conway's Game of Life cellular automaton built using Test-Driven Development
- [**devographics**](./devographics/README.md) - Notes summarizing the Devographics project, an open-source platform powering developer surveys

## About Amazon Q Developer

Amazon Q Developer is an AI-powered assistant that helps with software development tasks including:
- Code generation and modification
- Debugging and troubleshooting
- Architecture recommendations
- Best practices guidance
- Documentation generation

This repository serves as a practical exploration of these capabilities through real-world development scenarios.

## Amazon Q Rules

This project uses the `.amazonq/rules` directory to define custom rules that guide Amazon Q's behavior when working with this codebase. These rules are automatically loaded as context when using Amazon Q in this repository.

Current rules include:
- **Documentation is Important** - Ensures documentation stays up-to-date with code changes
- **No Whitespace Errors** - Prevents introducing whitespace errors in git
- **Prompt Then Commit** - Requires confirmation before committing changes

Rules are defined as markdown files in the `.amazonq/rules` directory. When Amazon Q is used within this repository, it automatically reads these rules and incorporates them into its responses and recommendations.

## Getting Started

Each project directory contains its own README with specific setup and usage instructions. Navigate to the individual project folders to explore the different experiments and implementations.