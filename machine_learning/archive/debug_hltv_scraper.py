#!/usr/bin/env python3
"""
Debug HLTV scraper to see what's actually being returned
"""

import cloudscraper
from bs4 import BeautifulSoup
import os

def debug_hltv_scraper():
    """Debug what HLTV is actually returning"""
    print("Debugging HLTV scraper...")
    
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'mobile': False
        }
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    
    scraper.headers.update(headers)
    
    # Test different endpoints
    endpoints = [
        "https://www.hltv.org/results",
        "https://www.hltv.org/matches",
        "https://www.hltv.org/events",
        "https://www.hltv.org/ranking/teams",
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting {endpoint}...")
        
        try:
            response = scraper.get(endpoint, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Content length: {len(response.text)}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for different container types
                containers = [
                    ('div.result-con', 'result-con'),
                    ('div.result', 'result'),
                    ('div.match', 'match'),
                    ('div.event', 'event'),
                    ('div.team', 'team'),
                    ('div.teamName', 'teamName'),
                    ('div.event-name', 'event-name'),
                ]
                
                for selector, name in containers:
                    elements = soup.select(selector)
                    print(f"  {name}: {len(elements)} found")
                    
                    if elements:
                        # Show first few elements
                        for i, elem in enumerate(elements[:3]):
                            print(f"    {i+1}: {elem.get_text(strip=True)[:100]}...")
                
                # Look for any divs with class containing 'result' or 'match'
                all_divs = soup.find_all('div', class_=lambda x: x and ('result' in x.lower() or 'match' in x.lower() or 'event' in x.lower()))
                print(f"  Divs with 'result/match/event' in class: {len(all_divs)}")
                
                # Look for any links to matches
                match_links = soup.find_all('a', href=lambda x: x and '/matches/' in x)
                print(f"  Match links: {len(match_links)}")
                
                # Save HTML for inspection
                debug_file = f"debug_{endpoint.split('/')[-1]}.html"
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"  HTML saved to: {debug_file}")
                
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    debug_hltv_scraper()
