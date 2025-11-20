#!/usr/bin/env python3
"""
Working Demo Parser - Uses correct demoparser2 API with lists
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
    """Extract a single RAR/ZIP archive with timeout handling"""
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
        
        # For RAR files, try multiple extraction methods with shorter timeouts
        # Try unar (commonly available on macOS via Homebrew)
        try:
            result = subprocess.run(
                ['unar', '-q', '-o', str(extract_to), str(archive_path)],
                capture_output=True,
                text=True,
                timeout=45  # 45 second timeout
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with unar")
                return True
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            print(f"  ✗ unar timed out")
        except Exception as e:
            print(f"  unar failed: {e}")
        
        # Try unrar
        try:
            result = subprocess.run(
                ['unrar', 'x', '-y', str(archive_path), str(extract_to) + '/'],
                capture_output=True,
                text=True,
                timeout=45
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with unrar")
                return True
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            print(f"  ✗ unrar timed out")
        except Exception as e:
            print(f"  unrar failed: {e}")
        
        print(f"  ✗ Failed to extract {archive_path.name}")
        return False
        
    except Exception as e:
        print(f"  ✗ Error extracting {archive_path.name}: {e}")
        return False

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
        
        # Parse all events at once (this is more efficient)
        try:
            # Get all the events we need
            events = parser.parse_events(['round_end', 'player_death', 'bomb_planted', 'bomb_defused', 'bomb_exploded'])
            
            if not events:
                print(f"    ✗ No events found in {demo_file.name}")
                return False
            
            print(f"    Found {len(events)} total events")
            
            # Convert to DataFrame
            events_data = []
            for event in events:
                event_data = {
                    'event_type': event.get('event_name', ''),
                    'tick': event.get('tick', 0),
                    'round': event.get('round', 0),
                    'reason': event.get('reason', ''),
                    'winner': event.get('winner', ''),
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
                events_data.append(event_data)
            
            if events_data:
                # Create DataFrame and save
                events_df = pd.DataFrame(events_data)
                events_file = OUTPUT_DIR / f"{demo_file.stem}_events.csv"
                events_df.to_csv(events_file, index=False)
                print(f"    ✓ Events saved: {events_file.name} ({len(events_df)} events)")
                return True
            else:
                print(f"    ✗ No events data in {demo_file.name}")
                return False
        
        except Exception as e:
            print(f"    ✗ Events parsing failed: {e}")
            return False
        
    except Exception as e:
        print(f"  ✗ Error parsing {demo_file.name}: {e}")
        return False

def process_demos_working():
    """Process all demos with proper error handling"""
    print("=== Working Demo Processing ===")
    
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
    total_events = 0
    
    # Process each demo individually
    for i, rar_file in enumerate(rar_files, 1):
        print(f"\n--- Processing {i}/{len(rar_files)}: {rar_file.name} ---")
        
        # Extract with timeout
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
                        # Count events in the generated file
                        events_file = OUTPUT_DIR / f"{demo_file.stem}_events.csv"
                        if events_file.exists():
                            events_df = pd.read_csv(events_file)
                            total_events += len(events_df)
            else:
                print(f"  ✗ No .dem files found in {extracted_dir}")
            
            # Clean up extracted files to save space
            shutil.rmtree(extracted_dir)
            print(f"  Cleaned up {extracted_dir.name}")
        else:
            print(f"  ✗ Failed to extract {rar_file.name}")
        
        # Small delay between demos
        time.sleep(1)
    
    print(f"\n=== Processing Complete ===")
    print(f"Successfully extracted: {successful_extractions}/{len(rar_files)}")
    print(f"Successfully parsed: {successful_parses} demos")
    print(f"Total events extracted: {total_events}")
    
    # Final summary
    output_files = list(OUTPUT_DIR.glob('*.csv'))
    print(f"\nGenerated {len(output_files)} CSV files:")
    for file in output_files:
        file_size = file.stat().st_size
        print(f"  - {file.name} ({file_size:,} bytes)")

if __name__ == "__main__":
    process_demos_working()
