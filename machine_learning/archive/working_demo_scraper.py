#!/usr/bin/env python3
"""
Working Demo Scraper - Downloads CS2 demos from HLTV
Successfully tested with demo ID 100773
"""

import cloudscraper
import re
import os
import time
import json
from urllib.parse import urljoin

def get_recent_matches():
    """Get recent match URLs from HLTV"""
    scraper = cloudscraper.create_scraper()
    
    urls = [
        'https://www.hltv.org/matches',
        'https://www.hltv.org/results',
        'https://www.hltv.org/events/8040/esl-pro-league-season-22',
    ]
    
    all_matches = []
    
    for url in urls:
        try:
            print(f"Getting matches from: {url}")
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 200:
                match_links = re.findall(r'href="(/matches/\d+/[^"]*)"', response.text)
                print(f"Found {len(match_links)} matches")
                
                for match_link in match_links:
                    full_url = f"https://www.hltv.org{match_link}"
                    all_matches.append(full_url)
            else:
                print(f"Failed to get {url}: {response.status_code}")
                
        except Exception as e:
            print(f"Error with {url}: {e}")
    
    # Remove duplicates and limit to recent matches
    unique_matches = list(set(all_matches))[:50]  # Limit to 50 most recent
    print(f"Total unique matches: {len(unique_matches)}")
    return unique_matches

def get_demo_info(match_url):
    """Get demo information from a match page"""
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"Checking match: {match_url}")
        response = scraper.get(match_url, timeout=30)
        
        if response.status_code != 200:
            print(f"Failed to get match: {response.status_code}")
            return None
        
        # Look for demo download link
        demo_links = re.findall(r'href="(/download/demo/\d+)"', response.text)
        
        if demo_links:
            demo_id = demo_links[0].split('/')[-1]
            demo_url = f"https://www.hltv.org{demo_links[0]}"
            
            # Extract match info
            match_id = match_url.split('/')[-2]
            match_name = match_url.split('/')[-1]
            
            return {
                'match_id': match_id,
                'match_name': match_name,
                'match_url': match_url,
                'demo_id': demo_id,
                'demo_url': demo_url
            }
        else:
            print(f"No demo found for match: {match_url}")
            return None
            
    except Exception as e:
        print(f"Error getting demo info for {match_url}: {e}")
        return None

def download_demo(demo_info, output_dir):
    """Download a demo file"""
    scraper = cloudscraper.create_scraper()
    
    try:
        demo_url = demo_info['demo_url']
        demo_id = demo_info['demo_id']
        match_name = demo_info['match_name']
        
        print(f"Downloading demo {demo_id} for match: {match_name}")
        
        response = scraper.get(demo_url, timeout=60, stream=True)
        
        if response.status_code != 200:
            print(f"Failed to download demo {demo_id}: HTTP {response.status_code}")
            return False
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        content_length = response.headers.get('content-length', '0')
        
        print(f"Content-Type: {content_type}, Content-Length: {content_length}")
        
        # Generate filename
        safe_name = re.sub(r'[^\w\-_\.]', '_', match_name)
        filename = f"{safe_name}_demo_{demo_id}.rar"
        filepath = os.path.join(output_dir, filename)
        
        # Download file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        print(f"Downloaded: {filename} ({file_size} bytes)")
        
        if file_size > 1000000:  # More than 1MB
            print(f"SUCCESS: Demo {demo_id} downloaded successfully!")
            return True
        else:
            os.remove(filepath)
            print(f"WARNING: Demo {demo_id} file is too small, removing")
            return False
        
    except Exception as e:
        print(f"Error downloading demo {demo_id}: {e}")
        return False

def main():
    """Main function"""
    print("=" * 80)
    print("WORKING DEMO SCRAPER - CS2 Demo Downloader")
    print("=" * 80)
    
    # Create output directory
    output_dir = "esl_demos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Get recent matches
    print("\n1. Getting recent matches...")
    matches = get_recent_matches()
    
    if not matches:
        print("No matches found!")
        return
    
    print(f"Found {len(matches)} matches to check")
    
    # Get demo info for each match
    print("\n2. Checking matches for demos...")
    demo_infos = []
    
    for i, match_url in enumerate(matches, 1):
        print(f"\n--- Checking match {i}/{len(matches)} ---")
        demo_info = get_demo_info(match_url)
        
        if demo_info:
            demo_infos.append(demo_info)
            print(f"Found demo: {demo_info['demo_id']}")
        
        # Be respectful to the server
        time.sleep(1)
    
    if not demo_infos:
        print("No demos found!")
        return
    
    print(f"\nFound {len(demo_infos)} demos to download")
    
    # Download demos
    print("\n3. Downloading demos...")
    successful_downloads = 0
    
    for i, demo_info in enumerate(demo_infos, 1):
        print(f"\n--- Downloading demo {i}/{len(demo_infos)} ---")
        
        if download_demo(demo_info, output_dir):
            successful_downloads += 1
        
        # Be respectful to the server
        time.sleep(2)
    
    # Save demo info to JSON
    json_file = "demo_info.json"
    with open(json_file, 'w') as f:
        json.dump(demo_infos, f, indent=2)
    
    print(f"\nDemo info saved to: {json_file}")
    
    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Total matches checked: {len(matches)}")
    print(f"Demos found: {len(demo_infos)}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Output directory: {output_dir}")
    
    # List downloaded files
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print(f"\nDownloaded files:")
            for file in files:
                filepath = os.path.join(output_dir, file)
                file_size = os.path.getsize(filepath)
                print(f"  - {file} ({file_size:,} bytes)")

if __name__ == "__main__":
    main()
