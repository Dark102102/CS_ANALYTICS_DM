#!/usr/bin/env python3
"""
Final Demo Parser - Uses correct demoparser2 API
Parses .dem files directly from the demos folder
"""

from demoparser2 import DemoParser
import pandas as pd
import os
from pathlib import Path
import warnings
import time

BASE_DIR = Path(__file__).parent
DEMOS_DIR = BASE_DIR / "demos"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_demo_with_demoparser2(demo_file: Path) -> bool:
    """Parse a single demo file using correct demoparser2 API"""
    print(f"  Parsing {demo_file.name}...")
    
    try:
        # Create parser
        parser = DemoParser(str(demo_file))
        
        # Get header info first
        try:
            header = parser.parse_header()
            print(f"    Map: {header.get('map_name', 'Unknown')}")
        except Exception as e:
            print(f"    Header parsing failed: {e}")
        
        # Parse specific events we need
        events_data = []
        
        # Get round events
        try:
            round_events = parser.parse_events('round_end')
            if not round_events.empty:
                print(f"    Found {len(round_events)} round_end events")
                for _, event in round_events.iterrows():
                    events_data.append({
                        'event_type': 'round_end',
                        'tick': event.get('tick', 0),
                        'round': event.get('round', 0),
                        'reason': event.get('reason', ''),
                        'winner': event.get('winner', '')
                    })
        except Exception as e:
            print(f"    Round events failed: {e}")
        
        # Get death events
        try:
            death_events = parser.parse_events('player_death')
            if not death_events.empty:
                print(f"    Found {len(death_events)} death events")
                for _, event in death_events.iterrows():
                    events_data.append({
                        'event_type': 'player_death',
                        'tick': event.get('tick', 0),
                        'attacker_name': event.get('attacker_name', ''),
                        'attacker_steamid': event.get('attacker_steamid', ''),
                        'user_name': event.get('user_name', ''),
                        'user_steamid': event.get('user_steamid', ''),
                        'weapon': event.get('weapon', ''),
                        'headshot': event.get('headshot', False),
                        'distance': event.get('distance', 0),
                        'dmg_health': event.get('dmg_health', 0),
                        'dmg_armor': event.get('dmg_armor', 0)
                    })
        except Exception as e:
            print(f"    Death events failed: {e}")
        
        # Get bomb events
        try:
            bomb_events = parser.parse_events('bomb_planted')
            if not bomb_events.empty:
                print(f"    Found {len(bomb_events)} bomb_planted events")
                for _, event in bomb_events.iterrows():
                    events_data.append({
                        'event_type': 'bomb_planted',
                        'tick': event.get('tick', 0),
                        'user_name': event.get('user_name', ''),
                        'user_steamid': event.get('user_steamid', '')
                    })
        except Exception as e:
            print(f"    Bomb events failed: {e}")
        
        if events_data:
            # Create DataFrame and save
            events_df = pd.DataFrame(events_data)
            events_file = OUTPUT_DIR / f"{demo_file.stem}_events.csv"
            events_df.to_csv(events_file, index=False)
            print(f"    ✓ Events saved: {events_file.name} ({len(events_df)} events)")
            return True
        else:
            print(f"    ✗ No events found in {demo_file.name}")
            return False
        
    except Exception as e:
        print(f"  ✗ Error parsing {demo_file.name}: {e}")
        return False

def process_demos_final():
    """Process all demos with proper error handling"""
    print("=== Final Demo Processing ===")

    if not DEMOS_DIR.exists():
        print(f"Demos directory {DEMOS_DIR} does not exist!")
        return

    # Get all .dem files directly
    demo_files = list(DEMOS_DIR.glob('*.dem'))
    print(f"Found {len(demo_files)} demo files to process")

    if not demo_files:
        print("No demo files found!")
        return

    successful_parses = 0
    total_events = 0

    # Process each demo file
    for i, demo_file in enumerate(demo_files, 1):
        print(f"\n--- Processing {i}/{len(demo_files)}: {demo_file.name} ---")

        if parse_demo_with_demoparser2(demo_file):
            successful_parses += 1
            # Count events in the generated file
            events_file = OUTPUT_DIR / f"{demo_file.stem}_events.csv"
            if events_file.exists():
                events_df = pd.read_csv(events_file)
                total_events += len(events_df)

        # Small delay between demos
        time.sleep(0.5)

    print(f"\n=== Processing Complete ===")
    print(f"Successfully parsed: {successful_parses}/{len(demo_files)} demos")
    print(f"Total events extracted: {total_events}")

    # Final summary
    output_files = list(OUTPUT_DIR.glob('*.csv'))
    print(f"\nGenerated {len(output_files)} CSV files:")
    for file in output_files:
        file_size = file.stat().st_size
        print(f"  - {file.name} ({file_size:,} bytes)")

if __name__ == "__main__":
    process_demos_final()
