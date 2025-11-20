#!/usr/bin/env python3
"""
Comprehensive demo scraper using multiple alternative sources
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import os
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
import json

class ComprehensiveDemoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.found_demos = []
        
    def setup_session(self):
        """Setup session with multiple user agents"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.session.headers.update(headers)
        
    def try_demo_archive_sites(self):
        """Try various demo archive sites"""
        print("Trying demo archive sites...")
        
        archive_sites = [
            "https://csgo-demos.com",
            "https://demo.gg", 
            "https://cs2-demos.net",
            "https://pro-demos.com",
            "https://csgo-demo-archive.com",
            "https://demo-archive.net",
            "https://cs2-demo-archive.com"
        ]
        
        for site in archive_sites:
            try:
                print(f"Trying {site}...")
                response = self.session.get(site, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for demo links
                    demo_links = soup.find_all('a', href=True)
                    for link in demo_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['demo', 'download', 'esl', 'pro league', 'cs2', 'csgo']):
                            if href.startswith('/'):
                                href = urljoin(site, href)
                            
                            self.found_demos.append({
                                'name': text,
                                'url': href,
                                'source': site,
                                'type': 'archive_site'
                            })
                            print(f"Found demo: {text}")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error with {site}: {e}")
                continue
    
    def try_community_sites(self):
        """Try community sites for demos"""
        print("Trying community sites...")
        
        community_sites = [
            "https://www.reddit.com/r/GlobalOffensive",
            "https://www.reddit.com/r/cs2",
            "https://www.reddit.com/r/csgo",
            "https://steamcommunity.com/app/730/workshop/",
            "https://steamcommunity.com/app/730/discussions/",
        ]
        
        for site in community_sites:
            try:
                print(f"Trying {site}...")
                response = self.session.get(site, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for demo-related content
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['demo', 'download', 'esl', 'pro league', 'match']):
                            if href.startswith('/'):
                                href = urljoin(site, href)
                            
                            self.found_demos.append({
                                'name': text,
                                'url': href,
                                'source': site,
                                'type': 'community_site'
                            })
                            print(f"Found demo: {text}")
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error with {site}: {e}")
                continue
    
    def try_alternative_hltv_endpoints(self):
        """Try alternative HLTV endpoints"""
        print("Trying alternative HLTV endpoints...")
        
        # Try different HLTV endpoints that might be less protected
        hltv_endpoints = [
            "https://www.hltv.org/matches",
            "https://www.hltv.org/events",
            "https://www.hltv.org/ranking/teams",
            "https://www.hltv.org/stats",
            "https://www.hltv.org/news",
            "https://www.hltv.org/forums",
        ]
        
        for endpoint in hltv_endpoints:
            try:
                print(f"Trying {endpoint}...")
                response = self.session.get(endpoint, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for match links
                    match_links = soup.find_all('a', href=True)
                    for link in match_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if '/matches/' in href and any(keyword in text.lower() for keyword in ['esl', 'pro league']):
                            if href.startswith('/'):
                                href = urljoin('https://www.hltv.org', href)
                            
                            self.found_demos.append({
                                'name': text,
                                'url': href,
                                'source': 'HLTV',
                                'type': 'match_page'
                            })
                            print(f"Found match: {text}")
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
    
    def try_esl_official_sites(self):
        """Try ESL official sites"""
        print("Trying ESL official sites...")
        
        esl_sites = [
            "https://pro.eslgaming.com",
            "https://www.esl.com",
            "https://www.eslgaming.com",
            "https://pro.eslgaming.com/csgo/proleague/",
        ]
        
        for site in esl_sites:
            try:
                print(f"Trying {site}...")
                response = self.session.get(site, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for match or demo links
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['match', 'demo', 'download', 'replay']):
                            if href.startswith('/'):
                                href = urljoin(site, href)
                            
                            self.found_demos.append({
                                'name': text,
                                'url': href,
                                'source': 'ESL',
                                'type': 'official_site'
                            })
                            print(f"Found ESL content: {text}")
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error with {site}: {e}")
                continue
    
    def try_youtube_twitch_sources(self):
        """Try YouTube and Twitch for demo sources"""
        print("Trying YouTube and Twitch sources...")
        
        # YouTube search URLs
        youtube_searches = [
            "https://www.youtube.com/results?search_query=ESL+Pro+League+CS2+demo+download",
            "https://www.youtube.com/results?search_query=CS2+demo+download+ESL",
            "https://www.youtube.com/results?search_query=Counter+Strike+2+demo+ESL+Pro+League",
        ]
        
        for search_url in youtube_searches:
            try:
                print(f"Trying {search_url}...")
                response = self.session.get(search_url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for video links
                    video_links = soup.find_all('a', href=True)
                    for link in video_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if '/watch?v=' in href and any(keyword in text.lower() for keyword in ['demo', 'download', 'esl', 'pro league']):
                            if href.startswith('/'):
                                href = urljoin('https://www.youtube.com', href)
                            
                            self.found_demos.append({
                                'name': text,
                                'url': href,
                                'source': 'YouTube',
                                'type': 'video'
                            })
                            print(f"Found YouTube video: {text}")
                
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"Error with YouTube search: {e}")
                continue
    
    def create_demo_downloader(self):
        """Create a demo downloader for found demos"""
        downloader_code = '''#!/usr/bin/env python3
"""
Demo downloader for found demo sources
"""

import requests
import os
import time
import random
from urllib.parse import urljoin

def download_demo(demo_url, filename, demos_dir="demos"):
    """Download a demo file"""
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

# Example usage with found demos
if __name__ == "__main__":
    # Add your found demo URLs here
    demos = [
        # ("https://example.com/demo1.rar", "demo1.rar"),
        # ("https://example.com/demo2.rar", "demo2.rar"),
    ]
    
    for demo_url, filename in demos:
        download_demo(demo_url, filename)
        time.sleep(random.uniform(2, 5))
'''
        
        with open('demo_downloader_found.py', 'w') as f:
            f.write(downloader_code)
        
        print("Created demo_downloader_found.py for downloading found demos")

def main():
    """Main function"""
    print("="*80)
    print("COMPREHENSIVE DEMO SCRAPER")
    print("="*80)
    
    scraper = ComprehensiveDemoScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "comprehensive_demos.csv")
    JSON_FILE = os.path.join(os.path.dirname(__file__), "comprehensive_demos.json")
    
    print(f"Configuration:")
    print(f"  CSV output: {OUTPUT_FILE}")
    print(f"  JSON output: {JSON_FILE}")
    print("="*80)
    
    try:
        # Try different sources
        print("Starting comprehensive demo search...")
        
        scraper.try_demo_archive_sites()
        scraper.try_community_sites()
        scraper.try_alternative_hltv_endpoints()
        scraper.try_esl_official_sites()
        scraper.try_youtube_twitch_sources()
        
        # Create downloader
        scraper.create_demo_downloader()
        
        # Save results
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'url', 'source', 'type'])
            
            for demo in scraper.found_demos:
                writer.writerow([
                    demo['name'],
                    demo['url'],
                    demo['source'],
                    demo['type']
                ])
        
        with open(JSON_FILE, 'w') as f:
            json.dump(scraper.found_demos, f, indent=2)
        
        print(f"\n" + "="*80)
        print("COMPREHENSIVE SCRAPING COMPLETE")
        print("="*80)
        print(f"Found {len(scraper.found_demos)} potential demo sources")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"JSON saved to: {JSON_FILE}")
        print(f"Downloader created: demo_downloader_found.py")
        
        if scraper.found_demos:
            print(f"\nSample findings:")
            for demo in scraper.found_demos[:5]:
                print(f"  - {demo['name']} ({demo['source']})")
                print(f"    {demo['url']}")
                print()
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
