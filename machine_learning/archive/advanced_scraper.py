#!/usr/bin/env python3
"""
Advanced HLTV scraper with multiple bypass techniques
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm
import json
from fake_useragent import UserAgent

BASE = "https://www.hltv.org"

# Multiple user agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class AdvancedHLTVScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_session()
        
    def setup_session(self):
        """Setup session with advanced headers and settings"""
        # Rotate user agent
        user_agent = random.choice(USER_AGENTS)
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "DNT": "1",
            "Sec-GPC": "1"
        }
        
        self.session.headers.update(headers)
        
        # Configure session with retries
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def get_with_retry(self, url, max_retries=3):
        """Get URL with retry logic and user agent rotation"""
        for attempt in range(max_retries):
            try:
                # Rotate user agent on retry
                if attempt > 0:
                    new_ua = random.choice(USER_AGENTS)
                    self.session.headers.update({"User-Agent": new_ua})
                    time.sleep(random.uniform(2, 5))
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    print(f"403 Forbidden on attempt {attempt + 1}, retrying...")
                    time.sleep(random.uniform(5, 10))
                else:
                    print(f"Status {response.status_code} on attempt {attempt + 1}")
                    
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(3, 7))
        
        return None
    
    def get_esl_matches(self, pages=5):
        """Get ESL Pro League match links"""
        matches = []
        
        print("Fetching ESL Pro League matches...")
        
        for page in range(pages):
            offset = page * 100
            url = f"{BASE}/results?offset={offset}"
            
            print(f"Fetching page {page + 1}/{pages} (offset {offset})")
            
            response = self.get_with_retry(url)
            if not response:
                print(f"Failed to fetch page {page + 1}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for match containers
            match_containers = soup.find_all('div', class_='result-con')
            print(f"Found {len(match_containers)} match containers")
            
            for container in match_containers:
                try:
                    # Check if it's ESL Pro League
                    event_elem = container.find('div', class_='event-name')
                    if not event_elem:
                        continue
                        
                    event_name = event_elem.get_text(strip=True)
                    if 'ESL Pro League' not in event_name:
                        continue
                    
                    # Get match link
                    match_link = container.find('a')
                    if not match_link:
                        continue
                        
                    href = match_link.get('href', '')
                    if not href or '/matches/' not in href:
                        continue
                        
                    if href.startswith('/'):
                        href = BASE + href
                    
                    matches.append({
                        'url': href,
                        'event': event_name,
                        'teams': self.extract_teams_from_container(container)
                    })
                    
                    print(f"Found ESL Pro League match: {href}")
                    
                except Exception as e:
                    print(f"Error processing match container: {e}")
                    continue
            
            # Random delay between pages
            time.sleep(random.uniform(3, 6))
        
        print(f"Total ESL Pro League matches found: {len(matches)}")
        return matches
    
    def extract_teams_from_container(self, container):
        """Extract team names from match container"""
        try:
            team_elems = container.find_all('div', class_='team')
            teams = []
            for team_elem in team_elems:
                team_name = team_elem.get_text(strip=True)
                if team_name:
                    teams.append(team_name)
            return teams
        except:
            return []
    
    def get_match_details(self, match_url):
        """Get detailed match information"""
        print(f"Fetching match details: {match_url}")
        
        response = self.get_with_retry(match_url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            # Extract match ID from URL
            match_id = match_url.split('/')[-2] if '/' in match_url else ''
            
            # Get teams
            teams = soup.find_all('div', class_='teamName')
            team1 = teams[0].get_text(strip=True) if len(teams) > 0 else ''
            team2 = teams[1].get_text(strip=True) if len(teams) > 1 else ''
            
            # Get score
            score_elem = soup.find('div', class_='score')
            score = score_elem.get_text(strip=True) if score_elem else ''
            
            # Get date
            date_elem = soup.find('div', class_='date')
            date = date_elem.get_text(strip=True) if date_elem else ''
            
            # Get players
            players = []
            lineup_links = soup.find_all('a', href=lambda x: x and x.startswith('/player/'))
            for link in lineup_links:
                player_name = link.get_text(strip=True)
                if player_name:
                    players.append(player_name)
            
            # Get demo link
            demo_url = self.extract_demo_link(soup)
            
            return {
                'match_id': match_id,
                'url': match_url,
                'team1': team1,
                'team2': team2,
                'score': score,
                'date': date,
                'players': players,
                'demo_url': demo_url
            }
            
        except Exception as e:
            print(f"Error extracting match details: {e}")
            return None
    
    def extract_demo_link(self, soup):
        """Extract demo download link from match page"""
        try:
            # Try different selectors for demo links
            selectors = [
                '.streams [data-demo-link]',
                '.streams a[data-manuel-download]',
                'a[href*="demo"]',
                '.download-demo'
            ]
            
            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    demo_url = elem.get('data-demo-link') or elem.get('href')
                    if demo_url:
                        if demo_url.startswith('/'):
                            demo_url = BASE + demo_url
                        return demo_url
            
            return None
            
        except Exception as e:
            print(f"Error extracting demo link: {e}")
            return None
    
    def download_demo(self, demo_url, match_info, demos_dir):
        """Download demo file"""
        try:
            os.makedirs(demos_dir, exist_ok=True)
            
            print(f"Downloading demo: {demo_url}")
            
            # Set referer header
            headers = dict(self.session.headers)
            headers['Referer'] = match_info['url']
            
            response = self.session.get(demo_url, headers=headers, stream=True, timeout=300)
            
            if response.status_code != 200:
                print(f"Failed to download demo: HTTP {response.status_code}")
                return None
            
            # Determine filename
            filename = f"{match_info['match_id']}_{match_info['team1']}-vs-{match_info['team2']}.rar"
            filename = "".join(c if c.isalnum() or c in (".", "-", "_") else "_" for c in filename)
            
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
    """Main scraping function"""
    print("="*80)
    print("ADVANCED HLTV SCRAPER - ESL PRO LEAGUE")
    print("="*80)
    
    scraper = AdvancedHLTVScraper()
    
    # Configuration
    PAGES = 5
    MAX_MATCHES = 10
    DOWNLOAD_DEMOS = True
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "demos")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "hltv_matches_advanced.csv")
    
    print(f"Configuration:")
    print(f"  Pages to scrape: {PAGES}")
    print(f"  Max matches: {MAX_MATCHES}")
    print(f"  Download demos: {DOWNLOAD_DEMOS}")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  Demos directory: {DEMOS_DIR}")
    print("="*80)
    
    try:
        # Get match links
        matches = scraper.get_esl_matches(pages=PAGES)
        
        if not matches:
            print("No ESL Pro League matches found!")
            return
        
        # Limit to max matches
        matches = matches[:MAX_MATCHES]
        print(f"\nProcessing {len(matches)} matches...")
        
        all_data = []
        downloaded_demos = []
        
        for i, match in enumerate(matches, 1):
            print(f"\n--- Processing match {i}/{len(matches)} ---")
            
            # Get match details
            match_details = scraper.get_match_details(match['url'])
            if not match_details:
                print(f"Failed to get details for {match['url']}")
                continue
            
            all_data.append(match_details)
            
            # Download demo if available
            if DOWNLOAD_DEMOS and match_details.get('demo_url'):
                demo_path = scraper.download_demo(match_details['demo_url'], match_details, DEMOS_DIR)
                if demo_path:
                    downloaded_demos.append(demo_path)
            
            # Random delay between matches
            time.sleep(random.uniform(5, 10))
        
        # Save data to CSV
        print(f"\nSaving data to {OUTPUT_FILE}")
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['match_id', 'date', 'team1', 'team2', 'score', 'player', 'demo_url'])
            
            for match in all_data:
                for player in match.get('players', []):
                    writer.writerow([
                        match['match_id'],
                        match['date'],
                        match['team1'],
                        match['team2'],
                        match['score'],
                        player,
                        match.get('demo_url', '')
                    ])
        
        print(f"\n" + "="*80)
        print("SCRAPING COMPLETE")
        print("="*80)
        print(f"Processed {len(all_data)} matches")
        print(f"Downloaded {len(downloaded_demos)} demos")
        print(f"Data saved to: {OUTPUT_FILE}")
        print(f"Demos saved to: {DEMOS_DIR}")
        
        if downloaded_demos:
            print(f"\nDownloaded demos:")
            for demo in downloaded_demos:
                print(f"  - {demo}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
