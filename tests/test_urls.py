import requests
from bs4 import BeautifulSoup
import re

def test_url(url, description):
    """Test a URL and show the results"""
    print(f"\n=== Testing: {description} ===")
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
        
        # Extract first few rows
        rows = table.find_all('tr')[1:4]  # First 3 data rows
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) >= 3:
                team = cells[1].get_text(strip=True) if len(cells) > 1 else "N/A"
                value = cells[2].get_text(strip=True) if len(cells) > 2 else "N/A"
                print(f"  Row {i+1}: {team} = {value}")
                
    except Exception as e:
        print(f"Error: {e}")

# Test different URL formats
urls_to_test = [
    ("https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-points-per-game-this-season", "Current format - per-game"),
    ("https://www.statmuse.com/nba/ask/nba-teams-who-give-up-the-most-points", "Alternative format - no per-game"),
    ("https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-points-this-season", "Alternative format - this-season"),
    ("https://www.statmuse.com/nba/ask/nba-teams-who-give-up-most-assists-this-season", "Assists format"),
    ("https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-rebounds-and-points-per-game-this-season", "Rebounds format")
]

for url, desc in urls_to_test:
    test_url(url, desc) 