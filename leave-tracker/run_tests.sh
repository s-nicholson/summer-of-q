#!/bin/bash
# Run pytest tests for leave tracker

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest is not installed. Installing..."
    pip install pytest
fi

# Run tests with verbose output
pytest -v test_leave_tracker.py
