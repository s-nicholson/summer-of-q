#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, date
from pathlib import Path

CONFIG_FILE = Path.home() / '.leave_tracker_config.json'
DATA_FILE = Path.home() / '.leave_tracker_data.json'

def get_leave_year(target_date):
    """Get leave year (Sept 1 - Aug 31) for a given date"""
    if target_date.month >= 9:
        return target_date.year
    return target_date.year - 1

def format_date_natural(date_obj):
    """Format date as '20th Sept 2024'"""
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    month = date_obj.strftime('%b')
    year = date_obj.year
    return f"{day}{suffix} {month} {year}"

def load_config():
    if not CONFIG_FILE.exists():
        print("No configuration found. Run 'setup' command first.")
        exit(1)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    
    # Handle legacy config format
    if 'years' not in config:
        config = {
            'years': {
                str(get_leave_year(date.today())): {
                    'hours_per_period': config['hours_per_period'],
                    'hours_per_day': config['hours_per_day'],
                    'carryover_hours': config['carryover_hours']
                }
            }
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    return config

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def setup(args):
    print("Leave Tracker Setup")
    print("==================")
    
    current_year = get_leave_year(date.today())
    config = load_config() if CONFIG_FILE.exists() else {'years': {}}
    
    hours_per_period = float(input("Hours accrued per period (2 periods per month): "))
    hours_per_day = float(input("Hours in a working day: "))
    carryover_hours = float(input("Hours carried over from previous year: "))
    
    config['years'][str(current_year)] = {
        'hours_per_period': hours_per_period,
        'hours_per_day': hours_per_day,
        'carryover_hours': carryover_hours
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved for {current_year}-{current_year+1}.")

def add_leave(args):
    config = load_config()
    data = load_data()
    
    leave_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    year = get_leave_year(leave_date)
    
    if str(year) not in config['years']:
        print(f"No configuration found for {year}-{year+1}. Run 'setup' command first.")
        return
    
    if str(year) not in data:
        data[str(year)] = []
    
    hours = args.hours if args.hours is not None else config['years'][str(year)]['hours_per_day']
    description = args.description if args.description else format_date_natural(leave_date)
    
    entry = {
        'date': args.date,
        'hours': hours,
        'description': description
    }
    data[str(year)].append(entry)
    save_data(data)
    print(f"Added {hours:.2f}h leave on {args.date}: {description}")

def remove_leave(args):
    data = load_data()
    target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    year = get_leave_year(target_date)
    
    if str(year) not in data:
        print("No leave entries found for that date.")
        return
    
    entries = data[str(year)]
    for i, entry in enumerate(entries):
        if entry['date'] == args.date:
            removed = entries.pop(i)
            save_data(data)
            print(f"Removed {removed['hours']:.2f}h leave on {args.date}: {removed['description']}")
            return
    
    print("No leave entry found for that date.")

def list_leave(args):
    config = load_config()
    data = load_data()
    current_year = get_leave_year(date.today())
    
    if str(current_year) not in config['years']:
        print(f"No configuration found for {current_year}-{current_year+1}. Run 'setup' command first.")
        return
    
    if str(current_year) not in data:
        print("No leave entries for current year.")
        return
    
    entries = sorted(data[str(current_year)], key=lambda x: x['date'])
    today = date.today()
    
    print(f"\nLeave entries for {current_year}-{current_year+1}:")
    print("-" * 50)
    
    for entry in entries:
        entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
        status = "PAST" if entry_date < today else "FUTURE"
        print(f"{entry['date']} | {entry['hours']:5.2f}h | {status:6} | {entry['description']}")

def balance(args):
    config = load_config()
    data = load_data()
    current_year = get_leave_year(date.today())
    
    if str(current_year) not in config['years']:
        print(f"No configuration found for {current_year}-{current_year+1}. Run 'setup' command first.")
        return
    
    year_config = config['years'][str(current_year)]
    
    # Calculate total allowance for the year
    periods_per_year = 24  # 2 periods per month * 12 months
    annual_allowance = year_config['hours_per_period'] * periods_per_year + year_config['carryover_hours']
    
    # Calculate used leave
    used_hours = 0
    if str(current_year) in data:
        used_hours = sum(entry['hours'] for entry in data[str(current_year)])
    
    current_balance = annual_allowance - used_hours
    
    print(f"\nLeave Balance for {current_year}-{current_year+1}:")
    print(f"Carryover from previous year: {year_config['carryover_hours']:.2f}h")
    print(f"Annual allowance: {annual_allowance:.2f}h")
    print(f"Used so far: {used_hours:.2f}h")
    print(f"Current balance: {current_balance:.2f}h")
    print(f"Balance in days: {current_balance / year_config['hours_per_day']:.2f}")

def main():
    parser = argparse.ArgumentParser(description='Annual Leave Tracker')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Configure leave tracker')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add leave entry')
    add_parser.add_argument('date', help='Date in YYYY-MM-DD format')
    add_parser.add_argument('hours', type=float, nargs='?', help='Hours of leave (defaults to full day)')
    add_parser.add_argument('description', nargs='?', help='Description of leave (defaults to formatted date)')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove leave entry')
    remove_parser.add_argument('date', help='Date in YYYY-MM-DD format')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List leave entries for current year')
    
    # Balance command
    balance_parser = subparsers.add_parser('balance', help='Show current leave balance')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'setup':
        setup(args)
    elif args.command == 'add':
        add_leave(args)
    elif args.command == 'remove':
        remove_leave(args)
    elif args.command == 'list':
        list_leave(args)
    elif args.command == 'balance':
        balance(args)

if __name__ == '__main__':
    main()