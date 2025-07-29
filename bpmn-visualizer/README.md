# BPMN Visualizer

A Python tool for parsing and visualizing BPMN 2.0 diagrams with support for Activiti framework metadata.

## Features

- Parse BPMN 2.0 XML files
- Display process diagrams with proper BPMN notation
- Show Activiti-specific metadata:
  - Service task class implementations
  - Sequence flow conditions
  - Task assignments and properties
  - Process variables and expressions

## Requirements

- Python 3.8+
- Required packages (install via `pip install -r requirements.txt`):
  - `lxml` - XML parsing
  - `graphviz` - Diagram generation
  - `matplotlib` - Additional visualization support

## Setup

1. Run the setup script to create virtual environment and install dependencies:
   ```bash
   ./setup.sh
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Usage

```bash
# Basic usage
python bpmn_visualizer.py sample_process.bpmn

# Or use the CLI wrapper
./bpmn sample_process.bpmn

# Output to specific file
./bpmn sample_process.bpmn --output my_diagram

# Show detailed Activiti metadata
./bpmn sample_process.bpmn --show-metadata

# Different output formats
./bpmn sample_process.bpmn --format svg
./bpmn sample_process.bpmn --format pdf
```

## Testing

Run the test suite:
```bash
python test_parser.py
```

## BPMN Elements Supported

- Start/End Events
- Service Tasks
- User Tasks
- Gateways (Exclusive, Parallel, Inclusive)
- Sequence Flows
- Pools and Lanes

## Activiti Metadata

The tool extracts and displays:
- `activiti:class` attributes on service tasks
- `activiti:expression` on sequence flows
- `activiti:assignee` on user tasks
- `activiti:candidateGroups` and `activiti:candidateUsers`
- Process variables and form properties
