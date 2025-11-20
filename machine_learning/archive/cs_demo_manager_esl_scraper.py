#!/usr/bin/env python3
"""
CS Demo Manager ESL Pro League Demo Scraper
Uses CS Demo Manager APIs to get 10 latest ESL Pro League demos
"""

import requests
import json
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm
from bs4 import BeautifulSoup

class CSDemoManagerESLScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.base_url = "https://cs-demo-manager.com"
        
    def setup_session(self):
        """Setup session for CS Demo Manager"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://cs-demo-manager.com",
        }
        
        self.session.headers.update(headers)
        
    def get_esl_events(self):
        """Get ESL Pro League events from CS Demo Manager"""
        print("Fetching ESL Pro League events...")
        
        try:
            # Try different event endpoints
            event_endpoints = [
                f"{self.base_url}/api/v1/events",
                f"{self.base_url}/api/events",
                f"{self.base_url}/api/v1/tournaments",
                f"{self.base_url}/api/tournaments",
            ]
            
            for endpoint in event_endpoints:
                try:
                    print(f"Trying {endpoint}...")
                    response = self.session.get(endpoint, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"Successfully got events data from {endpoint}")
                            
                            # Filter for ESL Pro League events
                            esl_events = []
                            if isinstance(data, list):
                                for event in data:
                                    if isinstance(event, dict):
                                        event_name = event.get('name', '').lower()
                                        if 'esl' in event_name and 'pro league' in event_name:
                                            esl_events.append(event)
                            elif isinstance(data, dict) and 'events' in data:
                                for event in data['events']:
                                    if isinstance(event, dict):
                                        event_name = event.get('name', '').lower()
                                        if 'esl' in event_name and 'pro league' in event_name:
                                            esl_events.append(event)
                            
                            print(f"Found {len(esl_events)} ESL Pro League events")
                            return esl_events
                            
                        except json.JSONDecodeError:
                            print(f"Response from {endpoint} is not JSON")
                            continue
                    else:
                        print(f"Failed to access {endpoint}: {response.status_code}")
                        
                except Exception as e:
                    print(f"Error accessing {endpoint}: {e}")
                    continue
                    
                time.sleep(random.uniform(1, 3))
            
            return []
            
        except Exception as e:
            print(f"Error getting ESL events: {e}")
            return []
    
    def get_esl_matches(self, event_ids=None):
        """Get ESL Pro League matches"""
        print("Fetching ESL Pro League matches...")
        
        try:
            # Try different match endpoints
            match_endpoints = [
                f"{self.base_url}/api/v1/matches",
                f"{self.base_url}/api/matches",
                f"{self.base_url}/api/v1/games",
                f"{self.base_url}/api/games",
            ]
            
            for endpoint in match_endpoints:
                try:
                    print(f"Trying {endpoint}...")
                    response = self.session.get(endpoint, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"Successfully got matches data from {endpoint}")
                            
                            # Filter for ESL Pro League matches
                            esl_matches = []
                            if isinstance(data, list):
                                for match in data:
                                    if isinstance(match, dict):
                                        # Check if it's ESL Pro League
                                        event_name = match.get('event', {}).get('name', '').lower() if isinstance(match.get('event'), dict) else ''
                                        match_name = match.get('name', '').lower()
                                        
                                        if 'esl' in event_name or 'esl' in match_name:
                                            if 'pro league' in event_name or 'pro league' in match_name:
                                                esl_matches.append(match)
                            elif isinstance(data, dict) and 'matches' in data:
                                for match in data['matches']:
                                    if isinstance(match, dict):
                                        event_name = match.get('event', {}).get('name', '').lower() if isinstance(match.get('event'), dict) else ''
                                        match_name = match.get('name', '').lower()
                                        
                                        if 'esl' in event_name or 'esl' in match_name:
                                            if 'pro league' in event_name or 'pro league' in match_name:
                                                esl_matches.append(match)
                            
                            print(f"Found {len(esl_matches)} ESL Pro League matches")
                            return esl_matches
                            
                        except json.JSONDecodeError:
                            print(f"Response from {endpoint} is not JSON")
                            continue
                    else:
                        print(f"Failed to access {endpoint}: {response.status_code}")
                        
                except Exception as e:
                    print(f"Error accessing {endpoint}: {e}")
                    continue
                    
                time.sleep(random.uniform(1, 3))
            
            return []
            
        except Exception as e:
            print(f"Error getting ESL matches: {e}")
            return []
    
    def get_esl_demos(self, match_ids=None):
        """Get ESL Pro League demos"""
        print("Fetching ESL Pro League demos...")
        
        try:
            # Try different demo endpoints
            demo_endpoints = [
                f"{self.base_url}/api/v1/demos",
                f"{self.base_url}/api/demos",
                f"{self.base_url}/api/v1/replays",
                f"{self.base_url}/api/replays",
            ]
            
            for endpoint in demo_endpoints:
                try:
                    print(f"Trying {endpoint}...")
                    response = self.session.get(endpoint, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"Successfully got demos data from {endpoint}")
                            
                            # Filter for ESL Pro League demos
                            esl_demos = []
                            if isinstance(data, list):
                                for demo in data:
                                    if isinstance(demo, dict):
                                        # Check if it's ESL Pro League
                                        event_name = demo.get('event', {}).get('name', '').lower() if isinstance(demo.get('event'), dict) else ''
                                        match_name = demo.get('match', {}).get('name', '').lower() if isinstance(demo.get('match'), dict) else ''
                                        demo_name = demo.get('name', '').lower()
                                        
                                        if any('esl' in name for name in [event_name, match_name, demo_name]):
                                            if any('pro league' in name for name in [event_name, match_name, demo_name]):
                                                esl_demos.append(demo)
                            elif isinstance(data, dict) and 'demos' in data:
                                for demo in data['demos']:
                                    if isinstance(demo, dict):
                                        event_name = demo.get('event', {}).get('name', '').lower() if isinstance(demo.get('event'), dict) else ''
                                        match_name = demo.get('match', {}).get('name', '').lower() if isinstance(demo.get('match'), dict) else ''
                                        demo_name = demo.get('name', '').lower()
                                        
                                        if any('esl' in name for name in [event_name, match_name, demo_name]):
                                            if any('pro league' in name for name in [event_name, match_name, demo_name]):
                                                esl_demos.append(demo)
                            
                            print(f"Found {len(esl_demos)} ESL Pro League demos")
                            return esl_demos
                            
                        except json.JSONDecodeError:
                            print(f"Response from {endpoint} is not JSON")
                            continue
                    else:
                        print(f"Failed to access {endpoint}: {response.status_code}")
                        
                except Exception as e:
                    print(f"Error accessing {endpoint}: {e}")
                    continue
                    
                time.sleep(random.uniform(1, 3))
            
            return []
            
        except Exception as e:
            print(f"Error getting ESL demos: {e}")
            return []
    
    def scrape_website_directly(self):
        """Scrape CS Demo Manager website directly for ESL content"""
        print("Scraping CS Demo Manager website directly...")
        
        try:
            # Try different pages
            pages = [
                f"{self.base_url}/",
                f"{self.base_url}/demos",
                f"{self.base_url}/matches",
                f"{self.base_url}/events",
                f"{self.base_url}/tournaments",
            ]
            
            all_content = []
            
            for page in pages:
                try:
                    print(f"Scraping {page}...")
                    response = self.session.get(page, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for ESL Pro League content
                        esl_links = soup.find_all('a', href=True)
                        for link in esl_links:
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            
                            if any(keyword in text.lower() for keyword in ['esl', 'pro league']):
                                if href.startswith('/'):
                                    href = urljoin(self.base_url, href)
                                
                                all_content.append({
                                    'url': href,
                                    'text': text,
                                    'page': page
                                })
                                print(f"Found ESL content: {text}")
                        
                        # Look for demo download links
                        demo_links = soup.find_all('a', href=True)
                        for link in demo_links:
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            
                            if any(keyword in text.lower() for keyword in ['demo', 'download', '.dem', '.rar']):
                                if href.startswith('/'):
                                    href = urljoin(self.base_url, href)
                                
                                all_content.append({
                                    'url': href,
                                    'text': text,
                                    'page': page,
                                    'type': 'demo'
                                })
                                print(f"Found demo link: {text}")
                    
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"Error scraping {page}: {e}")
                    continue
            
            return all_content
            
        except Exception as e:
            print(f"Error scraping website: {e}")
            return []
    
    def download_demo(self, demo_url, filename, demos_dir):
        """Download a demo file"""
        try:
            os.makedirs(demos_dir, exist_ok=True)
            
            print(f"Downloading {filename}...")
            
            # Set referer header
            headers = dict(self.session.headers)
            headers['Referer'] = self.base_url
            
            response = self.session.get(demo_url, headers=headers, stream=True, timeout=300)
            
            if response.status_code != 200:
                print(f"Failed to download demo: HTTP {response.status_code}")
                return None
            
            filepath = os.path.join(demos_dir, filename)
            
            # Download file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Check file size
            file_size = os.path.getsize(filepath)
            if file_size < 1000000:  # Less than 1MB
                os.remove(filepath)
                print(f"Downloaded file too small ({file_size} bytes), removing")
                return None
            
            print(f"Downloaded demo: {filepath} ({file_size} bytes)")
            return filepath
            
        except Exception as e:
            print(f"Error downloading demo: {e}")
            return None

def main():
    """Main function"""
    print("="*80)
    print("CS DEMO MANAGER ESL PRO LEAGUE SCRAPER")
    print("="*80)
    
    scraper = CSDemoManagerESLScraper()
    
    # Configuration
    MAX_DEMOS = 10
    DOWNLOAD_DEMOS = True
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "esl_demos")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "esl_demos_data.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "esl_demos_data.csv")
    
    print(f"Configuration:")
    print(f"  Max demos: {MAX_DEMOS}")
    print(f"  Download demos: {DOWNLOAD_DEMOS}")
    print(f"  Demos directory: {DEMOS_DIR}")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  CSV file: {CSV_FILE}")
    print("="*80)
    
    try:
        all_data = []
        downloaded_demos = []
        
        # Get ESL events
        print("\n1. Getting ESL Pro League events...")
        events = scraper.get_esl_events()
        if events:
            all_data.extend(events)
            print(f"Found {len(events)} ESL Pro League events")
        
        # Get ESL matches
        print("\n2. Getting ESL Pro League matches...")
        matches = scraper.get_esl_matches()
        if matches:
            all_data.extend(matches)
            print(f"Found {len(matches)} ESL Pro League matches")
        
        # Get ESL demos
        print("\n3. Getting ESL Pro League demos...")
        demos = scraper.get_esl_demos()
        if demos:
            all_data.extend(demos)
            print(f"Found {len(demos)} ESL Pro League demos")
        
        # Scrape website directly
        print("\n4. Scraping website directly...")
        website_content = scraper.scrape_website_directly()
        if website_content:
            all_data.extend(website_content)
            print(f"Found {len(website_content)} website content items")
        
        # Filter and limit to latest demos
        demo_items = [item for item in all_data if item.get('type') == 'demo' or 'demo' in str(item).lower()]
        demo_items = demo_items[:MAX_DEMOS]
        
        print(f"\nFiltered to {len(demo_items)} demo items")
        
        # Download demos if requested
        if DOWNLOAD_DEMOS and demo_items:
            print(f"\n5. Downloading {len(demo_items)} demos...")
            for i, demo in enumerate(demo_items, 1):
                print(f"\n--- Downloading demo {i}/{len(demo_items)} ---")
                
                demo_url = demo.get('url', '')
                if not demo_url:
                    continue
                
                # Generate filename
                filename = f"esl_demo_{i:02d}.rar"
                if 'text' in demo:
                    # Use text as filename base
                    base_name = demo['text'].replace(' ', '_').replace('/', '_')
                    filename = f"esl_{base_name}.rar"
                
                # Download demo
                demo_path = scraper.download_demo(demo_url, filename, DEMOS_DIR)
                if demo_path:
                    downloaded_demos.append(demo_path)
                
                time.sleep(random.uniform(3, 6))
        
        # Save data to JSON
        print(f"\nSaving data to {OUTPUT_FILE}")
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        # Save data to CSV
        print(f"Saving data to {CSV_FILE}")
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'url', 'text', 'page', 'data'])
            
            for item in all_data:
                writer.writerow([
                    item.get('type', ''),
                    item.get('url', ''),
                    item.get('text', ''),
                    item.get('page', ''),
                    str(item)[:200] + '...' if len(str(item)) > 200 else str(item)
                ])
        
        print(f"\n" + "="*80)
        print("CS DEMO MANAGER SCRAPING COMPLETE")
        print("="*80)
        print(f"Found {len(all_data)} total items")
        print(f"Downloaded {len(downloaded_demos)} demos")
        print(f"Data saved to: {OUTPUT_FILE}")
        print(f"CSV saved to: {CSV_FILE}")
        print(f"Demos saved to: {DEMOS_DIR}")
        
        if downloaded_demos:
            print(f"\nDownloaded demos:")
            for demo in downloaded_demos:
                print(f"  - {demo}")
        
        if not downloaded_demos and not all_data:
            print("\nNo ESL Pro League content found. This might mean:")
            print("1. CS Demo Manager doesn't have ESL Pro League content")
            print("2. The API structure is different than expected")
            print("3. Authentication might be required")
            print("\nTry the manual collection methods or use your existing 3 demos.")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
