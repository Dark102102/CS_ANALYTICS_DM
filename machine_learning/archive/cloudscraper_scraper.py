#!/usr/bin/env python3
"""
Cloudscraper-based scraper to bypass Cloudflare protection for HLTV
"""

import cloudscraper
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm
import os
from urllib.parse import urljoin
import random

BASE = "https://www.hltv.org"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

# Create cloudscraper session
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',
        'mobile': False
    }
)

DEBUG = True
DEBUG_DIR = os.path.join(os.path.dirname(__file__), "_debug")

def debug_write(name: str, content: str):
    if not DEBUG:
        return
    os.makedirs(DEBUG_DIR, exist_ok=True)
    path = os.path.join(DEBUG_DIR, name)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[debug] failed to write {path}: {e}")

def get_match_links(pages=5, event_filter=None):
    links = []
    
    print("Establishing session with HLTV using cloudscraper...")
    try:
        # First, try to access the main page to establish session
        main_page = scraper.get(f"{BASE}/", headers=HEADERS, timeout=30)
        if DEBUG:
            print(f"[debug] Main page GET -> {main_page.status_code}")
        time.sleep(random.uniform(2, 4))  # Random delay
    except Exception as e:
        print(f"Warning: Could not establish session: {e}")
    
    for offset in range(0, pages * 100, 100):
        url = f"{BASE}/results?offset={offset}"
        if DEBUG:
            print(f"[debug] Requesting: {url}")
        
        try:
            r = scraper.get(url, headers=HEADERS, timeout=30)
            if DEBUG:
                print(f"[debug] GET {url} -> {r.status_code}, {len(r.text)} bytes")
            
            if r.status_code != 200:
                print(f"Warning: non-200 status {r.status_code} for {url}")
                continue
                
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Each match is in a div.result-con which contains event info
            match_containers = soup.select("div.result-con")
            if DEBUG:
                print(f"[debug] Found {len(match_containers)} match containers on offset {offset}")
            if offset == 0:
                debug_write("results_offset0.html", r.text)
            
            for container in match_containers:
                # Get event name from the container
                event_elem = container.select_one(".event-name")
                event_name = event_elem.get_text(strip=True) if event_elem else ""
                
                # Get match link
                match_link = container.select_one("a")
                if not match_link:
                    continue
                href = match_link.get("href", "")
                if href.startswith("/"):
                    href = BASE + href
                if "/matches/" not in href:
                    continue
                
                # Apply event filter if specified
                if event_filter:
                    if event_filter.lower() not in event_name.lower():
                        if DEBUG:
                            print(f"[debug] Skipping match (event: {event_name})")
                        continue
                    if DEBUG:
                        print(f"[debug] Including match from event: {event_name}")
                
                links.append(href)
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
            
        # Random delay between pages
        time.sleep(random.uniform(3, 6))
    
    # de-dupe preserving order
    seen = set()
    unique_links = []
    for h in links:
        if h not in seen:
            seen.add(h)
            unique_links.append(h)
    if DEBUG:
        print(f"[debug] Total unique match links collected: {len(unique_links)}")
    return unique_links

def extract_match_id_from_url(url: str) -> str:
    try:
        path = url.split("?")[0]
        parts = path.split("/")
        # https://www.hltv.org/matches/<id>/...
        for i, part in enumerate(parts):
            if part == "matches" and i + 1 < len(parts):
                return parts[i + 1]
    except Exception:
        return ""
    return ""

def extract_demo_link(soup: BeautifulSoup) -> str | None:
    # Prefer data attribute on the button
    btn = soup.select_one(".streams [data-demo-link]")
    if btn and btn.get("data-demo-link"):
        return urljoin(BASE, btn.get("data-demo-link"))
    # Fallback hidden link anchor
    hidden = soup.select_one(".streams a[data-manuel-download]")
    if hidden and hidden.get("href"):
        return urljoin(BASE, hidden.get("href"))
    return None

def safe_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in (".", "-", "_") else "_" for c in name)

def download_demo_file(demo_url: str, match_url: str, match_id: str, demos_dir: str) -> str | None:
    try:
        os.makedirs(demos_dir, exist_ok=True)
        demo_id = demo_url.rstrip("/").split("/")[-1]
        default_basename = safe_filename(f"{match_id}_{demo_id}")
        headers = dict(HEADERS)
        headers["Referer"] = match_url

        print(f"Downloading demo from: {demo_url}")
        response = scraper.get(demo_url, headers=headers, timeout=300, stream=True)
        
        if response.status_code != 200:
            print(f"Warning: demo GET {demo_url} -> {response.status_code}")
            return None
        
        # Determine filename
        filename = default_basename
        if 'Content-Disposition' in response.headers:
            cd = response.headers['Content-Disposition']
            if 'filename=' in cd:
                fname = cd.split('filename=')[-1].strip().strip('"').strip("'")
                if fname:
                    filename = safe_filename(fname)
        
        # Add extension if not present
        if not any(filename.lower().endswith(ext) for ext in ['.rar', '.zip', '.7z', '.dem']):
            filename += '.rar'  # Default extension
        
        filepath = os.path.join(demos_dir, filename)
        
        # Download the file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size < 1000000:  # Less than 1MB, likely invalid
            os.remove(filepath)
            print(f"Warning: Downloaded file too small ({file_size} bytes), removing")
            return None
        
        print(f"Downloaded demo: {filepath} ({file_size} bytes)")
        return filepath
        
    except Exception as e:
        print(f"Error downloading demo {demo_url}: {e}")
        return None

def fetch_match_data(match_url):
    match_id = extract_match_id_from_url(match_url)
    url = match_url if match_url.startswith("http") else (BASE + match_url)
    
    try:
        r = scraper.get(url, headers=HEADERS, timeout=20)
        if DEBUG:
            print(f"[debug] GET {url} -> {r.status_code}, {len(r.text)} bytes")
        if r.status_code != 200:
            return {"match_id": match_id, "error": f"status_{r.status_code}", "players": []}

        soup = BeautifulSoup(r.text, "html.parser")

        teams = soup.select(".teamName")
        team1 = teams[0].text.strip() if teams else None
        team2 = teams[1].text.strip() if len(teams) > 1 else None

        score = None
        score_el = soup.select_one(".score")
        if score_el:
            score = score_el.get_text(strip=True).replace(" ", "")  # e.g. 3:1

        date = None
        date_el = soup.select_one(".date[data-unix]") or soup.select_one(".date")
        if date_el:
            date = date_el.get_text(strip=True)

        players = []
        lineup_links = soup.select("#lineups .lineup a[href^='/player/']")
        if DEBUG:
            print(f"[debug] lineup player links: {len(lineup_links)} for match {match_id}")
        for a in lineup_links:
            name = a.get_text(strip=True)
            if name:
                players.append({"name": name, "kd": None, "adr": None, "rating": None})

        demo_link = extract_demo_link(soup)

        if DEBUG:
            fname = f"match_{match_id or 'unknown'}.html"
            debug_write(fname, r.text)

        return {
            "match_id": match_id,
            "date": date,
            "team1": team1,
            "team2": team2,
            "score": score,
            "demo_url": demo_link,
            "players": players,
            "match_url": url,
        }
        
    except Exception as e:
        print(f"Error fetching match data for {url}: {e}")
        return {"match_id": match_id, "error": str(e), "players": []}

def scrape_and_save(pages=3, outfile="hltv_matches_cloudscraper.csv", download_demos=False, demos_dir="demos", event_filter=None):
    links = get_match_links(pages, event_filter=event_filter)
    if not links:
        print("No match links found. Check _debug/results_offset0.html and your network/headers.")
        return
    
    # Limit to first 10 matches
    links = links[:10]
    print(f"Found {len(links)} ESL Pro League matches to scrape")
    all_data = []
    downloaded_count = 0
    max_demos = 10
    
    for link in tqdm(links, desc="Scraping matches"):
        data = fetch_match_data(link)
        all_data.append(data)
        
        if download_demos and data.get("demo_url") and downloaded_count < max_demos:
            result_path = download_demo_file(data["demo_url"], data.get("match_url") or link, data.get("match_id") or "", demos_dir)
            if result_path:
                downloaded_count += 1
        
        # Random delay to avoid rate limiting
        time.sleep(random.uniform(5, 8))

    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["match_id", "date", "team1", "team2", "score", "player", "kd", "adr", "rating", "demo_url"])
        for m in all_data:
            if m.get("players"):
                for p in m["players"]:
                    writer.writerow([
                        m["match_id"], m.get("date"), m.get("team1"), m.get("team2"),
                        m.get("score"), p.get("name"), p.get("kd"), p.get("adr"), p.get("rating"),
                        m.get("demo_url")
                    ])

if __name__ == "__main__":
    """
    Cloudscraper-based HLTV scraper for ESL Pro League matches
    """
    
    # ===== CONFIGURATION =====
    DEBUG = True                 # Set to True for verbose debug output
    PAGES = 5                    # Number of result pages to scrape (100 matches per page)
    NUM_MATCHES = 10             # Limit number of matches to collect
    EVENT_FILTER = "ESL Pro League"  # Filter for specific event (None for all events)
    DOWNLOAD_DEMOS = True        # Download demo files (requires ~1GB per demo)
    
    # Output paths
    OUTFILE = os.path.join(os.path.dirname(__file__), "hltv_matches_cloudscraper.csv")
    DEMOS_DIR = os.path.join(os.path.dirname(__file__), "demos")
    
    # Rate limiting (adjust if getting blocked)
    DELAY_BETWEEN_MATCHES = 5    # Seconds between match requests
    DELAY_BETWEEN_PAGES = 3      # Seconds between page requests
    # ===== END CONFIGURATION =====
    
    # Print configuration
    print("="*80)
    print("HLTV.ORG DATA SCRAPER - ESL PRO LEAGUE CS2 (CLOUDSCRAPER)")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Event Filter: {EVENT_FILTER if EVENT_FILTER else 'All events'}")
    print(f"  Pages to scrape: {PAGES}")
    print(f"  Max matches: {NUM_MATCHES}")
    print(f"  Download demos: {DOWNLOAD_DEMOS}")
    print(f"  Output file: {OUTFILE}")
    print(f"  Demos directory: {DEMOS_DIR}")
    print(f"  Debug mode: {DEBUG}")
    print(f"  Rate limiting: Random delays between requests")
    print("\n" + "="*80)
    
    # Update global DEBUG setting
    if DEBUG:
        print("\n[DEBUG MODE ENABLED]")
        globals()['DEBUG'] = True
    
    # Run scraping
    try:
        scrape_and_save(
            pages=PAGES,
            outfile=OUTFILE,
            download_demos=DOWNLOAD_DEMOS,
            demos_dir=DEMOS_DIR,
            event_filter=EVENT_FILTER
        )
        
        print("\n" + "="*80)
        print("SCRAPING COMPLETE")
        print("="*80)
        print(f"\nData saved to: {OUTFILE}")
        if DOWNLOAD_DEMOS:
            print(f"Demos saved to: {DEMOS_DIR}")
        print("\nNext steps:")
        print("  1. Extract demos: Check demos/ folder")
        print("  2. Parse demos: python parse_demo_demoparser2.py")
        print("  3. Analyze data: python data_exploration.py")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Scraping cancelled by user")
        print(f"Partial data may be saved to: {OUTFILE}")
    except Exception as e:
        print(f"\n[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()
