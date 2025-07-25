# Leave Tracker

A simple command-line tool to track your annual leave allowance. The leave year runs from September 1st to August 31st.

[![Tests](https://img.shields.io/badge/tests-pytest-green)](test_leave_tracker.py)

## Setup

First, configure the tool with your leave parameters:

```bash
python3 leave_tracker.py setup
```

The setup command will prompt you for:
- Hours of leave you accrue per period (there are 24 periods per year - 2 per month)
- Hours in your working day
- Hours carried over from the previous year

## Commands

### Add Leave Entry
Record a new leave entry and subtract from your balance:

```bash
python3 leave_tracker.py add <date> [<hours>] ["<description>"]
```

Both hours and description are optional:
- Hours defaults to one full working day from your configuration
- Description defaults to formatted date (e.g. "25th Dec 2024")

**Examples:**
```bash
python3 leave_tracker.py add 2024-12-25 7.5 "Christmas Day"
python3 leave_tracker.py add 2024-12-26 3.5
python3 leave_tracker.py add 2024-12-27
```

### Remove Leave Entry
Remove a leave entry by date:

```bash
python3 leave_tracker.py remove <date>
```

**Example:**
```bash
python3 leave_tracker.py remove 2024-12-25
```

### List Leave Entries
View all leave entries for the current leave year:

```bash
python3 leave_tracker.py list
```

Shows entries with date, hours, status (PAST/FUTURE), and description.

### View Balance
Check your current leave balance:

```bash
python3 leave_tracker.py balance
```

Shows in a nicely formatted display:
- Annual allowance
- Hours used so far
- Days used so far
- Current balance in hours and days

## Data Storage

Configuration and leave data are stored in your home directory:
- `~/.leave_tracker_config.json` - Your setup configuration
- `~/.leave_tracker_data.json` - Your leave entries

## Leave Year

The tool automatically handles the leave year cycle (September 1st - August 31st). Entries are grouped by leave year, not calendar year.

## Development

### Testing

The project uses pytest for testing. To run the tests:

1. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest -v test_leave_tracker.py
   ```

Alternatively, use the provided script:
```bash
./run_tests.sh
```

This will create a virtual environment if it doesn't exist, install dependencies, and run the tests.