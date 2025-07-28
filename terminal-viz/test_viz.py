#!/usr/bin/env python3
"""
Tests for the visualization tool using pytest.
"""

import tempfile
from pathlib import Path
import pytest
from viz import parse_data_file


def test_parse_csv_with_header():
    """Test parsing CSV file with header."""
    test_data = "date,count\n2024-01-01,100\n2024-01-02,200\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write(test_data)
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert data == [100.0, 200.0]
        assert labels == ['2024-01-01', '2024-01-02']
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_parse_sql_table_format():
    """Test parsing SQL table output format."""
    test_data = """          h          | count 
---------------------+-------
 2025-07-01 00:00:00 |   517
 2025-07-01 01:00:00 |  1511
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write(test_data)
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert data == [517.0, 1511.0]
        assert len(labels) == 2
        assert '00:00' in labels[0]
        assert '01:00' in labels[1]
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_parse_csv_without_header():
    """Test parsing CSV file without header."""
    test_data = "2024-01-01,150\n2024-01-02,250\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write(test_data)
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert data == [150.0, 250.0]
        assert labels == ['2024-01-01', '2024-01-02']
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_parse_invalid_data():
    """Test handling of invalid numeric data."""
    test_data = "date,count\n2024-01-01,invalid\n2024-01-02,200\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write(test_data)
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert data == [200.0]
        assert labels == ['2024-01-02']
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_empty_file():
    """Test handling of empty file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("")
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert data == []
        assert labels == []
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@pytest.fixture
def sample_sql_data():
    """Fixture providing sample SQL table data."""
    return """          timestamp      | value 
---------------------+-------
 2025-07-01 08:00:00 |   100
 2025-07-01 09:00:00 |   150
 2025-07-01 10:00:00 |   200
"""


def test_sql_parsing_with_fixture(sample_sql_data):
    """Test SQL parsing using pytest fixture."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write(sample_sql_data)
        tmp_path = tmp.name
    
    try:
        data, labels = parse_data_file(tmp_path)
        assert len(data) == 3
        assert data == [100.0, 150.0, 200.0]
        assert all('08:00' in labels[0] or '09:00' in labels[1] or '10:00' in labels[2] for _ in range(1))
    finally:
        Path(tmp_path).unlink(missing_ok=True)
