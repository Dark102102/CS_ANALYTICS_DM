#!/usr/bin/env python3
"""
Parse existing valid demo files with robust error handling
"""

from demoparser2 import DemoParser
import pandas as pd
import os
from pathlib import Path
import warnings
import subprocess
import sys
import time

BASE_DIR = Path(__file__).parent
DEMOS_EXTRACTED_DIR = BASE_DIR / "demos_extracted"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_demo_robust(demo_path: Path):
    """Parse a demo file with comprehensive error handling"""
    print(f"Parsing {demo_path.name}...")
    
    try:
        # Initialize parser
        parser = DemoParser(str(demo_path))
        
        # Get header information
        try:
            header = parser.parse_header()
            map_name = header.get('map_name', 'unknown')
            print(f"  Map: {map_name}")
        except Exception as e:
            print(f"  Warning: Could not parse header: {e}")
            map_name = 'unknown'
        
        # Parse round events
        rounds_data = []
        try:
            rounds_events = parser.parse_event("round_end")
            if isinstance(rounds_events, list):
                rounds_data = rounds_events
            elif hasattr(rounds_events, 'to_dict'):
                rounds_data = [rounds_events.to_dict()]
            print(f"  Found {len(rounds_data)} round events")
        except Exception as e:
            print(f"  Warning: Could not parse round events: {e}")
        
        # Parse death events
        deaths_data = []
        try:
            deaths_events = parser.parse_event("player_death")
            if isinstance(deaths_events, list):
                deaths_data = deaths_events
            elif hasattr(deaths_events, 'to_dict'):
                deaths_data = [deaths_events.to_dict()]
            print(f"  Found {len(deaths_data)} death events")
        except Exception as e:
            print(f"  Warning: Could not parse death events: {e}")
        
        # Save rounds data
        if rounds_data:
            rounds_df = pd.DataFrame(rounds_data)
            rounds_csv = OUTPUT_DIR / f"{demo_path.stem}_rounds.csv"
            rounds_df.to_csv(rounds_csv, index=False)
            print(f"  ✓ Saved {len(rounds_df)} rounds to {rounds_csv.name}")
        
        # Save deaths data
        if deaths_data:
            deaths_df = pd.DataFrame(deaths_data)
            deaths_csv = OUTPUT_DIR / f"{demo_path.stem}_deaths.csv"
            deaths_df.to_csv(deaths_csv, index=False)
            print(f"  ✓ Saved {len(deaths_df)} deaths to {deaths_csv.name}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to parse {demo_path.name}: {e}")
        return False

def main():
    """Main parsing function for existing demos"""
    print("=== Parsing Existing Valid Demo Files ===\n")
    
    # Find all demo files with actual content (>1MB)
    valid_demos = []
    for root, dirs, files in os.walk(DEMOS_EXTRACTED_DIR):
        for file in files:
            if file.lower().endswith('.dem'):
                demo_path = Path(root) / file
                if demo_path.stat().st_size > 1024 * 1024:  # > 1MB
                    valid_demos.append(demo_path)
    
    if not valid_demos:
        print("No valid demo files found (>1MB)")
        return
    
    print(f"Found {len(valid_demos)} valid demo files:")
    for demo in valid_demos:
        size_mb = demo.stat().st_size / (1024 * 1024)
        print(f"  - {demo.name} ({size_mb:.1f}MB)")
    
    print(f"\n=== Starting Parsing ===")
    
    successful = 0
    failed = 0
    
    for i, demo_path in enumerate(valid_demos, 1):
        print(f"\n--- [{i}/{len(valid_demos)}] Processing {demo_path.name} ---")
        if parse_demo_robust(demo_path):
            successful += 1
        else:
            failed += 1
    
    print(f"\n=== Parsing Complete ===")
    print(f"Successfully parsed: {successful}/{len(valid_demos)}")
    print(f"Failed to parse: {failed}/{len(valid_demos)}")
    
    # Show summary of generated files
    csv_files = list(OUTPUT_DIR.glob("*.csv"))
    print(f"\nGenerated {len(csv_files)} CSV files:")
    for csv_file in sorted(csv_files):
        try:
            df = pd.read_csv(csv_file)
            if "_rounds.csv" in csv_file.name:
                print(f"  - {csv_file.name}: {len(df)} rounds")
            elif "_deaths.csv" in csv_file.name:
                print(f"  - {csv_file.name}: {len(df)} deaths")
        except Exception as e:
            print(f"  - {csv_file.name}: Error reading file ({e})")

if __name__ == "__main__":
    main()
