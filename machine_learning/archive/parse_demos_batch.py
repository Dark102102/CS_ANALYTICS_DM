#!/usr/bin/env python3
"""
Batch Demo Parser - Processes demos in smaller batches to avoid timeouts
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
                timeout=120  # 2 minute timeout
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
                timeout=120
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
                timeout=120
            )
            if result.returncode == 0:
                print(f"  ✓ Extracted with 7z")
                return True
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  7z failed: {e}")
        
        print(f"  ✗ Failed to extract {archive_path.name}")
        return False
        
    except Exception as e:
        print(f"  ✗ Error extracting {archive_path.name}: {e}")
        return False

def parse_demo_with_demoparser2(demo_file: Path) -> bool:
    """Parse a single demo file using demoparser2"""
    print(f"  Parsing {demo_file.name}...")
    
    try:
        # Create parser
        parser = DemoParser(str(demo_file))
        
        # Get match info
        match_info = parser.parse("match_info")
        if not match_info.empty:
            print(f"    Match: {match_info.iloc[0].get('map_name', 'Unknown')}")
        
        # Parse rounds
        rounds = parser.parse("rounds")
        if not rounds.empty:
            # Clean up rounds data
            rounds_clean = rounds[['reason', 'round', 'tick', 'winner']].copy()
            rounds_clean = rounds_clean.dropna(subset=['round'])
            
            # Save rounds
            rounds_file = OUTPUT_DIR / f"{demo_file.stem}_rounds.csv"
            rounds_clean.to_csv(rounds_file, index=False)
            print(f"    ✓ Rounds saved: {rounds_file.name} ({len(rounds_clean)} rounds)")
        
        # Parse deaths
        deaths = parser.parse("deaths")
        if not deaths.empty:
            # Save deaths
            deaths_file = OUTPUT_DIR / f"{demo_file.stem}_deaths.csv"
            deaths.to_csv(deaths_file, index=False)
            print(f"    ✓ Deaths saved: {deaths_file.name} ({len(deaths)} deaths)")
        
        print(f"  ✓ Successfully parsed {demo_file.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error parsing {demo_file.name}: {e}")
        return False

def process_demo_batch(batch_size=3):
    """Process demos in batches to avoid timeouts"""
    print("=== Batch Demo Processing ===")
    
    if not DEMOS_DIR.exists():
        print(f"Demos directory {DEMOS_DIR} does not exist!")
        return
    
    # Get all RAR files
    rar_files = list(DEMOS_DIR.glob('*.rar'))
    print(f"Found {len(rar_files)} RAR files to process")
    
    if not rar_files:
        print("No RAR files found!")
        return
    
    # Process in batches
    for batch_start in range(0, len(rar_files), batch_size):
        batch_end = min(batch_start + batch_size, len(rar_files))
        batch_files = rar_files[batch_start:batch_end]
        
        print(f"\n--- Processing Batch {batch_start//batch_size + 1} ({len(batch_files)} files) ---")
        
        # Extract batch
        for rar_file in batch_files:
            if extract_single_archive(rar_file, DEMOS_EXTRACTED_DIR):
                print(f"  ✓ Extracted {rar_file.name}")
            else:
                print(f"  ✗ Failed to extract {rar_file.name}")
        
        # Parse extracted demos from this batch
        print(f"\n--- Parsing Batch {batch_start//batch_size + 1} ---")
        
        # Find .dem files in the extracted directories
        demo_files = []
        for root, dirs, files in os.walk(DEMOS_EXTRACTED_DIR):
            for file in files:
                if file.lower().endswith('.dem'):
                    demo_files.append(Path(root) / file)
        
        # Remove duplicates
        seen_names = set()
        unique_demos = []
        for demo_file in demo_files:
            if demo_file.name not in seen_names:
                seen_names.add(demo_file.name)
                unique_demos.append(demo_file)
        
        print(f"Found {len(unique_demos)} demo files to parse")
        
        # Parse demos
        for demo_file in unique_demos:
            parse_demo_with_demoparser2(demo_file)
        
        # Clean up extracted files to save space
        print(f"Cleaning up extracted files...")
        for rar_file in batch_files:
            extracted_dir = DEMOS_EXTRACTED_DIR / rar_file.stem
            if extracted_dir.exists():
                shutil.rmtree(extracted_dir)
                print(f"  Removed {extracted_dir.name}")
        
        print(f"Batch {batch_start//batch_size + 1} completed")
        
        # Small delay between batches
        if batch_end < len(rar_files):
            print("Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    print("\n=== Processing Complete ===")
    
    # Final summary
    output_files = list(OUTPUT_DIR.glob('*.csv'))
    print(f"Generated {len(output_files)} CSV files:")
    for file in output_files:
        file_size = file.stat().st_size
        print(f"  - {file.name} ({file_size:,} bytes)")

if __name__ == "__main__":
    process_demo_batch(batch_size=2)  # Process 2 demos at a time
