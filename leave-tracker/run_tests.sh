#!/bin/bash
# Run pytest tests for leave tracker using a virtual environment

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run tests with verbose output
pytest -v test_leave_tracker.py

# Deactivate virtual environment
deactivate
