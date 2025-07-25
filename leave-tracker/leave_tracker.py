#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any, Union


class LeaveTracker:
    """Core class for leave tracking functionality"""
    
    def __init__(self, config_path=None, data_path=None):
        """Initialize with optional custom paths for testing"""
        self.config_path = config_path or Path.home() / '.leave_tracker_config.json'
        self.data_path = data_path or Path.home() / '.leave_tracker_data.json'
    
    @staticmethod
    def get_leave_year(target_date: date) -> int:
        """Get leave year (Sept 1 - Aug 31) for a given date"""
        if target_date.month >= 9:
            return target_date.year
        return target_date.year - 1
    
    @staticmethod
    def format_date_natural(date_obj: date) -> str:
        """Format date as '20th Sept 2024'"""
        day = date_obj.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        month = date_obj.strftime('%b')
        year = date_obj.year
        return f"{day}{suffix} {month} {year}"
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if not self.config_path.exists():
            raise FileNotFoundError("No configuration found. Run 'setup' command first.")
        
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            
            # Handle legacy config format
            if 'years' not in config:
                config = {
                    'years': {
                        str(self.get_leave_year(date.today())): {
                            'hours_per_period': config['hours_per_period'],
                            'hours_per_day': config['hours_per_day'],
                            'carryover_hours': config['carryover_hours']
                        }
                    }
                }
                self.save_config(config)
            
            return config
        except json.JSONDecodeError:
            # If the file is empty or invalid JSON, raise FileNotFoundError
            raise FileNotFoundError("Invalid configuration file. Run 'setup' command first.")
    
    def save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_data(self) -> Dict:
        """Load leave data from file"""
        if not self.data_path.exists():
            return {}
        
        try:
            with open(self.data_path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or invalid JSON, return empty dict
            return {}
    
    def save_data(self, data: Dict) -> None:
        """Save leave data to file"""
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def setup(self, hours_per_period: float, hours_per_day: float, carryover_hours: float) -> Dict:
        """Set up configuration for current leave year"""
        current_year = self.get_leave_year(date.today())
        
        try:
            config = self.load_config()
        except FileNotFoundError:
            config = {'years': {}}
        
        config['years'][str(current_year)] = {
            'hours_per_period': hours_per_period,
            'hours_per_day': hours_per_day,
            'carryover_hours': carryover_hours
        }
        
        self.save_config(config)
        return config
    
    def add_leave(self, leave_date_str: str, hours: Optional[float] = None, 
                  description: Optional[str] = None) -> Dict:
        """Add a leave entry"""
        config = self.load_config()
        data = self.load_data()
        
        leave_date = datetime.strptime(leave_date_str, '%Y-%m-%d').date()
        year = self.get_leave_year(leave_date)
        
        if str(year) not in config['years']:
            raise ValueError(f"No configuration found for {year}-{year+1}. Run 'setup' command first.")
        
        if str(year) not in data:
            data[str(year)] = []
        
        if hours is None:
            hours = config['years'][str(year)]['hours_per_day']
            
        if description is None:
            description = self.format_date_natural(leave_date)
        
        entry = {
            'date': leave_date_str,
            'hours': hours,
            'description': description
        }
        
        data[str(year)].append(entry)
        self.save_data(data)
        return entry
    
    def remove_leave(self, leave_date_str: str) -> Optional[Dict]:
        """Remove a leave entry by date"""
        data = self.load_data()
        target_date = datetime.strptime(leave_date_str, '%Y-%m-%d').date()
        year = self.get_leave_year(target_date)
        
        if str(year) not in data:
            return None
        
        entries = data[str(year)]
        for i, entry in enumerate(entries):
            if entry['date'] == leave_date_str:
                removed = entries.pop(i)
                self.save_data(data)
                return removed
        
        return None
    
    def list_leave(self, year: Optional[int] = None) -> List[Dict]:
        """List leave entries for a specific year"""
        data = self.load_data()
        target_year = year if year is not None else self.get_leave_year(date.today())
        
        if str(target_year) not in data:
            return []
        
        entries = sorted(data[str(target_year)], key=lambda x: x['date'])
        return entries
    
    def calculate_balance(self, year: Optional[int] = None) -> Dict:
        """Calculate leave balance for a specific year"""
        config = self.load_config()
        data = self.load_data()
        
        target_year = year if year is not None else self.get_leave_year(date.today())
        
        if str(target_year) not in config['years']:
            raise ValueError(f"No configuration found for {target_year}-{target_year+1}. Run 'setup' command first.")
        
        year_config = config['years'][str(target_year)]
        
        # Calculate total allowance for the year
        periods_per_year = 24  # 2 periods per month * 12 months
        annual_allowance = year_config['hours_per_period'] * periods_per_year + year_config['carryover_hours']
        
        # Calculate used leave
        used_hours = 0
        if str(target_year) in data:
            used_hours = sum(entry['hours'] for entry in data[str(target_year)])
        
        current_balance = annual_allowance - used_hours
        
        return {
            'year': target_year,
            'carryover_hours': year_config['carryover_hours'],
            'annual_allowance': annual_allowance,
            'used_hours': used_hours,
            'used_days': used_hours / year_config['hours_per_day'],
            'current_balance': current_balance,
            'balance_days': current_balance / year_config['hours_per_day']
        }


class LeaveTrackerCLI:
    """Command-line interface for the LeaveTracker"""
    
    def __init__(self, tracker=None):
        """Initialize with optional tracker for testing"""
        self.tracker = tracker or LeaveTracker()
    
    def setup_command(self, args):
        """Handle setup command"""
        print("Leave Tracker Setup")
        print("==================")
        
        hours_per_period = float(input("Hours accrued per period (2 periods per month): "))
        hours_per_day = float(input("Hours in a working day: "))
        carryover_hours = float(input("Hours carried over from previous year: "))
        
        config = self.tracker.setup(hours_per_period, hours_per_day, carryover_hours)
        current_year = self.tracker.get_leave_year(date.today())
        print(f"Configuration saved for {current_year}-{current_year+1}.")
    
    def add_command(self, args):
        """Handle add command"""
        try:
            entry = self.tracker.add_leave(args.date, args.hours, args.description)
            print(f"Added {entry['hours']:.2f}h leave on {args.date}: {entry['description']}")
        except (ValueError, FileNotFoundError) as e:
            print(str(e))
    
    def remove_command(self, args):
        """Handle remove command"""
        removed = self.tracker.remove_leave(args.date)
        if removed:
            print(f"Removed {removed['hours']:.2f}h leave on {args.date}: {removed['description']}")
        else:
            print("No leave entry found for that date.")
    
    def _print_box(self, title, headers=None, rows=None, footer_rows=None):
        """Helper method to print consistent box-style output
        
        Args:
            title: Title of the box
            headers: List of column headers (optional)
            rows: List of rows, each row is a list of values
            footer_rows: List of rows for the footer section (optional)
        """
        # Calculate the width needed for each column
        col_widths = []
        
        # Initialize with header widths
        if headers:
            col_widths = [len(str(h)) for h in headers]
            
        # Update with row content widths
        if rows:
            for row in rows:
                for i, cell in enumerate(row):
                    if i >= len(col_widths):
                        col_widths.append(len(str(cell)))
                    else:
                        col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Calculate total width (sum of column widths + separators)
        total_width = sum(col_widths) + (3 * (len(col_widths) - 1)) + 6  # 3 spaces between cols, 3 spaces padding on each side
        
        # Print the box
        print(f"\n╔{'═' * total_width}╗")
        print(f"║{title.center(total_width)}║")
        
        if headers:
            print(f"╠{'═' * total_width}╣")
            header_str = "║   "
            for i, header in enumerate(headers):
                header_str += f"{str(header):<{col_widths[i]}}"
                if i < len(headers) - 1:
                    header_str += "   "
            header_str += "   ║"
            print(header_str)
            
        if rows:
            print(f"╠{'═' * total_width}╣")
            for row in rows:
                row_str = "║   "
                for i, cell in enumerate(row):
                    row_str += f"{str(cell):<{col_widths[i]}}"
                    if i < len(row) - 1:
                        row_str += "   "
                row_str += "   ║"
                print(row_str)
        
        if footer_rows:
            print(f"╠{'═' * total_width}╣")
            for row in footer_rows:
                row_str = "║   "
                for i, cell in enumerate(row):
                    row_str += f"{str(cell):<{col_widths[i]}}"
                    if i < len(row) - 1:
                        row_str += "   "
                row_str += "   ║"
                print(row_str)
                
        print(f"╚{'═' * total_width}╝")

    def list_command(self, args):
        """Handle list command"""
        try:
            current_year = self.tracker.get_leave_year(date.today())
            entries = self.tracker.list_leave()
            
            if not entries:
                print("No leave entries for current year.")
                return
            
            title = f"Leave entries for {current_year}-{current_year+1}"
            headers = ["Date", "Hours", "Status", "Description"]
            
            rows = []
            today = date.today()
            for entry in entries:
                entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
                status = "PAST" if entry_date < today else "FUTURE"
                rows.append([
                    entry['date'],
                    f"{entry['hours']:.2f}h",
                    status,
                    entry['description']
                ])
            
            self._print_box(title, headers, rows)
        except FileNotFoundError as e:
            print(str(e))
    
    def balance_command(self, args):
        """Handle balance command"""
        try:
            balance = self.tracker.calculate_balance()
            year = balance['year']
            
            title = f"Leave Balance for {year}-{year+1}"
            rows = [
                ["Carryover:", f"{balance['carryover_hours']:.2f} hours"],
                ["Annual allowance:", f"{balance['annual_allowance']:.2f} hours"],
                ["Used so far:", f"{balance['used_hours']:.2f} hours"],
                ["Days used:", f"{balance['used_days']:.2f} days"]
            ]
            
            footer_rows = [
                ["Current balance:", f"{balance['current_balance']:.2f} hours"],
                ["Balance in days:", f"{balance['balance_days']:.2f} days"]
            ]
            
            self._print_box(title, None, rows, footer_rows)
        except (ValueError, FileNotFoundError) as e:
            print(str(e))
    
    def run(self):
        """Run the CLI application"""
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
        
        command_handlers = {
            'setup': self.setup_command,
            'add': self.add_command,
            'remove': self.remove_command,
            'list': self.list_command,
            'balance': self.balance_command
        }
        
        command_handlers[args.command](args)


def main():
    """Main entry point"""
    cli = LeaveTrackerCLI()
    cli.run()


if __name__ == '__main__':
    main()
