#!/usr/bin/env python3
"""
CS2 Demo Parser using demoparser2
Parses demo files in the demos_extracted folder and extracts match data
"""

from demoparser2 import DemoParser
import pandas as pd
import os
from pathlib import Path
import warnings
import subprocess
import shutil

BASE_DIR = Path(__file__).parent
DEMOS_DIR = BASE_DIR / "demos"
DEMOS_EXTRACTED_DIR = BASE_DIR / "demos_extracted"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_archive(archive_path: Path, output_dir: Path) -> bool:
    """Extract a RAR/ZIP archive to output directory"""
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
                timeout=300  # 5 minute timeout
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
                timeout=300
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with unrar")
                return True
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  unrar failed: {e}")
        
        # Try 7z
        try:
            result = subprocess.run(
                ['7z', 'x', f'-o{extract_to}', str(archive_path), '-y'],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with 7z")
                return True
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  7z failed: {e}")
        
        print(f"  ✗ Failed to extract {archive_path.name} - no suitable extraction tool found")
        print(f"    Please install one of: unar (brew install unar), unrar, or 7z")
        return False
        
    except Exception as e:
        print(f"  ✗ Error extracting {archive_path.name}: {e}")
        return False

def extract_all_archives():
    """Extract all archives from demos directory"""
    print("=== Extracting Demo Archives ===")
    
    if not DEMOS_DIR.exists():
        print(f"Demos directory {DEMOS_DIR} does not exist!")
        return False
    
    # Find all archive files
    archive_files = []
    for ext in ['*.rar', '*.zip', '*.7z', '*.gz']:
        archive_files.extend(DEMOS_DIR.glob(ext))
    
    if not archive_files:
        print("No archive files found in demos directory")
        return False
    
    print(f"Found {len(archive_files)} archive files")
    
    DEMOS_EXTRACTED_DIR.mkdir(exist_ok=True)
    
    successful = 0
    failed = 0
    
    for archive in archive_files:
        if extract_archive(archive, DEMOS_EXTRACTED_DIR):
            successful += 1
        else:
            failed += 1
    
    print(f"\nExtraction complete: {successful} successful, {failed} failed")
    return successful > 0

def parse_single_demo_isolated(dem_path_str: str):
    """Parse a single demo in an isolated subprocess to prevent crashes"""
    import sys
    import json
    
    code = f'''
import sys
sys.path.insert(0, "{BASE_DIR}")
from pathlib import Path
from demoparser2 import DemoParser
import pandas as pd

dem_path = Path("{dem_path_str}")
output_dir = Path("{OUTPUT_DIR}")
output_dir.mkdir(exist_ok=True)

try:
    parser = DemoParser(str(dem_path))
    header = parser.parse_header()
    
    # Parse events
    rounds_df = parser.parse_event("round_end")
    if isinstance(rounds_df, list):
        rounds_df = pd.DataFrame(rounds_df)
    
    deaths_df = parser.parse_event("player_death")
    if isinstance(deaths_df, list):
        deaths_df = pd.DataFrame(deaths_df)
    
    # Save basic round data
    stem = dem_path.stem
    if not rounds_df.empty:
        out_csv = output_dir / f"{{stem}}_rounds.csv"
        rounds_df.to_csv(out_csv, index=False)
        print(f"SUCCESS: {{len(rounds_df)}} rounds")
    
    if not deaths_df.empty:
        deaths_csv = output_dir / f"{{stem}}_deaths.csv"
        deaths_df.to_csv(deaths_csv, index=False)
        print(f"SUCCESS: {{len(deaths_df)}} deaths")
    
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {{str(e)[:100]}}")
    sys.exit(1)
'''
    
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout per demo
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr if result.stderr else result.stdout
    except subprocess.TimeoutExpired:
        return False, "Timeout after 60 seconds"
    except Exception as e:
        return False, str(e)

def parse_demo_with_demoparser2(dem_path: Path):
    """Parse a single demo file using demoparser2 in isolated subprocess"""
    print(f"Parsing {dem_path.name} with demoparser2...")
    
    success, message = parse_single_demo_isolated(str(dem_path))
    
    if success:
        print(f"  ✓ {message.strip()}")
        return True
    else:
        print(f"  ✗ Failed: {message.strip()[:100]}")
        # Create error CSV
        try:
            df = pd.DataFrame([{
                'round_num': None,
                'winning_team': None,
                'round_end_reason': None,
                'bomb_planted': None,
                'demo_type': 'cs2',
                'map_name': 'unknown',
                'parsing_status': f'error: {message[:50]}'
            }])
            stem = dem_path.stem
            out_csv = OUTPUT_DIR / f"{stem}_rounds.csv"
            df.to_csv(out_csv, index=False)
        except Exception:
            pass
        return False

def old_parse_demo_with_demoparser2(dem_path: Path):
    """Old direct parsing method - kept for reference"""
    print(f"Parsing {dem_path.name} with demoparser2...")
    
    try:
        # Initialize the parser
        try:
            parser = DemoParser(str(dem_path))
        except Exception as e:
            print(f"  ✗ Failed to initialize parser: {str(e)[:100]}")
            # Create error CSV
            df = pd.DataFrame([{
                'round_num': None,
                'winning_team': None,
                'round_end_reason': None,
                'bomb_planted': None,
                'demo_type': 'cs2',
                'map_name': 'unknown',
                'parsing_status': f'initialization_error: {str(e)[:50]}'
            }])
            stem = dem_path.stem
            out_csv = OUTPUT_DIR / f"{stem}_rounds.csv"
            df.to_csv(out_csv, index=False)
            print(f"  Created error CSV -> {out_csv}")
            return False
        
        # Parse basic match information
        try:
            header = parser.parse_header()
        except Exception as e:
            print(f"  ⚠ Failed to parse header: {e}")
            # Create minimal header
            header = {'map_name': 'unknown'}
        print(f"  Demo header: {header}")
        
        # Parse round-end events to get round information
        try:
            rounds_df = parser.parse_event("round_end")
            # Convert to DataFrame if it's a list
            if isinstance(rounds_df, list):
                rounds_df = pd.DataFrame(rounds_df)
            print(f"Found {len(rounds_df)} round_end events")
        except Exception as e:
            print(f"Failed to parse round_end events: {e}")
            rounds_df = pd.DataFrame()
        
        # Parse bomb events
        try:
            bomb_planted_df = parser.parse_event("bomb_planted")
            bomb_defused_df = parser.parse_event("bomb_defused")
            bomb_exploded_df = parser.parse_event("bomb_exploded")
            
            # Convert to DataFrames if they're lists
            if isinstance(bomb_planted_df, list):
                bomb_planted_df = pd.DataFrame(bomb_planted_df)
            if isinstance(bomb_defused_df, list):
                bomb_defused_df = pd.DataFrame(bomb_defused_df)
            if isinstance(bomb_exploded_df, list):
                bomb_exploded_df = pd.DataFrame(bomb_exploded_df)
                
            print(f"Bomb events - Planted: {len(bomb_planted_df)}, Defused: {len(bomb_defused_df)}, Exploded: {len(bomb_exploded_df)}")
        except Exception as e:
            print(f"Failed to parse bomb events: {e}")
            bomb_planted_df = pd.DataFrame()
            bomb_defused_df = pd.DataFrame()
            bomb_exploded_df = pd.DataFrame()
        
        # Parse player death events for additional context
        try:
            deaths_df = parser.parse_event("player_death")
            # Convert to DataFrame if it's a list
            if isinstance(deaths_df, list):
                deaths_df = pd.DataFrame(deaths_df)
            print(f"Found {len(deaths_df)} player death events")
        except Exception as e:
            print(f"Failed to parse player_death events: {e}")
            deaths_df = pd.DataFrame()
        
        # Create round summary data
        if not rounds_df.empty:
            # Process round data
            rounds_summary = []
            for idx, round_data in rounds_df.iterrows():
                round_num = round_data.get('round', idx + 1)
                winner = round_data.get('winner', None)
                reason = round_data.get('reason', None)
                
                # Check if bomb was planted in this round
                bomb_planted_in_round = False
                if not bomb_planted_df.empty:
                    # This is a simplified check - in practice you'd want to match by round number or tick
                    bomb_planted_in_round = len(bomb_planted_df) > 0
                
                rounds_summary.append({
                    'round_num': round_num,
                    'winning_team': winner,
                    'round_end_reason': reason,
                    'bomb_planted': bomb_planted_in_round,
                    'demo_type': 'cs2',
                    'map_name': header.get('map_name', 'unknown'),
                    'parsing_status': 'success'
                })
            
            df = pd.DataFrame(rounds_summary)
        else:
            # Create minimal data if no rounds found
            df = pd.DataFrame([{
                'round_num': None,
                'winning_team': None,
                'round_end_reason': None,
                'bomb_planted': None,
                'demo_type': 'cs2',
                'map_name': header.get('map_name', 'unknown'),
                'parsing_status': 'no_rounds_found'
            }])
        
        # Save to CSV
        stem = dem_path.stem
        out_csv = OUTPUT_DIR / f"{stem}_rounds.csv"
        df.to_csv(out_csv, index=False)
        print(f"Saved {len(df)} rounds to {out_csv}")
        
        # Also save detailed event data if available
        if not deaths_df.empty:
            deaths_csv = OUTPUT_DIR / f"{stem}_deaths.csv"
            deaths_df.to_csv(deaths_csv, index=False)
            print(f"Saved {len(deaths_df)} death events to {deaths_csv}")
        
        if not bomb_planted_df.empty or not bomb_defused_df.empty or not bomb_exploded_df.empty:
            bomb_csv = OUTPUT_DIR / f"{stem}_bomb_events.csv"
            # Combine all bomb events
            bomb_events_list = []
            
            if not bomb_planted_df.empty:
                bomb_planted_copy = bomb_planted_df.copy()
                bomb_planted_copy['event_type'] = 'planted'
                bomb_events_list.append(bomb_planted_copy)
            
            if not bomb_defused_df.empty:
                bomb_defused_copy = bomb_defused_df.copy()
                bomb_defused_copy['event_type'] = 'defused'
                bomb_events_list.append(bomb_defused_copy)
            
            if not bomb_exploded_df.empty:
                bomb_exploded_copy = bomb_exploded_df.copy()
                bomb_exploded_copy['event_type'] = 'exploded'
                bomb_events_list.append(bomb_exploded_copy)
            
            if bomb_events_list:
                bomb_events = pd.concat(bomb_events_list, ignore_index=True)
                bomb_events.to_csv(bomb_csv, index=False)
                print(f"Saved {len(bomb_events)} bomb events to {bomb_csv}")
        
        return True
        
    except Exception as e:
        print(f"Failed to parse {dem_path.name}: {e}")
        
        # Create error CSV
        df = pd.DataFrame([{
            'round_num': None,
            'winning_team': None,
            'round_end_reason': None,
            'bomb_planted': None,
            'demo_type': 'cs2',
            'map_name': 'unknown',
            'parsing_status': f'error: {str(e)[:100]}'
        }])
        
        stem = dem_path.stem
        out_csv = OUTPUT_DIR / f"{stem}_rounds.csv"
        df.to_csv(out_csv, index=False)
        print(f"Created error CSV -> {out_csv}")
        
        return False

def main():
    """Main parsing function"""
    print("=== CS2 Demo Parser using demoparser2 ===\n")
    
    # First, extract all archives from demos directory
    extract_all_archives()
    
    print(f"\n=== Scanning for Demo Files ===")
    print(f"Scanning {DEMOS_EXTRACTED_DIR} for demo files...")
    
    if not DEMOS_EXTRACTED_DIR.exists():
        print(f"Error: {DEMOS_EXTRACTED_DIR} does not exist!")
        return
    
    demo_files = []
    seen_names = set()
    
    # Find all .dem files recursively, avoiding duplicates
    for root, dirs, files in os.walk(DEMOS_EXTRACTED_DIR):
        for file in files:
            if file.lower().endswith('.dem'):
                # Only keep first occurrence of each demo file name
                if file not in seen_names:
                    seen_names.add(file)
                    demo_files.append(Path(root) / file)
    
    if not demo_files:
        print("No .dem files found in demos_extracted directory!")
        print("Extraction may have failed or archives may not contain .dem files")
        return
    
    print(f"Found {len(demo_files)} unique demo files (deduplicated):")
    for demo_file in demo_files:
        print(f"  - {demo_file.relative_to(DEMOS_EXTRACTED_DIR)}")
    
    print("\n=== Starting Parsing ===")
    
    successful_parses = 0
    failed_parses = 0
    
    for i, demo_file in enumerate(demo_files, 1):
        print(f"\n--- [{i}/{len(demo_files)}] Processing {demo_file.name} ---")
        try:
            if parse_demo_with_demoparser2(demo_file):
                successful_parses += 1
            else:
                failed_parses += 1
        except KeyboardInterrupt:
            print("\n\nParsing interrupted by user")
            break
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            failed_parses += 1
    
    print(f"\n=== Parsing Complete ===")
    print(f"Successfully parsed: {successful_parses}/{len(demo_files)}")
    print(f"Failed to parse: {failed_parses}/{len(demo_files)}")
    print(f"Results saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
