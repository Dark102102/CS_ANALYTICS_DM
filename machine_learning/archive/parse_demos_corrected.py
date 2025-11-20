#!/usr/bin/env python3
"""
Corrected Demo Parser - Uses proper demoparser2 API
"""

from demoparser2 import DemoParser
import pandas as pd
import os
from pathlib import Path
import warnings
import subprocess
import shutil
import time

BASE_DIR = Path(__file__).parent
DEMOS_DIR = BASE_DIR / "demos"
DEMOS_EXTRACTED_DIR = BASE_DIR / "demos_extracted"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_single_archive(archive_path: Path, output_dir: Path) -> bool:
    """Extract a single RAR/ZIP archive to output directory"""
    print(f"Extracting {archive_path.name}...")
    
    try:
        # Create output subdirectory for this archive
        extract_to = output_dir / archive_path.stem
        extract_to.mkdir(exist_ok=True)
        
        # Try using Python's built-in zipfile for .zip files
        if archive_path.suffix.lower() == '.zip':
            import zipfile
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"  ✓ Extracted with zipfile")
            return True
        
        # For RAR files, try multiple extraction methods
        # Try unar (commonly available on macOS via Homebrew)
        try:
            result = subprocess.run(
                ['unar', '-q', '-o', str(extract_to), str(archive_path)],
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with unar")
                return True
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  unar failed: {e}")
        
        # Try unrar
        try:
            result = subprocess.run(
                ['unrar', 'x', '-y', str(archive_path), str(extract_to) + '/'],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with unrar")
                return True
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  unrar failed: {e}")
        
        print(f"  ✗ Failed to extract {archive_path.name}")
        return False
        
    except Exception as e:
        print(f"  ✗ Error extracting {archive_path.name}: {e}")
        return False

def parse_demo_with_demoparser2(demo_file: Path) -> bool:
    """Parse a single demo file using demoparser2 with correct API"""
    print(f"  Parsing {demo_file.name}...")
    
    try:
        # Create parser
        parser = DemoParser(str(demo_file))
        
        # Get events (this is the new API)
        events = parser.parse_events()
        if events.empty:
            print(f"    ✗ No events found in {demo_file.name}")
            return False
        
        print(f"    Found {len(events)} events")
        
        # Filter for round-related events
        round_events = events[events['event_name'].isin(['round_start', 'round_end', 'bomb_planted', 'bomb_defused', 'bomb_exploded'])]
        
        if not round_events.empty:
            # Create rounds data
            rounds_data = []
            current_round = 0
            
            for _, event in round_events.iterrows():
                if event['event_name'] == 'round_start':
                    current_round += 1
                elif event['event_name'] == 'round_end':
                    rounds_data.append({
                        'round': current_round,
                        'tick': event['tick'],
                        'reason': event.get('reason', ''),
                        'winner': event.get('winner', '')
                    })
            
            if rounds_data:
                rounds_df = pd.DataFrame(rounds_data)
                rounds_file = OUTPUT_DIR / f"{demo_file.stem}_rounds.csv"
                rounds_df.to_csv(rounds_file, index=False)
                print(f"    ✓ Rounds saved: {rounds_file.name} ({len(rounds_df)} rounds)")
        
        # Filter for death events
        death_events = events[events['event_name'] == 'player_death']
        
        if not death_events.empty:
            # Create deaths data
            deaths_data = []
            for _, event in death_events.iterrows():
                death_data = {
                    'tick': event['tick'],
                    'attacker_name': event.get('attacker_name', ''),
                    'attacker_steamid': event.get('attacker_steamid', ''),
                    'user_name': event.get('user_name', ''),
                    'user_steamid': event.get('user_steamid', ''),
                    'weapon': event.get('weapon', ''),
                    'headshot': event.get('headshot', False),
                    'distance': event.get('distance', 0),
                    'dmg_health': event.get('dmg_health', 0),
                    'dmg_armor': event.get('dmg_armor', 0)
                }
                deaths_data.append(death_data)
            
            if deaths_data:
                deaths_df = pd.DataFrame(deaths_data)
                deaths_file = OUTPUT_DIR / f"{demo_file.stem}_deaths.csv"
                deaths_df.to_csv(deaths_file, index=False)
                print(f"    ✓ Deaths saved: {deaths_file.name} ({len(deaths_df)} deaths)")
        
        print(f"  ✓ Successfully parsed {demo_file.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error parsing {demo_file.name}: {e}")
        return False

def process_demos_corrected():
    """Process demos with corrected API"""
    print("=== Corrected Demo Processing ===")
    
    if not DEMOS_DIR.exists():
        print(f"Demos directory {DEMOS_DIR} does not exist!")
        return
    
    # Get all RAR files
    rar_files = list(DEMOS_DIR.glob('*.rar'))
    print(f"Found {len(rar_files)} RAR files to process")
    
    if not rar_files:
        print("No RAR files found!")
        return
    
    successful_extractions = 0
    successful_parses = 0
    
    # Process each demo individually
    for i, rar_file in enumerate(rar_files, 1):
        print(f"\n--- Processing {i}/{len(rar_files)}: {rar_file.name} ---")
        
        # Extract
        if extract_single_archive(rar_file, DEMOS_EXTRACTED_DIR):
            successful_extractions += 1
            print(f"  ✓ Extracted {rar_file.name}")
            
            # Find .dem files in the extracted directory
            extracted_dir = DEMOS_EXTRACTED_DIR / rar_file.stem
            demo_files = list(extracted_dir.rglob('*.dem'))
            
            if demo_files:
                print(f"  Found {len(demo_files)} demo files")
                
                # Parse each demo
                for demo_file in demo_files:
                    if parse_demo_with_demoparser2(demo_file):
                        successful_parses += 1
            else:
                print(f"  ✗ No .dem files found in {extracted_dir}")
            
            # Clean up extracted files to save space
            shutil.rmtree(extracted_dir)
            print(f"  Cleaned up {extracted_dir.name}")
        else:
            print(f"  ✗ Failed to extract {rar_file.name}")
    
    print(f"\n=== Processing Complete ===")
    print(f"Successfully extracted: {successful_extractions}/{len(rar_files)}")
    print(f"Successfully parsed: {successful_parses} demos")
    
    # Final summary
    output_files = list(OUTPUT_DIR.glob('*.csv'))
    print(f"Generated {len(output_files)} CSV files:")
    for file in output_files:
        file_size = file.stat().st_size
        print(f"  - {file.name} ({file_size:,} bytes)")

if __name__ == "__main__":
    process_demos_corrected()
