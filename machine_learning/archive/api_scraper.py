#!/usr/bin/env python3
"""
API-based scraper for CS2 demo data
"""

import requests
import json
import csv
import time
import random
import os
from tqdm import tqdm

class APIDemoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for API requests"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        self.session.headers.update(headers)
        
    def try_hltv_api(self):
        """Try to access HLTV API endpoints"""
        print("Trying HLTV API endpoints...")
        
        api_endpoints = [
            "https://www.hltv.org/api/matches",
            "https://www.hltv.org/api/results",
            "https://www.hltv.org/api/events",
            "https://www.hltv.org/api/teams",
            "https://www.hltv.org/api/players",
            "https://www.hltv.org/api/stats",
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
                        print(f"Response from {endpoint} is not JSON")
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
    
    def try_steam_api(self):
        """Try Steam API for CS2 data"""
        print("Trying Steam API...")
        
        # Steam API endpoints
        steam_endpoints = [
            "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?appid=730&key=YOUR_API_KEY",
            "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?appid=730&key=YOUR_API_KEY&steamid=76561198000000000",
        ]
        
        results = []
        
        for endpoint in steam_endpoints:
            try:
                print(f"Trying Steam endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=30)
                print(f"Steam API Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results.append({
                            'endpoint': endpoint,
                            'data': data,
                            'status': 'success'
                        })
                    except:
                        results.append({
                            'endpoint': endpoint,
                            'data': response.text[:500],
                            'status': 'non-json'
                        })
                        
            except Exception as e:
                print(f"Error with Steam API: {e}")
                continue
                
            time.sleep(random.uniform(1, 2))
        
        return results
    
    def try_esl_api(self):
        """Try ESL API endpoints"""
        print("Trying ESL API endpoints...")
        
        esl_endpoints = [
            "https://api.eslgaming.com/v1/events",
            "https://api.eslgaming.com/v1/matches",
            "https://api.eslgaming.com/v1/teams",
            "https://pro.eslgaming.com/api/v1/events",
            "https://pro.eslgaming.com/api/v1/matches",
        ]
        
        results = []
        
        for endpoint in esl_endpoints:
            try:
                print(f"Trying ESL endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=30)
                print(f"ESL API Status: {response.status_code}")
                
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
                        
            except Exception as e:
                print(f"Error with ESL API: {e}")
                continue
                
            time.sleep(random.uniform(1, 3))
        
        return results
    
    def try_alternative_apis(self):
        """Try alternative API endpoints"""
        print("Trying alternative API endpoints...")
        
        alternative_endpoints = [
            "https://api.faceit.com/v4/matches",
            "https://api.faceit.com/v4/events",
            "https://api.faceit.com/v4/teams",
            "https://api.faceit.com/v4/players",
            "https://api.faceit.com/v4/games",
        ]
        
        results = []
        
        for endpoint in alternative_endpoints:
            try:
                print(f"Trying alternative endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=30)
                print(f"Alternative API Status: {response.status_code}")
                
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
                        
            except Exception as e:
                print(f"Error with alternative API: {e}")
                continue
                
            time.sleep(random.uniform(1, 3))
        
        return results

def main():
    """Main function"""
    print("="*80)
    print("API DEMO SCRAPER")
    print("="*80)
    
    scraper = APIDemoScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "api_results.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "api_results.csv")
    
    print(f"Configuration:")
    print(f"  JSON output: {OUTPUT_FILE}")
    print(f"  CSV output: {CSV_FILE}")
    print("="*80)
    
    try:
        all_results = []
        
        # Try different API sources
        print("Testing HLTV API...")
        hltv_results = scraper.try_hltv_api()
        all_results.extend(hltv_results)
        
        print("Testing Steam API...")
        steam_results = scraper.try_steam_api()
        all_results.extend(steam_results)
        
        print("Testing ESL API...")
        esl_results = scraper.try_esl_api()
        all_results.extend(esl_results)
        
        print("Testing alternative APIs...")
        alt_results = scraper.try_alternative_apis()
        all_results.extend(alt_results)
        
        # Save results to JSON
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Save results to CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['endpoint', 'status', 'data_preview'])
            
            for result in all_results:
                data_preview = str(result.get('data', ''))[:200] + '...' if len(str(result.get('data', ''))) > 200 else str(result.get('data', ''))
                writer.writerow([
                    result.get('endpoint', ''),
                    result.get('status', ''),
                    data_preview
                ])
        
        print(f"\n" + "="*80)
        print("API SCRAPING COMPLETE")
        print("="*80)
        print(f"Tested {len(all_results)} API endpoints")
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
