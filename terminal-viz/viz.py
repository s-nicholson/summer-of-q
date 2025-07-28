#!/usr/bin/env python3
"""
Terminal data visualization tool for creating line graphs from CSV/text files.
"""

import sys
import csv
import subprocess
import tempfile
from pathlib import Path


def parse_data_file(filepath):
    """Parse data file and extract numeric values for plotting."""
    data = []
    labels = []
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Handle empty file
    if not lines:
        return data, labels
    
    # Detect format: CSV vs SQL table output
    if '|' in lines[0]:
        return parse_sql_table_format(lines)
    else:
        return parse_csv_format(lines)


def parse_sql_table_format(lines):
    """Parse SQL table output format with pipe separators."""
    data = []
    labels = []
    
    # Skip header and separator lines
    data_lines = []
    for line in lines:
        line = line.strip()
        if not line or '---' in line or line.count('|') < 1:
            continue
        # Skip header row (contains column names)
        if 'count' in line.lower() and len(data_lines) == 0:
            continue
        data_lines.append(line)
    
    for line in data_lines:
        parts = [part.strip() for part in line.split('|')]
        if len(parts) >= 2:
            try:
                # Extract date/timestamp and count
                timestamp = parts[0]
                count_value = float(parts[1])
                
                # Simplify timestamp for display (just hour)
                if ' ' in timestamp:
                    date_part, time_part = timestamp.split(' ', 1)
                    hour = time_part.split(':')[0]
                    simple_label = f"{date_part[-5:]} {hour}:00"  # MM-DD HH:00
                else:
                    simple_label = timestamp
                
                labels.append(simple_label)
                data.append(count_value)
            except (ValueError, IndexError):
                continue
    
    return data, labels


def parse_csv_format(lines):
    """Parse standard CSV format."""
    data = []
    labels = []
    
    # Check if first line is header
    first_line = lines[0].strip()
    start_idx = 0
    
    if not first_line.split(',')[1].replace('.', '').replace('-', '').isdigit():
        start_idx = 1
    
    for line in lines[start_idx:]:
        row = line.strip().split(',')
        if len(row) >= 2:
            try:
                label = row[0]
                value = float(row[1])
                labels.append(label)
                data.append(value)
            except ValueError:
                continue
    
    return data, labels


def create_line_graph(data, labels, title="Data Visualization"):
    """Create line graph using termgraph."""
    if not data:
        print("No valid data found in file")
        return
    
    # Create temporary file for termgraph
    with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as tmp:
        # Write data in termgraph format
        for i, (label, value) in enumerate(zip(labels, data)):
            # Truncate long labels
            short_label = label[:10] if len(label) > 10 else label
            tmp.write(f"{short_label},{value}\n")
        
        tmp_path = tmp.name
    
    try:
        # Run termgraph with line chart
        cmd = [
            'termgraph', 
            tmp_path,
            '--format', '{:.0f}',
            '--title', title,
            '--width', '50',
            '--color', 'blue'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error running termgraph: {result.stderr}")
            
    finally:
        # Clean up temp file
        Path(tmp_path).unlink(missing_ok=True)


def main():
    if len(sys.argv) != 2:
        print("Usage: python viz.py <data_file>")
        print("Expected format: date,count")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
    
    print(f"Visualizing data from: {filepath}")
    
    data, labels = parse_data_file(filepath)
    
    if not data:
        print("No valid numeric data found")
        sys.exit(1)
    
    print(f"Found {len(data)} data points")
    create_line_graph(data, labels, f"Data from {Path(filepath).name}")


if __name__ == "__main__":
    main()
