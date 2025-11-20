#!/usr/bin/env python3
"""
ESEA scraper for CS2 demo files
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm

BASE = "https://play.esea.net"

class ESEAScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for ESEA"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.session.headers.update(headers)
        
    def get_demo_list(self, page=1):
        """Get list of demos from ESEA"""
        url = f"{BASE}/index.php?d=view&id=921&s=demos&page={page}"
        
        try:
            print(f"Fetching ESEA demos page {page}...")
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page}: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for demo links
            demo_links = soup.find_all('a', href=lambda x: x and 'demo' in x.lower())
            demos = []
            
            for link in demo_links:
                try:
                    href = link.get('href', '')
                    if href.startswith('/'):
                        href = BASE + href
                    
                    demo_name = link.get_text(strip=True)
                    if demo_name and len(demo_name) > 3:
                        demos.append({
                            'name': demo_name,
                            'url': href
                        })
                        print(f"Found demo: {demo_name}")
                        
                except Exception as e:
                    print(f"Error processing demo link: {e}")
                    continue
            
            return demos
            
        except Exception as e:
            print(f"Error fetching ESEA page {page}: {e}")
            return []
    
    def get_demo_details(self, demo_url):
        """Get details of a specific demo"""
        try:
            response = self.session.get(demo_url, timeout=30)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract demo information
            details = {
                'url': demo_url,
                'title': '',
                'date': '',
                'teams': [],
                'download_url': ''
            }
            
            # Try to extract title
            title_elem = soup.find('h1') or soup.find('title')
            if title_elem:
                details['title'] = title_elem.get_text(strip=True)
            
            # Look for download link
            download_links = soup.find_all('a', href=lambda x: x and ('download' in x.lower() or '.dem' in x.lower()))
            for link in download_links:
                href = link.get('href', '')
                if href.startswith('/'):
                    href = BASE + href
                details['download_url'] = href
                break
            
            return details
            
        except Exception as e:
            print(f"Error getting demo details: {e}")
            return None

def main():
    """Main function"""
    print("="*80)
    print("ESEA DEMO SCRAPER")
    print("="*80)
    
    scraper = ESEAScraper()
    
    # Configuration
    MAX_PAGES = 5
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "esea_demos.csv")
    
    print(f"Configuration:")
    print(f"  Max pages: {MAX_PAGES}")
    print(f"  Output file: {OUTPUT_FILE}")
    print("="*80)
    
    try:
        all_demos = []
        
        for page in range(1, MAX_PAGES + 1):
            demos = scraper.get_demo_list(page)
            all_demos.extend(demos)
            
            if not demos:
                print(f"No more demos found on page {page}")
                break
                
            # Random delay between pages
            time.sleep(random.uniform(2, 4))
        
        print(f"\nFound {len(all_demos)} demos total")
        
        # Get details for each demo
        detailed_demos = []
        for i, demo in enumerate(all_demos[:20], 1):  # Limit to first 20
            print(f"Getting details for demo {i}/{min(20, len(all_demos))}: {demo['name']}")
            details = scraper.get_demo_details(demo['url'])
            if details:
                detailed_demos.append(details)
            time.sleep(random.uniform(1, 3))
        
        # Save to CSV
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'url', 'download_url', 'date', 'teams'])
            
            for demo in detailed_demos:
                writer.writerow([
                    demo.get('title', ''),
                    demo.get('url', ''),
                    demo.get('download_url', ''),
                    demo.get('date', ''),
                    ', '.join(demo.get('teams', []))
                ])
        
        print(f"\n" + "="*80)
        print("ESEA SCRAPING COMPLETE")
        print("="*80)
        print(f"Found {len(detailed_demos)} detailed demos")
        print(f"Data saved to: {OUTPUT_FILE}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
