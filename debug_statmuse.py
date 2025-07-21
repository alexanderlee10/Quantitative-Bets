#!/usr/bin/env python3
"""
Debug script to examine StatMuse table structure
"""

import requests
from bs4 import BeautifulSoup

def debug_statmuse_table(statistic):
    """Debug the StatMuse table structure"""
    
    # Map player stats to team defensive stats
    stat_mapping = {
        'PTS': 'points',
        'REB': 'rebounds', 
        'AST': 'assists',
        'STL': 'steals',
        'BLK': 'blocks',
        '3PM': '3-pointers',
        'FTM': 'free-throws',
        'TOV': 'turnovers',
        'FGM': 'field-goals',
        'FGA': 'field-goal-attempts',
        '3PA': '3-point-attempts',
        'FTA': 'free-throw-attempts'
    }
    
    team_stat = stat_mapping.get(statistic, statistic.lower())
    url = f"https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-{team_stat}-per-game-this-season"
    
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table
        table = soup.find('table')
        if not table:
            print("No table found!")
            return
        
        # Extract headers
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        print(f"\nHeaders: {headers}")
        
        # Extract first few rows to see structure
        rows = table.find_all('tr')[1:6]  # First 5 data rows
        
        print(f"\nFirst 5 rows structure:")
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            print(f"\nRow {i+1}:")
            for j, cell in enumerate(cells):
                cell_text = cell.get_text(strip=True)
                cell_html = str(cell)[:100] + "..." if len(str(cell)) > 100 else str(cell)
                print(f"  Cell {j}: '{cell_text}' | HTML: {cell_html}")
                
                # Check for links in this cell
                links = cell.find_all('a')
                if links:
                    print(f"    Links found: {[link.get_text(strip=True) for link in links]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Debugging StatMuse Table Structure ===\n")
    debug_statmuse_table('PTS') 