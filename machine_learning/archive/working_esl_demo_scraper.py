#!/usr/bin/env python3
"""
Working ESL Pro League Demo Scraper
Targets actual working sources for ESL Pro League demos
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

class WorkingESLDemoScraper:
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
        
    def scrape_hltv_esl_matches(self):
        """Scrape HLTV for ESL Pro League matches"""
        print("Scraping HLTV for ESL Pro League matches...")
        
        try:
            # Try different HLTV endpoints
            endpoints = [
                "https://www.hltv.org/results",
                "https://www.hltv.org/matches",
                "https://www.hltv.org/events",
            ]
            
            all_matches = []
            
            for endpoint in endpoints:
                try:
                    print(f"Trying {endpoint}...")
                    response = self.scraper.get(endpoint, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        # Save HTML for debugging
                        debug_file = f"debug_{endpoint.split('/')[-1]}.html"
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"HTML saved to {debug_file}")
                        
                        # Try to parse with BeautifulSoup
                        try:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Look for match links
                            match_links = soup.find_all('a', href=True)
                            for link in match_links:
                                href = link.get('href', '')
                                text = link.get_text(strip=True)
                                
                                if '/matches/' in href and any(keyword in text.lower() for keyword in ['esl', 'pro league']):
                                    if href.startswith('/'):
                                        href = 'https://www.hltv.org' + href
                                    
                                    all_matches.append({
                                        'url': href,
                                        'text': text,
                                        'source': 'HLTV',
                                        'endpoint': endpoint
                                    })
                                    print(f"Found ESL match: {text}")
                            
                        except Exception as e:
                            print(f"Error parsing HTML: {e}")
                            # Try to find ESL content in raw text
                            if 'esl' in response.text.lower() and 'pro league' in response.text.lower():
                                print("Found ESL Pro League content in raw HTML")
                                all_matches.append({
                                    'url': endpoint,
                                    'text': 'ESL Pro League content found',
                                    'source': 'HLTV',
                                    'endpoint': endpoint
                                })
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {endpoint}: {e}")
                    continue
            
            return all_matches
            
        except Exception as e:
            print(f"Error scraping HLTV: {e}")
            return []
    
    def scrape_esl_official_channels(self):
        """Scrape ESL official channels for demo links"""
        print("Scraping ESL official channels...")
        
        try:
            # ESL official channels
            channels = [
                "https://www.youtube.com/user/esltv",
                "https://www.twitch.tv/esl_csgo",
                "https://pro.eslgaming.com",
                "https://www.esl.com",
            ]
            
            all_content = []
            
            for channel in channels:
                try:
                    print(f"Trying {channel}...")
                    response = self.scraper.get(channel, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for demo-related content
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            
                            if any(keyword in text.lower() for keyword in ['demo', 'download', 'match', 'replay']):
                                if href.startswith('/'):
                                    href = urljoin(channel, href)
                                
                                all_content.append({
                                    'url': href,
                                    'text': text,
                                    'source': 'ESL Official',
                                    'channel': channel
                                })
                                print(f"Found ESL content: {text}")
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {channel}: {e}")
                    continue
            
            return all_content
            
        except Exception as e:
            print(f"Error scraping ESL channels: {e}")
            return []
    
    def scrape_reddit_esl_demos(self):
        """Scrape Reddit for ESL Pro League demo discussions"""
        print("Scraping Reddit for ESL Pro League demos...")
        
        try:
            # Reddit search URLs
            reddit_urls = [
                "https://www.reddit.com/r/GlobalOffensive/search.json?q=ESL+Pro+League+demo&sort=new&t=month",
                "https://www.reddit.com/r/cs2/search.json?q=ESL+Pro+League+demo&sort=new&t=month",
                "https://www.reddit.com/r/GlobalOffensive/search.json?q=demo+download+ESL&sort=new&t=month",
                "https://www.reddit.com/r/cs2/search.json?q=demo+download+ESL&sort=new&t=month",
            ]
            
            all_posts = []
            
            for url in reddit_urls:
                try:
                    print(f"Trying {url}...")
                    response = self.scraper.get(url, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            
                            if 'data' in data and 'children' in data['data']:
                                for post in data['data']['children']:
                                    post_data = post.get('data', {})
                                    title = post_data.get('title', '')
                                    url_text = post_data.get('url', '')
                                    selftext = post_data.get('selftext', '')
                                    
                                    if any(keyword in title.lower() for keyword in ['esl', 'pro league', 'demo', 'download']):
                                        all_posts.append({
                                            'title': title,
                                            'url': url_text,
                                            'selftext': selftext,
                                            'source': 'Reddit'
                                        })
                                        print(f"Found Reddit post: {title}")
                            
                        except json.JSONDecodeError:
                            print(f"Response from {url} is not JSON")
                            continue
                    
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"Error with {url}: {e}")
                    continue
            
            return all_posts
            
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            return []
    
    def scrape_steam_community(self):
        """Scrape Steam community for ESL demo discussions"""
        print("Scraping Steam community for ESL demos...")
        
        try:
            # Steam community URLs
            steam_urls = [
                "https://steamcommunity.com/app/730/discussions/",
                "https://steamcommunity.com/app/730/workshop/",
                "https://steamcommunity.com/app/730/guides/",
            ]
            
            all_content = []
            
            for url in steam_urls:
                try:
                    print(f"Trying {url}...")
                    response = self.scraper.get(url, timeout=30)
                    print(f"Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for ESL-related content
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link.get('href', '')
                            text = link.get_text(strip=True)
                            
                            if any(keyword in text.lower() for keyword in ['esl', 'pro league', 'demo', 'download']):
                                if href.startswith('/'):
                                    href = urljoin('https://steamcommunity.com', href)
                                
                                all_content.append({
                                    'url': href,
                                    'text': text,
                                    'source': 'Steam Community'
                                })
                                print(f"Found Steam content: {text}")
                    
                    time.sleep(random.uniform(3, 6))
                    
                except Exception as e:
                    print(f"Error with {url}: {e}")
                    continue
            
            return all_content
            
        except Exception as e:
            print(f"Error scraping Steam: {e}")
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
    print("WORKING ESL PRO LEAGUE DEMO SCRAPER")
    print("="*80)
    
    scraper = WorkingESLDemoScraper()
    
    # Configuration
    MAX_DEMOS = 10
    DOWNLOAD_DEMOS = True
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "esl_demos")
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "esl_demos_working.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "esl_demos_working.csv")
    
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
        print("\n1. Scraping HLTV for ESL Pro League matches...")
        hltv_matches = scraper.scrape_hltv_esl_matches()
        all_data.extend(hltv_matches)
        print(f"Found {len(hltv_matches)} HLTV matches")
        
        print("\n2. Scraping ESL official channels...")
        esl_content = scraper.scrape_esl_official_channels()
        all_data.extend(esl_content)
        print(f"Found {len(esl_content)} ESL content items")
        
        print("\n3. Scraping Reddit for ESL demos...")
        reddit_posts = scraper.scrape_reddit_esl_demos()
        all_data.extend(reddit_posts)
        print(f"Found {len(reddit_posts)} Reddit posts")
        
        print("\n4. Scraping Steam community...")
        steam_content = scraper.scrape_steam_community()
        all_data.extend(steam_content)
        print(f"Found {len(steam_content)} Steam content items")
        
        # Filter for demo-related content
        demo_items = []
        for item in all_data:
            text = item.get('text', '').lower() + item.get('title', '').lower()
            if any(keyword in text for keyword in ['demo', 'download', '.dem', '.rar']):
                demo_items.append(item)
        
        demo_items = demo_items[:MAX_DEMOS]
        
        print(f"\nFiltered to {len(demo_items)} demo-related items")
        
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
                elif 'title' in demo:
                    base_name = demo['title'].replace(' ', '_').replace('/', '_')
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
            writer.writerow(['source', 'url', 'text', 'title', 'selftext'])
            
            for item in all_data:
                writer.writerow([
                    item.get('source', ''),
                    item.get('url', ''),
                    item.get('text', ''),
                    item.get('title', ''),
                    item.get('selftext', '')
                ])
        
        print(f"\n" + "="*80)
        print("ESL PRO LEAGUE SCRAPING COMPLETE")
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
            print("1. The sources don't have recent ESL Pro League content")
            print("2. The content is behind authentication")
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
