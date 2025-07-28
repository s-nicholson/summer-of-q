# Terminal Visualization

A simple Python application for creating line graphs from data files in the terminal.

## Features

- Generate ASCII line charts from CSV/text data files
- Support for date columns and numeric values
- Clean terminal output suitable for quick data analysis

## Installation

```bash
cd terminal-viz
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the visualization tool
python viz.py /tmp/ris-volumes.txt
```

Expected data formats:

**CSV format:**
```
date,count
2024-01-01,150
2024-01-02,200
```

**SQL table output:**
```
          h          | count 
---------------------+-------
 2025-07-01 00:00:00 |   517
 2025-07-01 01:00:00 |  1511
```

## Dependencies

- termgraph: Simple terminal graphing library
- pandas: Data manipulation (optional, for complex parsing)
- pytest: Testing framework

## Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest test_viz.py::test_parse_sql_table_format
```
