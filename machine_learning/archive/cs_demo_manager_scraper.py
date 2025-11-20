#!/usr/bin/env python3
"""
CS Demo Manager scraper - uses CS Demo Manager API and tools
"""

import requests
import json
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm

class CSDemoManagerScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for CS Demo Manager"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        self.session.headers.update(headers)
        
    def try_cs_demo_manager_api(self):
        """Try to access CS Demo Manager API"""
        print("Trying CS Demo Manager API...")
        
        # CS Demo Manager API endpoints
        api_endpoints = [
            "https://cs-demo-manager.com/api/v1/demos",
            "https://cs-demo-manager.com/api/v1/matches",
            "https://cs-demo-manager.com/api/v1/events",
            "https://cs-demo-manager.com/api/v1/teams",
            "https://cs-demo-manager.com/api/v1/players",
            "https://cs-demo-manager.com/api/demos",
            "https://cs-demo-manager.com/api/matches",
            "https://cs-demo-manager.com/api/events",
        ]
        
        results = []
        
        for endpoint in api_endpoints:
            try:
                print(f"Trying {endpoint}...")
                response = self.session.get(endpoint, timeout=30)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results.append({
                            'endpoint': endpoint,
                            'data': data,
                            'status': 'success'
                        })
                        print(f"Successfully got data from {endpoint}")
                    except:
                        results.append({
                            'endpoint': endpoint,
                            'data': response.text[:500],
                            'status': 'non-json'
                        })
                else:
                    print(f"Failed to access {endpoint}: {response.status_code}")
                    
            except Exception as e:
                print(f"Error accessing {endpoint}: {e}")
                continue
                
            time.sleep(random.uniform(1, 3))
        
        return results
    
    def try_cs_demo_manager_web(self):
        """Try to scrape CS Demo Manager website"""
        print("Trying CS Demo Manager website...")
        
        base_url = "https://cs-demo-manager.com"
        endpoints = [
            "/",
            "/downloads",
            "/demos",
            "/matches",
            "/events",
            "/teams",
            "/players",
            "/api",
            "/docs",
        ]
        
        results = []
        
        for endpoint in endpoints:
            try:
                url = base_url + endpoint
                print(f"Trying {url}...")
                response = self.session.get(url, timeout=30)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Look for demo links or API endpoints
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for demo links
                    demo_links = soup.find_all('a', href=True)
                    for link in demo_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['demo', 'download', 'esl', 'pro league', 'match']):
                            if href.startswith('/'):
                                href = urljoin(base_url, href)
                            
                            results.append({
                                'url': href,
                                'text': text,
                                'source': 'CS Demo Manager'
                            })
                            print(f"Found demo link: {text}")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error accessing {url}: {e}")
                continue
        
        return results
    
    def try_leetify_api(self):
        """Try to access Leetify API"""
        print("Trying Leetify API...")
        
        # Leetify API endpoints
        leetify_endpoints = [
            "https://api.leetify.com/api/v1/matches",
            "https://api.leetify.com/api/v1/demos",
            "https://api.leetify.com/api/v1/players",
            "https://api.leetify.com/api/v1/teams",
            "https://leetify.com/api/v1/matches",
            "https://leetify.com/api/v1/demos",
            "https://leetify.com/api/v1/players",
        ]
        
        results = []
        
        for endpoint in leetify_endpoints:
            try:
                print(f"Trying {endpoint}...")
                response = self.session.get(endpoint, timeout=30)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results.append({
                            'endpoint': endpoint,
                            'data': data,
                            'status': 'success'
                        })
                        print(f"Successfully got data from {endpoint}")
                    except:
                        results.append({
                            'endpoint': endpoint,
                            'data': response.text[:500],
                            'status': 'non-json'
                        })
                else:
                    print(f"Failed to access {endpoint}: {response.status_code}")
                    
            except Exception as e:
                print(f"Error accessing {endpoint}: {e}")
                continue
                
            time.sleep(random.uniform(1, 3))
        
        return results
    
    def try_pureskill_api(self):
        """Try to access PureSkill API"""
        print("Trying PureSkill API...")
        
        # PureSkill API endpoints
        pureskill_endpoints = [
            "https://api.pureskill.gg/v1/matches",
            "https://api.pureskill.gg/v1/demos",
            "https://api.pureskill.gg/v1/players",
            "https://api.pureskill.gg/v1/teams",
            "https://pureskill.gg/api/v1/matches",
            "https://pureskill.gg/api/v1/demos",
        ]
        
        results = []
        
        for endpoint in pureskill_endpoints:
            try:
                print(f"Trying {endpoint}...")
                response = self.session.get(endpoint, timeout=30)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results.append({
                            'endpoint': endpoint,
                            'data': data,
                            'status': 'success'
                        })
                        print(f"Successfully got data from {endpoint}")
                    except:
                        results.append({
                            'endpoint': endpoint,
                            'data': response.text[:500],
                            'status': 'non-json'
                        })
                else:
                    print(f"Failed to access {endpoint}: {response.status_code}")
                    
            except Exception as e:
                print(f"Error accessing {endpoint}: {e}")
                continue
                
            time.sleep(random.uniform(1, 3))
        
        return results

def main():
    """Main function"""
    print("="*80)
    print("CS DEMO MANAGER SCRAPER")
    print("="*80)
    
    scraper = CSDemoManagerScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "cs_demo_manager_results.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "cs_demo_manager_results.csv")
    
    print(f"Configuration:")
    print(f"  JSON output: {OUTPUT_FILE}")
    print(f"  CSV output: {CSV_FILE}")
    print("="*80)
    
    try:
        all_results = []
        
        # Try different sources
        print("Testing CS Demo Manager API...")
        cs_demo_results = scraper.try_cs_demo_manager_api()
        all_results.extend(cs_demo_results)
        
        print("Testing CS Demo Manager website...")
        cs_web_results = scraper.try_cs_demo_manager_web()
        all_results.extend(cs_web_results)
        
        print("Testing Leetify API...")
        leetify_results = scraper.try_leetify_api()
        all_results.extend(leetify_results)
        
        print("Testing PureSkill API...")
        pureskill_results = scraper.try_pureskill_api()
        all_results.extend(pureskill_results)
        
        # Save results to JSON
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Save results to CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['endpoint', 'status', 'data_preview'])
            
            for result in all_results:
                if 'endpoint' in result:
                    data_preview = str(result.get('data', ''))[:200] + '...' if len(str(result.get('data', ''))) > 200 else str(result.get('data', ''))
                    writer.writerow([
                        result.get('endpoint', ''),
                        result.get('status', ''),
                        data_preview
                    ])
                else:
                    writer.writerow([
                        result.get('url', ''),
                        'found',
                        result.get('text', '')
                    ])
        
        print(f"\n" + "="*80)
        print("CS DEMO MANAGER SCRAPING COMPLETE")
        print("="*80)
        print(f"Tested {len(all_results)} endpoints")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"CSV saved to: {CSV_FILE}")
        
        # Show successful endpoints
        successful = [r for r in all_results if r.get('status') == 'success']
        if successful:
            print(f"\nSuccessful API endpoints:")
            for result in successful:
                print(f"  - {result['endpoint']}")
        else:
            print("\nNo successful API endpoints found")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
