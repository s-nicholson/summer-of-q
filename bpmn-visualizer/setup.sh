#!/bin/bash

# Setup script for BPMN Visualizer

echo "Setting up BPMN Visualizer..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To test the parser, run: python test_parser.py"
echo "To visualize a BPMN file, run: python bpmn_visualizer.py sample_process.bpmn"
