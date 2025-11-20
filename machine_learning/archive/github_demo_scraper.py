#!/usr/bin/env python3
"""
GitHub-based demo scraper using existing tools
"""

import requests
import json
import csv
import time
import random
import os
import subprocess
import sys
from tqdm import tqdm

class GitHubDemoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session for GitHub API"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/vnd.github.v3+json",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        self.session.headers.update(headers)
        
    def get_repo_info(self, repo_url):
        """Get information about a GitHub repository"""
        try:
            # Convert GitHub URL to API URL
            if 'github.com' in repo_url:
                api_url = repo_url.replace('github.com', 'api.github.com/repos')
                if not api_url.endswith('/'):
                    api_url += '/'
                    
                print(f"Fetching repo info: {api_url}")
                response = self.session.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Failed to get repo info: {response.status_code}")
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"Error getting repo info: {e}")
            return None
    
    def get_repo_files(self, repo_url):
        """Get files from a GitHub repository"""
        try:
            # Get repository contents
            api_url = repo_url.replace('github.com', 'api.github.com/repos') + '/contents'
            
            print(f"Fetching repo files: {api_url}")
            response = self.session.get(api_url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get repo files: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting repo files: {e}")
            return None
    
    def analyze_demo_tools(self):
        """Analyze the GitHub repositories for demo tools"""
        print("Analyzing GitHub repositories for demo tools...")
        
        # Promising repositories from our search
        demo_repos = [
            "https://github.com/ReagentX/HLTVDemoDownloader",
            "https://github.com/InnoDevTM/csgo-demo-downloader", 
            "https://github.com/jannislehmann/csgo-demodownloader",
            "https://github.com/botent/CSGO-DemoURL",
            "https://github.com/3urobeat/csgo-overwatch-downloader",
            "https://github.com/One-Studio/csgo-demo-downloader",
            "https://github.com/claabs/cs-demo-downloader",
            "https://github.com/GamerNoTitle/CSGO-Demo-AutoDownloader",
            "https://github.com/jannislehmann/csgo-tools",
            "https://github.com/AlexMFV/CSGO-Demo-Stats",
            "https://github.com/RubenvanGemeren/Fragify"
        ]
        
        repo_analysis = []
        
        for repo_url in demo_repos:
            print(f"\nAnalyzing {repo_url}...")
            
            # Get repository information
            repo_info = self.get_repo_info(repo_url)
            if not repo_info:
                continue
                
            # Get repository files
            repo_files = self.get_repo_files(repo_url)
            
            analysis = {
                'url': repo_url,
                'name': repo_info.get('name', ''),
                'description': repo_info.get('description', ''),
                'stars': repo_info.get('stargazers_count', 0),
                'forks': repo_info.get('forks_count', 0),
                'language': repo_info.get('language', ''),
                'updated': repo_info.get('updated_at', ''),
                'files': [],
                'readme_content': '',
                'usefulness_score': 0
            }
            
            # Analyze files
            if repo_files:
                for file_info in repo_files:
                    if isinstance(file_info, dict):
                        file_name = file_info.get('name', '')
                        file_type = file_info.get('type', '')
                        
                        analysis['files'].append({
                            'name': file_name,
                            'type': file_type,
                            'size': file_info.get('size', 0)
                        })
                        
                        # Check for important files
                        if file_name.lower() in ['readme.md', 'readme.txt', 'readme']:
                            # Try to get README content
                            try:
                                readme_url = file_info.get('download_url', '')
                                if readme_url:
                                    readme_response = self.session.get(readme_url, timeout=30)
                                    if readme_response.status_code == 200:
                                        analysis['readme_content'] = readme_response.text[:1000]
                            except:
                                pass
            
            # Calculate usefulness score
            score = 0
            if 'hltv' in analysis['name'].lower() or 'hltv' in analysis['description'].lower():
                score += 3
            if 'esl' in analysis['description'].lower():
                score += 2
            if 'pro league' in analysis['description'].lower():
                score += 2
            if analysis['stars'] > 10:
                score += 1
            if analysis['stars'] > 50:
                score += 2
            if 'python' in analysis['language'].lower():
                score += 1
            if 'javascript' in analysis['language'].lower():
                score += 1
                
            analysis['usefulness_score'] = score
            repo_analysis.append(analysis)
            
            time.sleep(random.uniform(1, 3))
        
        return repo_analysis
    
    def create_usage_guide(self, repo_analysis):
        """Create a usage guide for the most promising repositories"""
        guide = """
# GitHub Demo Tools Usage Guide

Based on analysis of GitHub repositories, here are the most promising tools for downloading ESL Pro League demos:

"""
        
        # Sort by usefulness score
        sorted_repos = sorted(repo_analysis, key=lambda x: x['usefulness_score'], reverse=True)
        
        for i, repo in enumerate(sorted_repos[:5], 1):
            guide += f"""
## {i}. {repo['name']}
- **URL**: {repo['url']}
- **Description**: {repo['description']}
- **Stars**: {repo['stars']} | **Forks**: {repo['forks']}
- **Language**: {repo['language']}
- **Usefulness Score**: {repo['usefulness_score']}/10
- **Last Updated**: {repo['updated']}

### Installation
```bash
git clone {repo['url']}.git
cd {repo['name']}
```

### Usage
Check the repository's README for specific usage instructions.

"""
        
        guide += """
## Next Steps
1. Clone the most promising repositories
2. Follow their installation instructions
3. Use them to download ESL Pro League demos
4. Parse the downloaded demos using your existing parsing scripts

## Recommended Order
1. Start with HLTVDemoDownloader (highest score)
2. Try cs-demo-downloader for automatic downloads
3. Use CSGO-Demo-Stats for analysis features
"""
        
        return guide

def main():
    """Main function"""
    print("="*80)
    print("GITHUB DEMO SCRAPER")
    print("="*80)
    
    scraper = GitHubDemoScraper()
    
    # Configuration
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "github_demo_analysis.json")
    CSV_FILE = os.path.join(os.path.dirname(__file__), "github_demo_analysis.csv")
    GUIDE_FILE = os.path.join(os.path.dirname(__file__), "GITHUB_DEMO_GUIDE.md")
    
    print(f"Configuration:")
    print(f"  JSON output: {OUTPUT_FILE}")
    print(f"  CSV output: {CSV_FILE}")
    print(f"  Guide output: {GUIDE_FILE}")
    print("="*80)
    
    try:
        # Analyze repositories
        repo_analysis = scraper.analyze_demo_tools()
        
        # Save results to JSON
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(repo_analysis, f, indent=2)
        
        # Save results to CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'url', 'description', 'stars', 'forks', 'language', 'usefulness_score', 'updated'])
            
            for repo in repo_analysis:
                writer.writerow([
                    repo['name'],
                    repo['url'],
                    repo['description'],
                    repo['stars'],
                    repo['forks'],
                    repo['language'],
                    repo['usefulness_score'],
                    repo['updated']
                ])
        
        # Create usage guide
        guide = scraper.create_usage_guide(repo_analysis)
        with open(GUIDE_FILE, 'w') as f:
            f.write(guide)
        
        print(f"\n" + "="*80)
        print("GITHUB ANALYSIS COMPLETE")
        print("="*80)
        print(f"Analyzed {len(repo_analysis)} repositories")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"CSV saved to: {CSV_FILE}")
        print(f"Usage guide saved to: {GUIDE_FILE}")
        
        # Show top repositories
        sorted_repos = sorted(repo_analysis, key=lambda x: x['usefulness_score'], reverse=True)
        print(f"\nTop repositories by usefulness score:")
        for i, repo in enumerate(sorted_repos[:5], 1):
            print(f"  {i}. {repo['name']} (Score: {repo['usefulness_score']}/10)")
            print(f"     {repo['url']}")
            print(f"     {repo['description']}")
            print()
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
