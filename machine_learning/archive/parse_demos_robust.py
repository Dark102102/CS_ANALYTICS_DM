#!/usr/bin/env python3
"""
Robust CS2 Demo Parser using demoparser2
Handles parsing errors gracefully and continues processing other demos
"""

import subprocess
import sys
import os
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
DEMOS_EXTRACTED_DIR = BASE_DIR / "demos_extracted"
OUTPUT_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_demo_robust(dem_path: Path):
    """Parse a single demo file using a subprocess to handle panics"""
    print(f"Parsing {dem_path.name}...")
    
    # Create a temporary script for parsing this specific demo
    temp_script = BASE_DIR / "temp_parser.py"
    
    script_content = f'''#!/usr/bin/env python3
import sys
from demoparser2 import DemoParser
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

try:
    parser = DemoParser("{dem_path}")
    
    # Parse header
    try:
        header = parser.parse_header()
        print(f"Header: {{header}}")
    except Exception as e:
        print(f"Header error: {{e}}")
        header = {{'map_name': 'unknown'}}
    
    # Parse rounds
    try:
        rounds_df = parser.parse_event("round_end")
        if isinstance(rounds_df, list):
            rounds_df = pd.DataFrame(rounds_df)
        print(f"Rounds: {{len(rounds_df)}}")
    except Exception as e:
        print(f"Rounds error: {{e}}")
        rounds_df = pd.DataFrame()
    
    # Parse deaths
    try:
        deaths_df = parser.parse_event("player_death")
        if isinstance(deaths_df, list):
            deaths_df = pd.DataFrame(deaths_df)
        print(f"Deaths: {{len(deaths_df)}}")
    except Exception as e:
        print(f"Deaths error: {{e}}")
        deaths_df = pd.DataFrame()
    
    # Parse bomb events
    try:
        bomb_planted_df = parser.parse_event("bomb_planted")
        if isinstance(bomb_planted_df, list):
            bomb_planted_df = pd.DataFrame(bomb_planted_df)
        print(f"Bomb planted: {{len(bomb_planted_df)}}")
    except Exception as e:
        print(f"Bomb planted error: {{e}}")
        bomb_planted_df = pd.DataFrame()
    
    # Create summary
    if not rounds_df.empty:
        rounds_summary = []
        for idx, round_data in rounds_df.iterrows():
            round_num = round_data.get('round', idx + 1)
            winner = round_data.get('winner', None)
            reason = round_data.get('reason', None)
            
            rounds_summary.append({{
                'round_num': round_num,
                'winning_team': winner,
                'round_end_reason': reason,
                'bomb_planted': len(bomb_planted_df) > 0,
                'demo_type': 'cs2',
                'map_name': header.get('map_name', 'unknown'),
                'parsing_status': 'success'
            }})
        
        df = pd.DataFrame(rounds_summary)
    else:
        df = pd.DataFrame([{{
            'round_num': None,
            'winning_team': None,
            'round_end_reason': None,
            'bomb_planted': None,
            'demo_type': 'cs2',
            'map_name': header.get('map_name', 'unknown'),
            'parsing_status': 'no_rounds_found'
        }}])
    
    # Save results
    stem = "{dem_path.stem}"
    output_dir = "{OUTPUT_DIR}"
    
    # Save rounds
    rounds_csv = f"{{output_dir}}/{{stem}}_rounds.csv"
    df.to_csv(rounds_csv, index=False)
    print(f"SAVED_ROUNDS:{{rounds_csv}}")
    
    # Save deaths if available
    if not deaths_df.empty:
        deaths_csv = f"{{output_dir}}/{{stem}}_deaths.csv"
        deaths_df.to_csv(deaths_csv, index=False)
        print(f"SAVED_DEATHS:{{deaths_csv}}")
    
    print("SUCCESS")
    
except Exception as e:
    print(f"ERROR:{{e}}")
    sys.exit(1)
'''
    
    # Write the temporary script
    with open(temp_script, 'w') as f:
        f.write(script_content)
    
    try:
        # Run the script in a subprocess
        result = subprocess.run([sys.executable, str(temp_script)], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✓ Successfully parsed {dem_path.name}")
            # Parse the output to get file paths
            for line in result.stdout.split('\n'):
                if line.startswith('SAVED_ROUNDS:'):
                    print(f"  → {line.split(':', 1)[1]}")
                elif line.startswith('SAVED_DEATHS:'):
                    print(f"  → {line.split(':', 1)[1]}")
            return True
        else:
            print(f"✗ Failed to parse {dem_path.name}")
            print(f"  Error: {result.stderr}")
            
            # Create error CSV
            df = pd.DataFrame([{
                'round_num': None,
                'winning_team': None,
                'round_end_reason': None,
                'bomb_planted': None,
                'demo_type': 'cs2',
                'map_name': 'unknown',
                'parsing_status': f'error: {result.stderr[:100]}'
            }])
            
            stem = dem_path.stem
            out_csv = OUTPUT_DIR / f"{stem}_rounds.csv"
            df.to_csv(out_csv, index=False)
            print(f"  → Created error CSV: {out_csv}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout parsing {dem_path.name}")
        return False
    except Exception as e:
        print(f"✗ Exception parsing {dem_path.name}: {e}")
        return False
    finally:
        # Clean up temporary script
        if temp_script.exists():
            temp_script.unlink()

def main():
    """Main parsing function"""
    print("=== Robust CS2 Demo Parser ===")
    print(f"Scanning {DEMOS_EXTRACTED_DIR} for demo files...")
    
    if not DEMOS_EXTRACTED_DIR.exists():
        print(f"Error: {DEMOS_EXTRACTED_DIR} does not exist!")
        return
    
    demo_files = []
    
    # Find all .dem files recursively
    for root, dirs, files in os.walk(DEMOS_EXTRACTED_DIR):
        for file in files:
            if file.lower().endswith('.dem'):
                demo_files.append(Path(root) / file)
    
    if not demo_files:
        print("No .dem files found in demos_extracted directory!")
        return
    
    print(f"Found {len(demo_files)} demo files")
    print("\nStarting parsing...")
    
    successful_parses = 0
    failed_parses = 0
    
    for i, demo_file in enumerate(demo_files, 1):
        print(f"\n[{i}/{len(demo_files)}] Processing {demo_file.name}")
        if parse_demo_robust(demo_file):
            successful_parses += 1
        else:
            failed_parses += 1
    
    print(f"\n=== Parsing Complete ===")
    print(f"Successfully parsed: {successful_parses}")
    print(f"Failed to parse: {failed_parses}")
    print(f"Results saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
