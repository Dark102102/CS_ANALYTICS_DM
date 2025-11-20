#!/usr/bin/env python3
"""
Targeted CS2 Demo Scraper
Focuses on actual CS2 demo sources and files
"""

import cloudscraper
from bs4 import BeautifulSoup
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm
import json
import re

class TargetedCS2DemoScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'mobile': False
            }
        )
        self.setup_headers()
        
    def setup_headers(self):
        """Setup headers for the scraper"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.scraper.headers.update(headers)
        
    def scrape_hltv_direct_demo_links(self):
        """Scrape HLTV for direct demo download links"""
        print("Scraping HLTV for direct demo links...")
        
        try:
            # Try to find demo download pages
            demo_pages = [
                "https://www.hltv.org/matches",
                "https://www.hltv.org/results",
                "https://www.hltv.org/events",
            ]
            
            all_demos = []
            
            for page in demo_pages:
                try:
                    print(f"Trying {page}...")
                    response = self.scraper.get(page, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        # Look for demo download links in the HTML
                        demo_links = re.findall(r'href="([^"]*\.(?:dem|rar|zip)[^"]*)"', response.text)
                        for link in demo_links:
                            if link.startswith('/'):
                                link = 'https://www.hltv.org' + link
                            
                            all_demos.append({
                                'url': link,
                                'source': 'HLTV',
                                'page': page,
                                'type': 'direct_demo'
                            })
                            print(f"Found demo link: {link}")
                        
                        # Also look for match pages that might have demos
                        match_links = re.findall(r'href="(/matches/\d+[^"]*)"', response.text)
                        for link in match_links[:10]:  # Limit to first 10
                            match_url = 'https://www.hltv.org' + link
                            all_demos.append({
                                'url': match_url,
                                'source': 'HLTV',
                                'page': page,
                                'type': 'match_page'
                            })
                            print(f"Found match page: {match_url}")
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {page}: {e}")
                    continue
            
            return all_demos
            
        except Exception as e:
            print(f"Error scraping HLTV: {e}")
            return []
    
    def scrape_github_cs2_demo_repos(self):
        """Scrape GitHub for CS2 demo repositories"""
        print("Scraping GitHub for CS2 demo repositories...")
        
        try:
            # GitHub search URLs for CS2 demos
            github_urls = [
                "https://api.github.com/search/repositories?q=cs2+demo+download",
                "https://api.github.com/search/repositories?q=csgo+demo+download",
                "https://api.github.com/search/repositories?q=counter+strike+demo",
                "https://api.github.com/search/repositories?q=esl+pro+league+demo",
            ]
            
            all_repos = []
            
            for url in github_urls:
                try:
                    print(f"Trying {url}...")
                    response = self.scraper.get(url, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            
                            if 'items' in data:
                                for repo in data['items'][:5]:  # Limit to first 5
                                    repo_name = repo.get('name', '')
                                    repo_url = repo.get('html_url', '')
                                    description = repo.get('description', '')
                                    
                                    all_repos.append({
                                        'name': repo_name,
                                        'url': repo_url,
                                        'description': description,
                                        'source': 'GitHub'
                                    })
                                    print(f"Found GitHub repo: {repo_name}")
                            
                        except json.JSONDecodeError:
                            print(f"Response from {url} is not JSON")
                            continue
                    
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"Error with {url}: {e}")
                    continue
            
            return all_repos
            
        except Exception as e:
            print(f"Error scraping GitHub: {e}")
            return []
    
    def scrape_steam_workshop_cs2(self):
        """Scrape Steam Workshop for CS2 content"""
        print("Scraping Steam Workshop for CS2 content...")
        
        try:
            # Steam Workshop URLs
            workshop_urls = [
                "https://steamcommunity.com/app/730/workshop/",
                "https://steamcommunity.com/app/730/workshop/?browsesort=trend&section=readytouseitems&actualsort=trend&p=1&days=7",
                "https://steamcommunity.com/app/730/workshop/?browsesort=trend&section=readytouseitems&actualsort=trend&p=1&days=30",
            ]
            
            all_content = []
            
            for url in workshop_urls:
                try:
                    print(f"Trying {url}...")
                    response = self.scraper.get(url, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for workshop items
                        workshop_links = soup.find_all('a', href=True)
                        for link in workshop_links:
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            
                            if '/sharedfiles/filedetails/' in href:
                                if href.startswith('/'):
                                    href = urljoin('https://steamcommunity.com', href)
                                
                                all_content.append({
                                    'url': href,
                                    'text': text,
                                    'source': 'Steam Workshop'
                                })
                                print(f"Found workshop item: {text}")
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {url}: {e}")
                    continue
            
            return all_content
            
        except Exception as e:
            print(f"Error scraping Steam Workshop: {e}")
            return []
    
    def scrape_alternative_demo_sites(self):
        """Scrape alternative demo sites"""
        print("Scraping alternative demo sites...")
        
        try:
            # Alternative demo sites
            demo_sites = [
                "https://csgo-demos.com",
                "https://demo.gg",
                "https://cs2-demos.net",
                "https://pro-demos.com",
            ]
            
            all_demos = []
            
            for site in demo_sites:
                try:
                    print(f"Trying {site}...")
                    response = self.scraper.get(site, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        # Look for demo links
                        demo_links = re.findall(r'href="([^"]*\.(?:dem|rar|zip)[^"]*)"', response.text)
                        for link in demo_links:
                            if link.startswith('/'):
                                link = urljoin(site, link)
                            
                            all_demos.append({
                                'url': link,
                                'source': site,
                                'type': 'direct_demo'
                            })
                            print(f"Found demo link: {link}")
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {site}: {e}")
                    continue
            
            return all_demos
            
        except Exception as e:
            print(f"Error scraping alternative sites: {e}")
            return []
    
    def download_demo(self, demo_url, filename, demos_dir):
        """Download a demo file"""
        try:
            os.makedirs(demos_dir, exist_ok=True)
            
            print(f"Downloading {filename}...")
            
            # Set referer header
            headers = dict(self.scraper.headers)
            headers['Referer'] = demo_url
            
            response = self.scraper.get(demo_url, headers=headers, stream=True, timeout=300)
            
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
    print("TARGETED CS2 DEMO SCRAPER")
    print("="*80)
    
    scraper = TargetedCS2DemoScraper()
    
    # Configuration
    MAX_DEMOS = 10
    DOWNLOAD_DEMOS = True
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "cs2_demos")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "cs2_demos_targeted.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "cs2_demos_targeted.csv")
    
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
        
        # Scrape different sources
        print("\n1. Scraping HLTV for direct demo links...")
        hltv_demos = scraper.scrape_hltv_direct_demo_links()
        all_data.extend(hltv_demos)
        print(f"Found {len(hltv_demos)} HLTV demos")
        
        print("\n2. Scraping GitHub for CS2 demo repos...")
        github_repos = scraper.scrape_github_cs2_demo_repos()
        all_data.extend(github_repos)
        print(f"Found {len(github_repos)} GitHub repos")
        
        print("\n3. Scraping Steam Workshop for CS2 content...")
        steam_content = scraper.scrape_steam_workshop_cs2()
        all_data.extend(steam_content)
        print(f"Found {len(steam_content)} Steam content items")
        
        print("\n4. Scraping alternative demo sites...")
        alt_demos = scraper.scrape_alternative_demo_sites()
        all_data.extend(alt_demos)
        print(f"Found {len(alt_demos)} alternative demos")
        
        # Filter for actual demo files
        demo_files = [item for item in all_data if item.get('type') == 'direct_demo']
        demo_files = demo_files[:MAX_DEMOS]
        
        print(f"\nFiltered to {len(demo_files)} actual demo files")
        
        # Download demos if requested
        if DOWNLOAD_DEMOS and demo_files:
            print(f"\n5. Downloading {len(demo_files)} demos...")
            for i, demo in enumerate(demo_files, 1):
                print(f"\n--- Downloading demo {i}/{len(demo_files)} ---")
                
                demo_url = demo.get('url', '')
                if not demo_url:
                    continue
                
                # Generate filename
                filename = f"cs2_demo_{i:02d}.rar"
                if 'text' in demo:
                    base_name = demo['text'].replace(' ', '_').replace('/', '_')
                    filename = f"cs2_{base_name}.rar"
                
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
            writer.writerow(['source', 'url', 'text', 'type', 'description'])
            
            for item in all_data:
                writer.writerow([
                    item.get('source', ''),
                    item.get('url', ''),
                    item.get('text', ''),
                    item.get('type', ''),
                    item.get('description', '')
                ])
        
        print(f"\n" + "="*80)
        print("TARGETED CS2 DEMO SCRAPING COMPLETE")
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
            print("\nNo CS2 demo content found. This might mean:")
            print("1. The sources don't have accessible CS2 demos")
            print("2. The demo links are behind authentication")
            print("3. The scraping methods need adjustment")
            print("\nTry the manual collection methods or use your existing 3 demos.")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
