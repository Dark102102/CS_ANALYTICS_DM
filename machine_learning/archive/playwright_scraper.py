#!/usr/bin/env python3
"""
Playwright-based HLTV scraper with stealth capabilities
"""

import asyncio
import csv
import os
import time
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

BASE = "https://www.hltv.org"

class PlaywrightHLTVScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    async def setup_browser(self):
        """Setup browser with stealth settings"""
        playwright = await async_playwright().start()
        
        # Launch browser with stealth settings
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',  # Speed up loading
                '--disable-javascript',  # We'll enable it selectively
            ]
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        # Add stealth scripts
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
        """)
        
        self.page = await self.context.new_page()
        
        # Set extra headers
        await self.page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        
    async def wait_for_cloudflare(self, timeout=30):
        """Wait for Cloudflare challenge to complete"""
        print("Waiting for Cloudflare challenge...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                content = await self.page.content()
                if "Just a moment" not in content and "challenge-platform" not in content:
                    print("Cloudflare challenge completed!")
                    return True
                await asyncio.sleep(2)
            except Exception:
                await asyncio.sleep(2)
        
        print("Cloudflare challenge timeout")
        return False
    
    async def get_esl_matches(self, pages=5):
        """Get ESL Pro League match links"""
        matches = []
        
        print("Fetching ESL Pro League matches...")
        
        for page in range(pages):
            offset = page * 100
            url = f"{BASE}/results?offset={offset}"
            
            print(f"Fetching page {page + 1}/{pages} (offset {offset})")
            
            try:
                # Navigate to results page
                await self.page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Wait for Cloudflare if present
                await self.wait_for_cloudflare()
                
                # Wait for page to load
                await asyncio.sleep(random.uniform(2, 4))
                
                # Get page content
                content = await self.page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
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
                await asyncio.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error fetching page {page + 1}: {e}")
                continue
        
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
    
    async def get_match_details(self, match_url):
        """Get detailed match information"""
        print(f"Fetching match details: {match_url}")
        
        try:
            await self.page.goto(match_url, wait_until='networkidle', timeout=60000)
            await self.wait_for_cloudflare()
            await asyncio.sleep(random.uniform(2, 4))
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
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
    
    async def download_demo(self, demo_url, match_info, demos_dir):
        """Download demo file using requests"""
        try:
            os.makedirs(demos_dir, exist_ok=True)
            
            print(f"Downloading demo: {demo_url}")
            
            # Use requests for file download
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': match_info['url'],
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(demo_url, headers=headers, stream=True, timeout=300)
            
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
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

async def main():
    """Main scraping function"""
    print("="*80)
    print("PLAYWRIGHT HLTV SCRAPER - ESL PRO LEAGUE")
    print("="*80)
    
    scraper = PlaywrightHLTVScraper()
    
    # Configuration
    PAGES = 5
    MAX_MATCHES = 10
    DOWNLOAD_DEMOS = True
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "demos")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "hltv_matches_playwright.csv")
    
    print(f"Configuration:")
    print(f"  Pages to scrape: {PAGES}")
    print(f"  Max matches: {MAX_MATCHES}")
    print(f"  Download demos: {DOWNLOAD_DEMOS}")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  Demos directory: {DEMOS_DIR}")
    print("="*80)
    
    try:
        # Setup browser
        await scraper.setup_browser()
        
        # Get match links
        matches = await scraper.get_esl_matches(pages=PAGES)
        
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
            match_details = await scraper.get_match_details(match['url'])
            if not match_details:
                print(f"Failed to get details for {match['url']}")
                continue
            
            all_data.append(match_details)
            
            # Download demo if available
            if DOWNLOAD_DEMOS and match_details.get('demo_url'):
                demo_path = await scraper.download_demo(match_details['demo_url'], match_details, DEMOS_DIR)
                if demo_path:
                    downloaded_demos.append(demo_path)
            
            # Random delay between matches
            await asyncio.sleep(random.uniform(5, 10))
        
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
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())
