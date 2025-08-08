import requests
from bs4 import BeautifulSoup
import time
import re

def get_comprehensive_defense_rankings():
    """
    Get comprehensive team defense rankings by combining multiple statistics
    """
    # Define the statistics we want to analyze (focusing on offensive production allowed)
    stats_to_analyze = [
        'PTS', 'REB', 'AST', 'FGM', '3PM', 'FTM', 'FGA', '3PA', 'FTA'
    ]
    
    # Weights for each statistic (higher weight = more important for overall ranking)
    stat_weights = {
        'PTS': 0.30,    # Points allowed - most important
        'AST': 0.20,    # Assists allowed (shows ball movement)
        'REB': 0.15,    # Rebounds allowed (second chance opportunities)
        'FGM': 0.15,    # Field goals made allowed
        '3PM': 0.10,    # 3-pointers made allowed
        'FTM': 0.05,    # Free throws made allowed
        'FGA': 0.03,    # Field goal attempts allowed
        '3PA': 0.01,    # 3-point attempts allowed
        'FTA': 0.01     # Free throw attempts allowed
    }
    
    all_team_data = {}
    
    print("Fetching comprehensive defensive statistics...")
    
    for stat in stats_to_analyze:
        print(f"  Analyzing {stat} defense...")
        
        # Get rankings for this statistic
        rankings = get_team_defense_rankings_single_stat(stat)
        
        if rankings:
            # Store the data for each team
            for rank, team, value in rankings:
                if team not in all_team_data:
                    all_team_data[team] = {}
                all_team_data[team][stat] = {
                    'rank': rank,
                    'value': value,
                    'total_teams': len(rankings)
                }
        
        # Small delay to be respectful to the server
        time.sleep(1)
    
    # Calculate composite scores
    composite_rankings = calculate_composite_rankings(all_team_data, stat_weights)
    
    return composite_rankings, all_team_data

def get_team_defense_rankings_single_stat(statistic):
    """
    Get team defense rankings for a single statistic
    """
    # Map player stats to team defensive stats (using the same mapping as the working scraper)
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
    
    # Use the same URL pattern as the working scraper
    url = f"https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-{team_stat}-per-game-this-season"
    
    if not url:
        print(f"No URL found for statistic: {statistic}")
        return []
    
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
        
        # Based on the headers, team names are in column 2, defensive stats in column 3 (per-game) or 4 (total)
        team_name_col = 2  # TEAM column
        
        # Based on our debug, we know the structure for all stats:
        # Column 3: OPP [STAT]/GP (per-game stats like 121.23, 29.62, 48.88)
        # Column 4: OPP [STAT] (total stats like 9,941, 2,429, 4,008)
        # We want per-game stats, so use column 3
        
        # Map player stats to defensive stat column names
        stat_column_map = {
            'PTS': 'OPP PTS/GP',
            'AST': 'OPP AST/GP', 
            'REB': 'OPP REB/GP',
            'STL': 'OPP STL/GP',
            'BLK': 'OPP BLK/GP',
            '3PM': 'OPP 3PM/GP',
            'FTM': 'OPP FTM/GP',
            'TOV': 'OPP TOV/GP',
            'FGM': 'OPP FGM/GP',
            'FGA': 'OPP FGA/GP',
            '3PA': 'OPP 3PA/GP',
            'FTA': 'OPP FTA/GP'
        }
        
        # Find the correct per-game column
        expected_per_game_col = stat_column_map.get(statistic, f'OPP {statistic}/GP')
        if expected_per_game_col in headers:
            def_stat_col = headers.index(expected_per_game_col)
            print(f"Using per-game stats from column {def_stat_col} ({expected_per_game_col})")
        else:
            # Fallback to column 3 (which should always be the per-game column)
            def_stat_col = 3
            print(f"Using fallback column {def_stat_col} for {statistic}")
        
        # Extract rows
        rows = table.find_all('tr')[1:]  # Skip header row
        raw_rankings = []
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) > max(team_name_col, def_stat_col):
                try:
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
                    
                    # Clean value by removing commas and converting to float
                    try:
                        # Remove commas and any extra whitespace
                        clean_value = value.replace(',', '').strip()
                        float_value = float(clean_value)
                        if team_name and len(team_name) > 2:  # Only add if we have a meaningful team name
                            raw_rankings.append((team_name, float_value))
                    except ValueError:
                        print(f"  Skipping non-numeric value: '{value}' for team '{team_name}'")
                        continue  # Skip non-numeric values
                except Exception as e:
                    print(f"  Error processing row {i}: {e}")
                    continue
        
        # Sort by value (worst defense first) and assign proper ranks
        raw_rankings.sort(key=lambda x: x[1], reverse=True)
        rankings = []
        for i, (team_name, value) in enumerate(raw_rankings):
            rankings.append((i + 1, team_name, value))  # Fix order: (rank, team, value)
        
        print(f"  Found {len(rankings)} teams for {statistic}")
        if rankings:
            print(f"  Sample: {rankings[0]}")  # Show first ranking
        
        return rankings
        
    except Exception as e:
        print(f"Error fetching {statistic} rankings: {e}")
        return []

def clean_team_name(team_name):
    """
    Clean and standardize team names
    """
    # Remove common suffixes and clean up
    team_name = re.sub(r'\s*\([^)]*\)', '', team_name)  # Remove parentheses
    team_name = team_name.strip()
    
    # Team abbreviation mapping
    team_mapping = {
        'Atlanta Hawks': 'Hawks',
        'Boston Celtics': 'Celtics',
        'Brooklyn Nets': 'Nets',
        'Charlotte Hornets': 'Hornets',
        'Chicago Bulls': 'Bulls',
        'Cleveland Cavaliers': 'Cavaliers',
        'Dallas Mavericks': 'Mavericks',
        'Denver Nuggets': 'Nuggets',
        'Detroit Pistons': 'Pistons',
        'Golden State Warriors': 'Warriors',
        'Houston Rockets': 'Rockets',
        'Indiana Pacers': 'Pacers',
        'LA Clippers': 'Clippers',
        'Los Angeles Clippers': 'Clippers',
        'LA Lakers': 'Lakers',
        'Los Angeles Lakers': 'Lakers',
        'Memphis Grizzlies': 'Grizzlies',
        'Miami Heat': 'Heat',
        'Milwaukee Bucks': 'Bucks',
        'Minnesota Timberwolves': 'Timberwolves',
        'New Orleans Pelicans': 'Pelicans',
        'New York Knicks': 'Knicks',
        'Oklahoma City Thunder': 'Thunder',
        'Orlando Magic': 'Magic',
        'Philadelphia 76ers': '76ers',
        'Phoenix Suns': 'Suns',
        'Portland Trail Blazers': 'Trail Blazers',
        'Sacramento Kings': 'Kings',
        'San Antonio Spurs': 'Spurs',
        'Toronto Raptors': 'Raptors',
        'Utah Jazz': 'Jazz',
        'Washington Wizards': 'Wizards'
    }
    
    return team_mapping.get(team_name, team_name)

def extract_numeric_value(value_text):
    """
    Extract numeric value from text
    """
    try:
        # Remove any non-numeric characters except decimal points
        cleaned = re.sub(r'[^\d.]', '', value_text)
        if cleaned:
            return float(cleaned)
    except:
        pass
    return None

def calculate_composite_rankings(team_data, weights):
    """
    Calculate composite defensive rankings based on multiple statistics
    """
    composite_scores = {}
    
    for team, stats in team_data.items():
        total_score = 0
        total_weight = 0
        
        for stat, weight in weights.items():
            if stat in stats:
                try:
                    # Normalize the rank (1 = worst, higher = better)
                    rank = int(stats[stat]['rank'])  # Ensure rank is an integer
                    total_teams = int(stats[stat]['total_teams'])  # Ensure total_teams is an integer
                    
                    # Convert rank to a score (1 = worst defense, 30 = best defense)
                    # For defensive stats, we want teams that allow MORE to be ranked WORSE
                    normalized_score = (total_teams - rank + 1) / total_teams
                    
                    total_score += normalized_score * weight
                    total_weight += weight
                except (ValueError, TypeError) as e:
                    print(f"Error processing {stat} for {team}: {e}")
                    continue
        
        if total_weight > 0:
            # Average score weighted by importance
            composite_scores[team] = total_score / total_weight
        else:
            composite_scores[team] = 0
    
    # Sort by composite score (lower = worse defense)
    sorted_teams = sorted(composite_scores.items(), key=lambda x: x[1])
    
    # Create final rankings
    rankings = []
    for i, (team, score) in enumerate(sorted_teams, 1):
        rankings.append((i, str(team), score))  # Ensure team is a string
    
    return rankings

def print_comprehensive_rankings():
    """
    Print comprehensive defensive rankings
    """
    print("=" * 80)
    print("COMPREHENSIVE OFFENSIVE PRODUCTION ALLOWED RANKINGS")
    print("=" * 80)
    print("Ranking teams by how much offensive production they allow")
    print("(Lower rank = allows more offensive production from opponents)")
    print()
    
    composite_rankings, detailed_data = get_comprehensive_defense_rankings()
    
    if not composite_rankings:
        print("No data available")
        return
    
    print("OVERALL OFFENSIVE PRODUCTION ALLOWED (Worst to Best):")
    print("-" * 60)
    
    for rank, team, score in composite_rankings:
        print(f"{rank:2d}. {team:15s} (Score: {score:.3f})")
    
    print()
    print("DETAILED BREAKDOWN BY STATISTIC:")
    print("-" * 60)
    
    # Show detailed breakdown for each team
    for rank, team, score in composite_rankings[:10]:  # Top 10 teams that allow most offensive production
        print(f"\n{rank}. {team} (Overall Score: {score:.3f})")
        print("   Individual Rankings:")
        
        if team in detailed_data:
            for stat, data in detailed_data[team].items():
                stat_rank = data['rank']
                stat_value = data['value']
                total_teams = data['total_teams']
                print(f"     {stat:3s}: #{stat_rank:2d}/{total_teams} ({stat_value:.2f})")

if __name__ == "__main__":
    print_comprehensive_rankings() 