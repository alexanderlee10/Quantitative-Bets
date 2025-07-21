import requests
from bs4 import BeautifulSoup
import re

def get_team_defense_rankings(statistic):
    """
    Scrapes team defensive rankings for a given statistic from StatMuse
    Returns a list of tuples: (team_name, value, rank)
    """
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
    
    # Convert player stat to team defensive stat
    team_stat = stat_mapping.get(statistic, statistic.lower())
    
    url = f"https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-{team_stat}-per-game-this-season"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table
        table = soup.find('table')
        if not table:
            print(f"No table found for {statistic}")
            return []
        
        # Extract headers
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        
        # Based on the debug output, team names are in column 2, defensive stats in column 3
        team_name_col = 2  # TEAM column
        def_stat_col = 3   # OPP PTS/GP column
        
        # Extract rows
        rows = table.find_all('tr')[1:]  # Skip header row
        raw_rankings = []
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) > max(team_name_col, def_stat_col):
                # Get team name from the team column (index 2)
                team_cell = cells[team_name_col]
                value = cells[def_stat_col].get_text(strip=True)
                
                # Get team name from the team cell
                team_name = team_cell.get_text(strip=True)
                
                # Clean up team name
                team_name = re.sub(r'\s*\([^)]*\)', '', team_name)  # Remove parentheses
                team_name = re.sub(r'\s*Logo.*', '', team_name)  # Remove Logo text
                team_name = re.sub(r'\s*2024-25.*', '', team_name)  # Remove season
                team_name = team_name.strip()
                
                # Debug: print what we're extracting
                print(f"Extracted team: '{team_name}', value: {value}")
                
                # Try to convert value to float, skip if not numeric
                try:
                    float_value = float(value)
                    if team_name and len(team_name) > 2:  # Only add if we have a meaningful team name
                        raw_rankings.append((team_name, float_value))
                except ValueError:
                    print(f"  Skipping non-numeric value: '{value}' for team '{team_name}'")
                    continue  # Skip non-numeric values
        
        # Sort by value (worst defense first) and assign proper ranks
        raw_rankings.sort(key=lambda x: x[1], reverse=True)
        rankings = []
        for i, (team_name, value) in enumerate(raw_rankings):
            rankings.append((team_name, value, i + 1))
        
        print(f"Final rankings (worst to best):")
        for team, value, rank in rankings:
            print(f"  {rank}. {team}: {value:.2f}")
        
        return rankings
        
    except Exception as e:
        print(f"Error scraping team defense rankings for {statistic}: {e}")
        return []

def get_opponent_defense_rank(player_data, statistic):
    """
    Gets the defensive ranking of the opponent for a specific statistic
    """
    if not player_data or len(player_data) < 2:
        return None
    
    # Get the opponent from the most recent game
    header = player_data[0]
    if 'OPP' not in header:
        return None
    
    opp_index = header.index('OPP')
    opponent = player_data[1][opp_index]  # Most recent game
    
    # Get team defense rankings
    rankings = get_team_defense_rankings(statistic)
    
    # Find the opponent's ranking
    print(f"Looking for opponent: '{opponent}'")
    for team_name, value, rank in rankings:
        print(f"Checking against: '{team_name}'")
        # More flexible matching
        if (team_name.lower() in opponent.lower() or 
            opponent.lower() in team_name.lower() or
            any(word in team_name.lower() for word in opponent.lower().split()) or
            any(word in opponent.lower() for word in team_name.lower().split())):
            print(f"Found match: {team_name}")
            return {
                'team': team_name,
                'value': value,
                'rank': rank,
                'total_teams': len(rankings)
            }
    
    return None

def get_defense_analysis(player_data, statistic):
    """
    Comprehensive defense analysis for a player's upcoming opponent
    """
    if not player_data or len(player_data) < 2:
        print("No player data available")
        return None
    
    header = player_data[0]
    if 'OPP' not in header:
        print("No OPP column found in header")
        return None
    
    opp_index = header.index('OPP')
    opponent = player_data[1][opp_index]  # Most recent game
    print(f"Looking for opponent: '{opponent}'")
    
    # Get team defense rankings
    rankings = get_team_defense_rankings(statistic)
    print(f"Found {len(rankings)} team rankings")
    
    # Find the opponent's ranking with improved matching
    opponent_rank = None
    
    # Team abbreviation mapping
    team_abbrevs = {
        'UTA': 'Jazz', 'JAZ': 'Jazz',
        'LAL': 'Lakers', 'LAK': 'Lakers',
        'GSW': 'Warriors', 'GOL': 'Warriors',
        'BOS': 'Celtics', 'CEL': 'Celtics',
        'CHI': 'Bulls', 'BUL': 'Bulls',
        'DAL': 'Mavericks', 'MAV': 'Mavericks',
        'DEN': 'Nuggets', 'NUG': 'Nuggets',
        'HOU': 'Rockets', 'ROC': 'Rockets',
        'LAC': 'Clippers', 'CLI': 'Clippers',
        'MEM': 'Grizzlies', 'GRI': 'Grizzlies',
        'MIA': 'Heat', 'HEA': 'Heat',
        'MIL': 'Bucks', 'BUC': 'Bucks',
        'MIN': 'Timberwolves', 'TIM': 'Timberwolves',
        'NOP': 'Pelicans', 'PEL': 'Pelicans',
        'NYK': 'Knicks', 'KNI': 'Knicks',
        'OKC': 'Thunder', 'THU': 'Thunder',
        'ORL': 'Magic', 'MAG': 'Magic',
        'PHI': '76ers', 'SIX': '76ers',
        'PHX': 'Suns', 'SUN': 'Suns',
        'POR': 'Trail Blazers', 'BLA': 'Trail Blazers',
        'SAC': 'Kings', 'KIN': 'Kings',
        'SAS': 'Spurs', 'SPU': 'Spurs',
        'TOR': 'Raptors', 'RAP': 'Raptors',
        'WAS': 'Wizards', 'WIZ': 'Wizards',
        'ATL': 'Hawks', 'HAW': 'Hawks',
        'BKN': 'Nets', 'NET': 'Nets',
        'CHA': 'Hornets', 'HOR': 'Hornets',
        'CLE': 'Cavaliers', 'CAV': 'Cavaliers',
        'DET': 'Pistons', 'PIS': 'Pistons',
        'IND': 'Pacers', 'PAC': 'Pacers'
    }
    
    for team_name, value, rank in rankings:
        print(f"Checking '{team_name}' against '{opponent}'")
        
        # Check direct match
        if (team_name.lower() in opponent.lower() or 
            opponent.lower() in team_name.lower()):
            print(f"MATCH FOUND: {team_name}")
            opponent_rank = {
                'team': team_name,
                'value': value,
                'rank': rank,
                'total_teams': len(rankings)
            }
            break
        
        # Check abbreviation match
        if opponent.upper() in team_abbrevs and team_abbrevs[opponent.upper()] == team_name:
            print(f"MATCH FOUND via abbreviation: {team_name}")
            opponent_rank = {
                'team': team_name,
                'value': value,
                'rank': rank,
                'total_teams': len(rankings)
            }
            break
        
        # Check word-based matching
        if (any(word in team_name.lower() for word in opponent.lower().split()) or
            any(word in opponent.lower() for word in team_name.lower().split())):
            
            print(f"MATCH FOUND via word matching: {team_name}")
            opponent_rank = {
                'team': team_name,
                'value': value,
                'rank': rank,
                'total_teams': len(rankings)
            }
            break
    
    if not opponent_rank:
        print(f"No match found for opponent '{opponent}'")
        # Return a default analysis with the opponent name
        return {
            'opponent': opponent,
            'rank': 15,  # Default middle rank
            'total_teams': len(rankings),
            'value_allowed': 0.0,
            'difficulty': "Unknown",
            'color': "white",
            'rank_percentage': 50.0
        }
    
    # Calculate difficulty level
    rank_percentage = (opponent_rank['rank'] / opponent_rank['total_teams']) * 100
    
    if rank_percentage <= 33:
        difficulty = "Easy"
        color = "green"
    elif rank_percentage <= 66:
        difficulty = "Medium"
        color = "orange"
    else:
        difficulty = "Hard"
        color = "red"
    
    print(f"Opponent analysis complete: {opponent_rank['team']} ranked #{opponent_rank['rank']}")
    
    return {
        'opponent': opponent_rank['team'],
        'rank': opponent_rank['rank'],
        'total_teams': opponent_rank['total_teams'],
        'value_allowed': opponent_rank['value'],
        'difficulty': difficulty,
        'color': color,
        'rank_percentage': rank_percentage
    } 