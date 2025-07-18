#!/usr/bin/env python3
import pytest
import json
import tempfile
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

from leave_tracker import LeaveTracker


@pytest.fixture
def tracker():
    """Create a LeaveTracker instance with temporary files for testing"""
    # Create temporary files for config and data
    temp_config = tempfile.NamedTemporaryFile(delete=False)
    temp_data = tempfile.NamedTemporaryFile(delete=False)
    
    # Initialize paths
    config_path = Path(temp_config.name)
    data_path = Path(temp_data.name)
    
    # Close the files so we can write to them in the tests
    temp_config.close()
    temp_data.close()
    
    # Create tracker with test paths
    tracker = LeaveTracker(
        config_path=config_path,
        data_path=data_path
    )
    
    yield tracker
    
    # Clean up temporary files after test
    config_path.unlink(missing_ok=True)
    data_path.unlink(missing_ok=True)


@pytest.fixture
def sample_config():
    """Sample configuration data"""
    return {
        'years': {
            '2024': {
                'hours_per_period': 7.0,
                'hours_per_day': 7.5,
                'carryover_hours': 15.0
            }
        }
    }


@pytest.fixture
def sample_data():
    """Sample leave data"""
    return {
        '2024': [
            {
                'date': '2024-12-25',
                'hours': 7.5,
                'description': 'Christmas Day'
            },
            {
                'date': '2024-12-26',
                'hours': 7.5,
                'description': 'Boxing Day'
            }
        ]
    }


def test_get_leave_year():
    """Test get_leave_year method"""
    # Test dates in first part of leave year (Sept-Dec)
    assert LeaveTracker.get_leave_year(date(2024, 9, 1)) == 2024
    assert LeaveTracker.get_leave_year(date(2024, 12, 31)) == 2024
    
    # Test dates in second part of leave year (Jan-Aug)
    assert LeaveTracker.get_leave_year(date(2025, 1, 1)) == 2024
    assert LeaveTracker.get_leave_year(date(2025, 8, 31)) == 2024
    
    # Test boundary
    assert LeaveTracker.get_leave_year(date(2025, 9, 1)) == 2025


def test_format_date_natural():
    """Test format_date_natural method"""
    assert LeaveTracker.format_date_natural(date(2024, 12, 1)) == "1st Dec 2024"
    assert LeaveTracker.format_date_natural(date(2024, 12, 2)) == "2nd Dec 2024"
    assert LeaveTracker.format_date_natural(date(2024, 12, 3)) == "3rd Dec 2024"
    assert LeaveTracker.format_date_natural(date(2024, 12, 4)) == "4th Dec 2024"
    assert LeaveTracker.format_date_natural(date(2024, 12, 11)) == "11th Dec 2024"
    assert LeaveTracker.format_date_natural(date(2024, 12, 21)) == "21st Dec 2024"


def test_load_config_missing_file(tracker):
    """Test load_config with missing file"""
    with pytest.raises(FileNotFoundError):
        tracker.load_config()


def test_load_and_save_config(tracker, sample_config):
    """Test load_config and save_config methods"""
    # Save test config
    tracker.save_config(sample_config)
    
    # Load and verify
    loaded_config = tracker.load_config()
    assert loaded_config == sample_config


def test_load_and_save_data(tracker, sample_data):
    """Test load_data and save_data methods"""
    # Save test data
    tracker.save_data(sample_data)
    
    # Load and verify
    loaded_data = tracker.load_data()
    assert loaded_data == sample_data


def test_setup(tracker):
    """Test setup method"""
    # Run setup with a fixed date for testing
    with patch('leave_tracker.date') as mock_date:
        mock_date.today.return_value = date(2024, 10, 1)
        config = tracker.setup(7.0, 7.5, 15.0)
    
    # Verify config
    assert 'years' in config
    assert '2024' in config['years']
    assert config['years']['2024']['hours_per_period'] == 7.0
    assert config['years']['2024']['hours_per_day'] == 7.5
    assert config['years']['2024']['carryover_hours'] == 15.0


def test_add_leave_with_defaults(tracker, sample_config):
    """Test add_leave method with default values"""
    # Setup test config
    tracker.save_config(sample_config)
    
    # Add leave with minimal parameters
    with patch('leave_tracker.date') as mock_date:
        mock_date.today.return_value = date(2024, 12, 1)
        entry = tracker.add_leave('2024-12-25')
    
    # Verify entry
    assert entry['date'] == '2024-12-25'
    assert entry['hours'] == 7.5  # Default from config
    assert entry['description'] == '25th Dec 2024'  # Default formatted date
    
    # Verify data was saved
    data = tracker.load_data()
    assert '2024' in data
    assert len(data['2024']) == 1
    assert data['2024'][0] == entry


def test_add_leave_with_custom_values(tracker, sample_config):
    """Test add_leave method with custom values"""
    # Setup test config
    tracker.save_config(sample_config)
    
    # Add leave with custom parameters
    entry = tracker.add_leave('2024-12-25', 3.5, 'Half day Christmas')
    
    # Verify entry
    assert entry['date'] == '2024-12-25'
    assert entry['hours'] == 3.5
    assert entry['description'] == 'Half day Christmas'


def test_add_leave_missing_config(tracker):
    """Test add_leave with missing config"""
    with pytest.raises(FileNotFoundError):
        tracker.add_leave('2024-12-25')


def test_remove_leave(tracker, sample_data):
    """Test remove_leave method"""
    # Setup test data
    tracker.save_data(sample_data)
    
    # Remove an entry
    removed = tracker.remove_leave('2024-12-25')
    
    # Verify removed entry
    assert removed['date'] == '2024-12-25'
    assert removed['hours'] == 7.5
    assert removed['description'] == 'Christmas Day'
    
    # Verify data was updated
    data = tracker.load_data()
    assert len(data['2024']) == 1
    assert data['2024'][0]['date'] == '2024-12-26'


def test_remove_nonexistent_leave(tracker, sample_data):
    """Test remove_leave with nonexistent entry"""
    # Setup test data
    tracker.save_data(sample_data)
    
    # Try to remove nonexistent entry
    removed = tracker.remove_leave('2024-12-27')
    
    # Verify nothing was removed
    assert removed is None
    
    # Verify data was not changed
    data = tracker.load_data()
    assert len(data['2024']) == 2


def test_list_leave(tracker, sample_data):
    """Test list_leave method"""
    # Setup test data
    tracker.save_data(sample_data)
    
    # List entries
    entries = tracker.list_leave(2024)
    
    # Verify entries
    assert len(entries) == 2
    assert entries[0]['date'] == '2024-12-25'
    assert entries[1]['date'] == '2024-12-26'


def test_list_leave_empty(tracker):
    """Test list_leave with no entries"""
    # Setup empty data
    tracker.save_data({})
    
    # List entries
    entries = tracker.list_leave(2024)
    
    # Verify empty list
    assert entries == []


def test_calculate_balance(tracker, sample_config, sample_data):
    """Test calculate_balance method"""
    # Setup test config and data
    tracker.save_config(sample_config)
    tracker.save_data(sample_data)
    
    # Calculate balance
    balance = tracker.calculate_balance(2024)
    
    # Verify balance
    assert balance['year'] == 2024
    assert balance['carryover_hours'] == 15.0
    assert balance['annual_allowance'] == 15.0 + (7.0 * 24)  # carryover + (hours_per_period * periods)
    assert balance['used_hours'] == 15.0  # Sum of hours in sample_data
    assert balance['current_balance'] == balance['annual_allowance'] - balance['used_hours']
    assert balance['balance_days'] == balance['current_balance'] / 7.5


def test_calculate_balance_missing_config(tracker):
    """Test calculate_balance with missing config"""
    with pytest.raises(FileNotFoundError):
        tracker.calculate_balance(2024)


# Test CLI class with mocked tracker
@pytest.fixture
def mock_tracker():
    """Create a mock tracker for CLI testing"""
    return MagicMock()


@pytest.fixture
def cli(mock_tracker):
    """Create a CLI instance with mocked tracker"""
    from leave_tracker import LeaveTrackerCLI
    return LeaveTrackerCLI(tracker=mock_tracker)


def test_cli_add_command(cli, mock_tracker):
    """Test CLI add_command"""
    # Setup mock
    mock_tracker.add_leave.return_value = {
        'date': '2024-12-25',
        'hours': 7.5,
        'description': 'Christmas Day'
    }
    
    # Create args object
    args = MagicMock()
    args.date = '2024-12-25'
    args.hours = 7.5
    args.description = 'Christmas Day'
    
    # Call command
    with patch('builtins.print') as mock_print:
        cli.add_command(args)
    
    # Verify tracker was called correctly
    mock_tracker.add_leave.assert_called_once_with('2024-12-25', 7.5, 'Christmas Day')
    mock_print.assert_called_once()


def test_cli_remove_command(cli, mock_tracker):
    """Test CLI remove_command"""
    # Setup mock
    mock_tracker.remove_leave.return_value = {
        'date': '2024-12-25',
        'hours': 7.5,
        'description': 'Christmas Day'
    }
    
    # Create args object
    args = MagicMock()
    args.date = '2024-12-25'
    
    # Call command
    with patch('builtins.print') as mock_print:
        cli.remove_command(args)
    
    # Verify tracker was called correctly
    mock_tracker.remove_leave.assert_called_once_with('2024-12-25')
    mock_print.assert_called_once()


def test_cli_list_command(cli, mock_tracker):
    """Test CLI list_command"""
    # Setup mock
    mock_tracker.get_leave_year.return_value = 2024
    mock_tracker.list_leave.return_value = [
        {
            'date': '2024-12-25',
            'hours': 7.5,
            'description': 'Christmas Day'
        }
    ]
    
    # Create args object
    args = MagicMock()
    
    # Call command
    with patch('builtins.print') as mock_print:
        with patch('leave_tracker.date') as mock_date:
            mock_date.today.return_value = date(2024, 10, 1)
            cli.list_command(args)
    
    # Verify tracker was called correctly
    mock_tracker.list_leave.assert_called_once()
    assert mock_print.call_count > 0


def test_cli_balance_command(cli, mock_tracker):
    """Test CLI balance_command"""
    # Setup mock
    mock_tracker.calculate_balance.return_value = {
        'year': 2024,
        'carryover_hours': 15.0,
        'annual_allowance': 183.0,
        'used_hours': 15.0,
        'current_balance': 168.0,
        'balance_days': 22.4
    }
    
    # Create args object
    args = MagicMock()
    
    # Call command
    with patch('builtins.print') as mock_print:
        cli.balance_command(args)
    
    # Verify tracker was called correctly
    mock_tracker.calculate_balance.assert_called_once()
    assert mock_print.call_count > 0
