#!/usr/bin/env python3
"""
Test script to check team defense rankings for all statistics
"""

import requests
from bs4 import BeautifulSoup
import re

def test_stat_url(stat, url):
    """Test a specific stat URL and show the results"""
    print(f"\n=== Testing {stat.upper()} ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table
        table = soup.find('table')
        if not table:
            print("No table found")
            return
        
        # Extract headers
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        print(f"Headers: {headers}")
        
        # Show first 2 rows with key columns
        rows = table.find_all('tr')[1:3]  # First 2 data rows
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) >= 5:
                team = cells[2].get_text(strip=True) if len(cells) > 2 else "N/A"
                col3 = cells[3].get_text(strip=True) if len(cells) > 3 else "N/A"
                col4 = cells[4].get_text(strip=True) if len(cells) > 4 else "N/A"
                print(f"  Row {i+1}: {team} | Col3: {col3} | Col4: {col4}")
                
        # Check for specific columns
        if 'OPP PTS/GP' in headers:
            print(f"✓ Found 'OPP PTS/GP' at index {headers.index('OPP PTS/GP')}")
        if 'OPP PTS' in headers:
            print(f"✓ Found 'OPP PTS' at index {headers.index('OPP PTS')}")
        if 'OPP AST/GP' in headers:
            print(f"✓ Found 'OPP AST/GP' at index {headers.index('OPP AST/GP')}")
        if 'OPP AST' in headers:
            print(f"✓ Found 'OPP AST' at index {headers.index('OPP AST')}")
        if 'OPP REB/GP' in headers:
            print(f"✓ Found 'OPP REB/GP' at index {headers.index('OPP REB/GP')}")
        if 'OPP REB' in headers:
            print(f"✓ Found 'OPP REB' at index {headers.index('OPP REB')}")
                
    except Exception as e:
        print(f"Error: {e}")

# Test different stats
stats_to_test = [
    ("points", "https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-points-per-game-this-season"),
    ("assists", "https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-assists-per-game-this-season"),
    ("rebounds", "https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-rebounds-per-game-this-season")
]

for stat, url in stats_to_test:
    test_stat_url(stat, url) 