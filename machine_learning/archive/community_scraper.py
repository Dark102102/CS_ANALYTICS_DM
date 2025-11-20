#!/usr/bin/env python3
"""
Community demo scraper for alternative sources
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm
import re

class CommunityDemoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for community sites"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        self.session.headers.update(headers)
        
    def scrape_kick_lv(self):
        """Scrape KICK.LV for demos"""
        print("Scraping KICK.LV...")
        url = "https://www.kick.lv/demo_war3"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                print(f"Failed to access KICK.LV: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            demos = []
            
            # Look for demo links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if any(keyword in text.lower() for keyword in ['demo', 'cs', 'cs2', 'csgo', 'match']):
                    if href.startswith('/'):
                        href = urljoin(url, href)
                    
                    demos.append({
                        'name': text,
                        'url': href,
                        'source': 'KICK.LV'
                    })
                    print(f"Found demo: {text}")
            
            return demos
            
        except Exception as e:
            print(f"Error scraping KICK.LV: {e}")
            return []
    
    def scrape_reddit_demos(self):
        """Scrape Reddit for demo links"""
        print("Searching Reddit for demo links...")
        
        # Reddit search URLs for CS2 demos
        reddit_urls = [
            "https://www.reddit.com/r/GlobalOffensive/search.json?q=demo%20download&sort=new&t=month",
            "https://www.reddit.com/r/cs2/search.json?q=demo%20download&sort=new&t=month",
            "https://www.reddit.com/r/GlobalOffensive/search.json?q=ESL%20Pro%20League%20demo&sort=new&t=month"
        ]
        
        demos = []
        
        for url in reddit_urls:
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data and 'children' in data['data']:
                        for post in data['data']['children']:
                            post_data = post.get('data', {})
                            title = post_data.get('title', '')
                            url_text = post_data.get('url', '')
                            
                            if any(keyword in title.lower() for keyword in ['demo', 'download', 'esl', 'pro league']):
                                demos.append({
                                    'name': title,
                                    'url': url_text,
                                    'source': 'Reddit'
                                })
                                print(f"Found Reddit post: {title}")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error scraping Reddit: {e}")
                continue
        
        return demos
    
    def scrape_demo_archive_sites(self):
        """Scrape various demo archive sites"""
        print("Scraping demo archive sites...")
        
        # List of potential demo archive sites
        archive_sites = [
            "https://csgo-demos.com",
            "https://demo.gg",
            "https://cs2-demos.net",
            "https://pro-demos.com"
        ]
        
        demos = []
        
        for site in archive_sites:
            try:
                print(f"Trying {site}...")
                response = self.session.get(site, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for demo links
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['demo', 'download', 'esl', 'pro league']):
                            if href.startswith('/'):
                                href = urljoin(site, href)
                            
                            demos.append({
                                'name': text,
                                'url': href,
                                'source': site
                            })
                            print(f"Found demo: {text}")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error scraping {site}: {e}")
                continue
        
        return demos
    
    def search_github_demos(self):
        """Search GitHub for demo repositories"""
        print("Searching GitHub for demo repositories...")
        
        github_urls = [
            "https://api.github.com/search/repositories?q=cs2+demo+esl+pro+league",
            "https://api.github.com/search/repositories?q=csgo+demo+download",
            "https://api.github.com/search/repositories?q=counter+strike+demo+archive"
        ]
        
        demos = []
        
        for url in github_urls:
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'items' in data:
                        for repo in data['items'][:10]:  # Limit to first 10
                            repo_name = repo.get('name', '')
                            repo_url = repo.get('html_url', '')
                            description = repo.get('description', '')
                            
                            if any(keyword in (repo_name + ' ' + description).lower() for keyword in ['demo', 'cs2', 'csgo', 'esl']):
                                demos.append({
                                    'name': repo_name,
                                    'url': repo_url,
                                    'source': 'GitHub',
                                    'description': description
                                })
                                print(f"Found GitHub repo: {repo_name}")
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Error searching GitHub: {e}")
                continue
        
        return demos

def main():
    """Main function"""
    print("="*80)
    print("COMMUNITY DEMO SCRAPER")
    print("="*80)
    
    scraper = CommunityDemoScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "community_demos.csv")
    
    print(f"Configuration:")
    print(f"  Output file: {OUTPUT_FILE}")
    print("="*80)
    
    try:
        all_demos = []
        
        # Scrape different sources
        print("Scraping KICK.LV...")
        kick_demos = scraper.scrape_kick_lv()
        all_demos.extend(kick_demos)
        
        print("Searching Reddit...")
        reddit_demos = scraper.scrape_reddit_demos()
        all_demos.extend(reddit_demos)
        
        print("Scraping demo archive sites...")
        archive_demos = scraper.scrape_demo_archive_sites()
        all_demos.extend(archive_demos)
        
        print("Searching GitHub...")
        github_demos = scraper.search_github_demos()
        all_demos.extend(github_demos)
        
        print(f"\nFound {len(all_demos)} demos total")
        
        # Save to CSV
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'url', 'source', 'description'])
            
            for demo in all_demos:
                writer.writerow([
                    demo.get('name', ''),
                    demo.get('url', ''),
                    demo.get('source', ''),
                    demo.get('description', '')
                ])
        
        print(f"\n" + "="*80)
        print("COMMUNITY SCRAPING COMPLETE")
        print("="*80)
        print(f"Found {len(all_demos)} demos from community sources")
        print(f"Data saved to: {OUTPUT_FILE}")
        
        if all_demos:
            print(f"\nSample demos found:")
            for demo in all_demos[:5]:
                print(f"  - {demo['name']} ({demo['source']})")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
