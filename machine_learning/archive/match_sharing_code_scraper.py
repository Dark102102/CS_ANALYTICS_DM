#!/usr/bin/env python3
"""
Match sharing code scraper - uses Valve's match sharing codes to get demos
"""

import requests
import json
import csv
import time
import random
import os
from urllib.parse import urljoin
from tqdm import tqdm
import base64
import struct

class MatchSharingCodeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for match sharing code requests"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        self.session.headers.update(headers)
        
    def decode_match_sharing_code(self, share_code):
        """Decode a match sharing code to get match details"""
        try:
            # Remove any whitespace and convert to bytes
            share_code = share_code.strip()
            
            # Add padding if needed
            padding = 4 - (len(share_code) % 4)
            if padding != 4:
                share_code += '=' * padding
            
            # Decode base64
            decoded = base64.b64decode(share_code)
            
            # Parse the decoded data
            # This is a simplified version - the actual format is more complex
            if len(decoded) >= 8:
                match_id = struct.unpack('<Q', decoded[:8])[0]
                return {
                    'match_id': match_id,
                    'share_code': share_code,
                    'decoded_length': len(decoded)
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error decoding share code {share_code}: {e}")
            return None
    
    def get_demo_from_share_code(self, share_code):
        """Get demo URL from match sharing code"""
        try:
            # Steam API endpoint for match sharing codes
            api_url = "https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1/"
            
            # This is a simplified approach - the actual API might be different
            params = {
                'key': 'YOUR_STEAM_API_KEY',  # You'd need a Steam API key
                'steamid': '76561198000000000',  # Example Steam ID
                'steamidkey': 'YOUR_STEAM_ID_KEY',  # You'd need this too
                'sharecode': share_code
            }
            
            response = self.session.get(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Failed to get demo from share code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting demo from share code: {e}")
            return None
    
    def try_alternative_share_code_sources(self):
        """Try to find match sharing codes from alternative sources"""
        print("Searching for match sharing codes...")
        
        # Sources that might have match sharing codes
        sources = [
            "https://www.reddit.com/r/GlobalOffensive",
            "https://www.reddit.com/r/cs2",
            "https://www.reddit.com/r/csgo",
            "https://steamcommunity.com/app/730/discussions/",
            "https://steamcommunity.com/app/730/workshop/",
        ]
        
        found_codes = []
        
        for source in sources:
            try:
                print(f"Searching {source}...")
                response = self.session.get(source, timeout=30)
                
                if response.status_code == 200:
                    # Look for match sharing codes in the content
                    content = response.text
                    
                    # Match sharing codes are typically in format: CSGO-XXXXX-XXXX-XXXXX
                    import re
                    share_code_pattern = r'CSGO-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}'
                    codes = re.findall(share_code_pattern, content)
                    
                    for code in codes:
                        found_codes.append({
                            'share_code': code,
                            'source': source,
                            'type': 'reddit_steam'
                        })
                        print(f"Found share code: {code}")
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error searching {source}: {e}")
                continue
        
        return found_codes
    
    def try_steam_api_endpoints(self):
        """Try Steam API endpoints for match data"""
        print("Trying Steam API endpoints...")
        
        # Steam API endpoints
        steam_endpoints = [
            "https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1/",
            "https://api.steampowered.com/ICSGOPlayers_730/GetMatchHistory/v1/",
            "https://api.steampowered.com/ICSGOPlayers_730/GetMatchDetails/v1/",
            "https://api.steampowered.com/ICSGOPlayers_730/GetPlayerSummaries/v2/",
            "https://api.steampowered.com/ICSGOPlayers_730/GetOwnedGames/v1/",
        ]
        
        results = []
        
        for endpoint in steam_endpoints:
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
    
    def create_share_code_generator(self):
        """Create a tool to generate and test share codes"""
        generator_code = '''#!/usr/bin/env python3
"""
Match sharing code generator and tester
"""

import requests
import time
import random
import base64
import struct

def generate_test_share_codes():
    """Generate test share codes for ESL Pro League matches"""
    # These are example share codes - you'd need real ones
    test_codes = [
        "CSGO-XXXXX-XXXXX-XXXXX",  # Replace with real codes
        "CSGO-YYYYY-YYYYY-YYYYY",  # Replace with real codes
        "CSGO-ZZZZZ-ZZZZZ-ZZZZZ",  # Replace with real codes
    ]
    
    return test_codes

def test_share_code(share_code):
    """Test if a share code is valid"""
    try:
        # Remove CSGO- prefix and decode
        code = share_code.replace('CSGO-', '')
        code = code.replace('-', '')
        
        # Add padding
        padding = 4 - (len(code) % 4)
        if padding != 4:
            code += '=' * padding
        
        # Try to decode
        decoded = base64.b64decode(code)
        
        if len(decoded) >= 8:
            match_id = struct.unpack('<Q', decoded[:8])[0]
            return {
                'valid': True,
                'match_id': match_id,
                'share_code': share_code
            }
        else:
            return {
                'valid': False,
                'error': 'Invalid length'
            }
            
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def main():
    """Main function"""
    print("Testing match sharing codes...")
    
    test_codes = generate_test_share_codes()
    
    for code in test_codes:
        print(f"Testing {code}...")
        result = test_share_code(code)
        
        if result['valid']:
            print(f"  Valid! Match ID: {result['match_id']}")
        else:
            print(f"  Invalid: {result['error']}")

if __name__ == "__main__":
    main()
'''
        
        with open('share_code_generator.py', 'w') as f:
            f.write(generator_code)
        
        print("Created share_code_generator.py for testing match sharing codes")

def main():
    """Main function"""
    print("="*80)
    print("MATCH SHARING CODE SCRAPER")
    print("="*80)
    
    scraper = MatchSharingCodeScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "share_code_results.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "share_code_results.csv")
    
    print(f"Configuration:")
    print(f"  JSON output: {OUTPUT_FILE}")
    print(f"  CSV output: {CSV_FILE}")
    print("="*80)
    
    try:
        all_results = []
        
        # Try different methods
        print("Searching for match sharing codes...")
        share_codes = scraper.try_alternative_share_code_sources()
        all_results.extend(share_codes)
        
        print("Testing Steam API endpoints...")
        steam_results = scraper.try_steam_api_endpoints()
        all_results.extend(steam_results)
        
        # Create share code generator
        scraper.create_share_code_generator()
        
        # Save results to JSON
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Save results to CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['share_code', 'source', 'type', 'endpoint', 'status'])
            
            for result in all_results:
                writer.writerow([
                    result.get('share_code', ''),
                    result.get('source', ''),
                    result.get('type', ''),
                    result.get('endpoint', ''),
                    result.get('status', '')
                ])
        
        print(f"\n" + "="*80)
        print("SHARE CODE SCRAPING COMPLETE")
        print("="*80)
        print(f"Found {len(share_codes)} share codes")
        print(f"Tested {len(steam_results)} Steam API endpoints")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"CSV saved to: {CSV_FILE}")
        print(f"Generator created: share_code_generator.py")
        
        if share_codes:
            print(f"\nFound share codes:")
            for code in share_codes:
                print(f"  - {code['share_code']} from {code['source']}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
