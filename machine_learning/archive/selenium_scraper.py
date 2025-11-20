#!/usr/bin/env python3
"""
Selenium-based scraper to bypass Cloudflare protection
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from pathlib import Path
import csv

BASE_DIR = Path(__file__).parent
DEMOS_DIR = BASE_DIR / "demos"
DEMOS_DIR.mkdir(exist_ok=True)

def setup_driver():
    """Setup Chrome driver with options to bypass detection"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def wait_for_cloudflare(driver, timeout=30):
    """Wait for Cloudflare challenge to complete"""
    print("Waiting for Cloudflare challenge to complete...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Check if we're still on a challenge page
            if "Just a moment" in driver.page_source or "challenge-platform" in driver.page_source:
                time.sleep(2)
                continue
            else:
                print("Cloudflare challenge completed!")
                return True
        except Exception:
            time.sleep(2)
    
    print("Cloudflare challenge timeout")
    return False

def scrape_matches_with_selenium():
    """Scrape match data using Selenium"""
    driver = setup_driver()
    
    try:
        print("Navigating to HLTV results page...")
        driver.get("https://www.hltv.org/results")
        
        # Wait for Cloudflare challenge
        if not wait_for_cloudflare(driver, timeout=60):
            print("Failed to bypass Cloudflare protection")
            return []
        
        # Wait for page to load
        time.sleep(5)
        
        # Find match links
        match_links = []
        try:
            # Look for match result containers
            result_containers = driver.find_elements(By.CSS_SELECTOR, "div.result-con")
            print(f"Found {len(result_containers)} match containers")
            
            for container in result_containers[:10]:  # Limit to first 10
                try:
                    # Check if it's ESL Pro League
                    event_elem = container.find_element(By.CSS_SELECTOR, ".event-name")
                    event_name = event_elem.text.strip()
                    
                    if "ESL Pro League" in event_name:
                        # Get match link
                        match_link = container.find_element(By.CSS_SELECTOR, "a")
                        href = match_link.get_attribute("href")
                        if href and "/matches/" in href:
                            match_links.append(href)
                            print(f"Found ESL Pro League match: {href}")
                except Exception as e:
                    print(f"Error processing container: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error finding match containers: {e}")
        
        print(f"Found {len(match_links)} ESL Pro League matches")
        return match_links
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    finally:
        driver.quit()

def download_demo_from_match(match_url, demos_dir):
    """Download demo from a specific match page"""
    driver = setup_driver()
    
    try:
        print(f"Processing match: {match_url}")
        driver.get(match_url)
        
        # Wait for Cloudflare challenge
        if not wait_for_cloudflare(driver, timeout=30):
            print("Failed to bypass Cloudflare protection")
            return None
        
        time.sleep(3)
        
        # Look for demo download link
        try:
            # Try different selectors for demo links
            demo_selectors = [
                ".streams [data-demo-link]",
                ".streams a[data-manuel-download]",
                "a[href*='demo']",
                ".download-demo"
            ]
            
            demo_url = None
            for selector in demo_selectors:
                try:
                    demo_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if demo_elem:
                        demo_url = demo_elem.get_attribute("data-demo-link") or demo_elem.get_attribute("href")
                        if demo_url:
                            break
                except:
                    continue
            
            if demo_url:
                if demo_url.startswith("/"):
                    demo_url = "https://www.hltv.org" + demo_url
                
                print(f"Found demo URL: {demo_url}")
                
                # Download the demo file
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "Referer": match_url
                }
                
                response = requests.get(demo_url, headers=headers, stream=True, timeout=300)
                if response.status_code == 200:
                    # Extract filename from URL or headers
                    filename = demo_url.split("/")[-1]
                    if not filename.endswith(('.rar', '.zip', '.7z')):
                        filename += '.rar'  # Default extension
                    
                    filepath = demos_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Downloaded demo: {filepath}")
                    return str(filepath)
                else:
                    print(f"Failed to download demo: HTTP {response.status_code}")
            else:
                print("No demo link found")
                
        except Exception as e:
            print(f"Error finding demo link: {e}")
        
        return None
        
    except Exception as e:
        print(f"Error processing match {match_url}: {e}")
        return None
    finally:
        driver.quit()

def main():
    """Main scraping function"""
    print("=== Selenium-based HLTV Scraper ===\n")
    
    # Scrape match links
    match_links = scrape_matches_with_selenium()
    
    if not match_links:
        print("No match links found")
        return
    
    print(f"\n=== Downloading Demos ===")
    downloaded_demos = []
    
    for i, match_url in enumerate(match_links[:5], 1):  # Limit to 5 demos
        print(f"\n--- [{i}/{min(5, len(match_links))}] Processing match ---")
        demo_path = download_demo_from_match(match_url, DEMOS_DIR)
        if demo_path:
            downloaded_demos.append(demo_path)
        time.sleep(5)  # Delay between downloads
    
    print(f"\n=== Download Complete ===")
    print(f"Downloaded {len(downloaded_demos)} demo files:")
    for demo in downloaded_demos:
        print(f"  - {demo}")
    
    if downloaded_demos:
        print(f"\nDemos saved to: {DEMOS_DIR}")
        print("Next step: Extract and parse the demos")

if __name__ == "__main__":
    main()
