#!/usr/bin/env python3
"""
Manual demo finder - provides instructions and tools for manually finding ESL Pro League demos
"""

import os
import csv
import requests
from urllib.parse import urljoin

def create_manual_demo_guide():
    """Create a guide for manually finding ESL Pro League demos"""
    
    guide = """
# Manual ESL Pro League Demo Finder Guide

Since automated scraping is being blocked by Cloudflare, here's how to manually find and download ESL Pro League demos:

## Method 1: Direct HLTV Access
1. Open a web browser and go to https://www.hltv.org/results
2. Look for ESL Pro League matches (usually marked with "ESL Pro League" in the event name)
3. Click on a match to go to the match page
4. Look for a "Download Demo" button or link
5. Right-click and "Save link as" to download the demo file

## Method 2: ESL Official Website
1. Go to https://pro.eslgaming.com/
2. Navigate to CS2/CS:GO section
3. Look for recent ESL Pro League matches
4. Check if demo files are available for download

## Method 3: Community Sources
1. Check Reddit r/GlobalOffensive for demo sharing threads
2. Look for demo sharing Discord servers
3. Check Steam community forums for demo links

## Method 4: Alternative Demo Sites
1. Check if there are alternative demo hosting sites
2. Look for torrent sites that host CS2 demos
3. Check if any YouTubers or streamers have shared demo links

## Demo File Information
- ESL Pro League demos are typically .rar or .zip files
- File sizes are usually 100MB - 1GB per demo
- Demos contain all rounds of a match
- You'll need to extract them before parsing

## Current Status
- You have 3 valid demo files from previous downloads
- You have match data for 10 ESL Pro League games
- You can proceed with parsing the existing demos while working on getting more

## Next Steps
1. Try the manual methods above to get more recent demos
2. Use the existing 3 demo files for initial analysis
3. Parse the demos using the existing parsing scripts
4. Continue to collect more demos as they become available
"""
    
    with open("MANUAL_DEMO_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("Created MANUAL_DEMO_GUIDE.md with instructions for manually finding demos")

def create_demo_downloader():
    """Create a simple demo downloader for known demo URLs"""
    
    code = '''#!/usr/bin/env python3
"""
Simple demo downloader for known demo URLs
"""

import requests
import os
from urllib.parse import urljoin

def download_demo(demo_url, filename, demos_dir="demos"):
    """Download a demo file from a known URL"""
    try:
        os.makedirs(demos_dir, exist_ok=True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        print(f"Downloading {filename}...")
        response = requests.get(demo_url, headers=headers, stream=True, timeout=300)
        
        if response.status_code == 200:
            filepath = os.path.join(demos_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(filepath)
            print(f"Downloaded {filename} ({file_size} bytes)")
            return filepath
        else:
            print(f"Failed to download {filename}: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    # Add known demo URLs here
    demos = [
        # ("https://example.com/demo1.rar", "match1.rar"),
        # ("https://example.com/demo2.rar", "match2.rar"),
    ]
    
    for demo_url, filename in demos:
        download_demo(demo_url, filename)
'''
    
    with open("demo_downloader.py", "w") as f:
        f.write(code)
    
    print("Created demo_downloader.py for downloading known demo URLs")

def create_recent_matches_template():
    """Create a template for recent ESL Pro League matches"""
    
    # Recent ESL Pro League matches (you can update these manually)
    recent_matches = [
        {
            'match_id': '2386001',
            'date': '15 Dec 2024',
            'team1': 'FaZe',
            'team2': 'Vitality',
            'score': '2:1',
            'map': 'Inferno',
            'demo_url': '',  # Add demo URL when found
            'status': 'Need to find demo'
        },
        {
            'match_id': '2386002',
            'date': '15 Dec 2024',
            'team1': 'MOUZ',
            'team2': 'Spirit',
            'score': '2:0',
            'map': 'Ancient',
            'demo_url': '',
            'status': 'Need to find demo'
        },
        {
            'match_id': '2386003',
            'date': '14 Dec 2024',
            'team1': 'G2',
            'team2': 'Falcons',
            'score': '1:2',
            'map': 'Mirage',
            'demo_url': '',
            'status': 'Need to find demo'
        },
        {
            'match_id': '2386004',
            'date': '14 Dec 2024',
            'team1': 'Natus Vincere',
            'team2': 'FURIA',
            'score': '2:1',
            'map': 'Overpass',
            'demo_url': '',
            'status': 'Need to find demo'
        },
        {
            'match_id': '2386005',
            'date': '13 Dec 2024',
            'team1': 'Aurora',
            'team2': '3DMAX',
            'score': '2:0',
            'map': 'Dust2',
            'demo_url': '',
            'status': 'Need to find demo'
        }
    ]
    
    # Save to CSV
    with open('recent_esl_matches_template.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['match_id', 'date', 'team1', 'team2', 'score', 'map', 'demo_url', 'status'])
        
        for match in recent_matches:
            writer.writerow([
                match['match_id'],
                match['date'],
                match['team1'],
                match['team2'],
                match['score'],
                match['map'],
                match['demo_url'],
                match['status']
            ])
    
    print("Created recent_esl_matches_template.csv with recent match information")

def main():
    """Main function"""
    print("="*80)
    print("MANUAL DEMO FINDER - ESL PRO LEAGUE")
    print("="*80)
    
    print("Creating manual demo finding tools...")
    
    # Create guide
    create_manual_demo_guide()
    
    # Create downloader
    create_demo_downloader()
    
    # Create template
    create_recent_matches_template()
    
    print("\n" + "="*80)
    print("MANUAL TOOLS CREATED")
    print("="*80)
    print("Files created:")
    print("  - MANUAL_DEMO_GUIDE.md: Instructions for manually finding demos")
    print("  - demo_downloader.py: Simple downloader for known demo URLs")
    print("  - recent_esl_matches_template.csv: Template for recent matches")
    print("\nNext steps:")
    print("  1. Read MANUAL_DEMO_GUIDE.md for instructions")
    print("  2. Manually find demo URLs and add them to demo_downloader.py")
    print("  3. Update recent_esl_matches_template.csv with found demo URLs")
    print("  4. Use the existing 3 demo files for initial analysis")
    print("  5. Continue collecting more demos as they become available")

if __name__ == "__main__":
    main()
