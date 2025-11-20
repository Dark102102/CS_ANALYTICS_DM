#!/usr/bin/env python3
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
