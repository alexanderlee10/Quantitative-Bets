import requests
from bs4 import BeautifulSoup
import time
import re
from team_defense_scraper import get_team_defense_rankings

def get_stat_from_statmuse(url, stat_name):
    """Scrape a stat from a StatMuse table and return {team: value}"""
    print(f"Scraping {stat_name} from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    if not table:
        print(f"No table found for {stat_name}")
        return {}
    
    # Extract headers to find the correct column
    headers = [header.get_text(strip=True) for header in table.find_all('th')]
    print(f"Headers for {stat_name}: {headers}")
    
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
    expected_per_game_col = stat_column_map.get(stat_name, f'OPP {stat_name}/GP')
    if expected_per_game_col in headers:
        stat_col = headers.index(expected_per_game_col)
        print(f"Using per-game stats from column {stat_col} ({expected_per_game_col}) for {stat_name}")
    else:
        # Fallback to column 3 (which should always be the per-game column)
        stat_col = 3
        print(f"Using fallback column {stat_col} for {stat_name}")
    
    rows = table.find_all('tr')[1:]  # skip header
    stat_dict = {}
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) <= stat_col or len(cells) < 3:
            continue
        team = cells[2].get_text(strip=True)
        try:
            # Clean value by removing commas and converting to float
            value_text = cells[stat_col].get_text(strip=True)
            clean_value = value_text.replace(',', '').strip()
            value = float(clean_value)
            print(f"Extracted: {team} -> {value}")
            stat_dict[team] = value
        except ValueError:
            print(f"Could not parse value '{value_text}' for {team} in {stat_name}")
            continue
    print(f"Found {len(stat_dict)} teams for {stat_name}")
    return stat_dict

def get_pra_team_rankings():
    """Get PRA allowed for each team by summing PTS, REB, AST allowed from StatMuse links."""
    pts_url = 'https://www.statmuse.com/nba/ask/nba-teams-who-give-up-the-most-points'
    ast_url = 'https://www.statmuse.com/nba/ask/nba-teams-who-give-up-most-assists-this-season'
    reb_url = 'https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-rebounds-and-points-per-game-this-season'
    pts = get_stat_from_statmuse(pts_url, 'PTS')
    ast = get_stat_from_statmuse(ast_url, 'AST')
    reb = get_stat_from_statmuse(reb_url, 'REB')
    
    all_teams = set(pts.keys()) | set(ast.keys()) | set(reb.keys())
    pra_list = []
    for team in all_teams:
        note = ''
        missing = []
        p = pts.get(team)
        r = reb.get(team)
        a = ast.get(team)
        if p is None:
            missing.append('PTS')
        if r is None:
            missing.append('REB')
        if a is None:
            missing.append('AST')
        if missing:
            note = f"Missing: {', '.join(missing)}"
        total = sum(x for x in [p, r, a] if x is not None)
        pra_list.append((team, total, note))
    pra_list.sort(key=lambda x: x[1], reverse=True)
    return pra_list

def get_general_combined_team_rankings(components, url_map):
    """
    For any set of components (e.g., ['PTS', 'REB', 'AST']),
    scrape each stat from url_map, sum for each team, and note missing components.
    url_map: dict like {'PTS': url, 'REB': url, ...}
    Returns: sorted list of (team, total, note)
    """
    stat_dicts = {}
    for comp in components:
        url = url_map.get(comp)
        if url:
            stat_dicts[comp] = get_stat_from_statmuse(url, comp)
        else:
            stat_dicts[comp] = {}
    all_teams = set()
    for d in stat_dicts.values():
        all_teams |= set(d.keys())
    combined_list = []
    for team in all_teams:
        note = ''
        missing = []
        total = 0
        for comp in components:
            val = stat_dicts[comp].get(team)
            if val is None:
                missing.append(comp)
            else:
                total += val
        if missing:
            note = f"Missing: {', '.join(missing)}"
        combined_list.append((team, total, note))
    combined_list.sort(key=lambda x: x[1], reverse=True)
    return combined_list

def print_pra_team_rankings():
    pra_list = get_pra_team_rankings()
    print("TEAM PRA ALLOWED (PTS+REB+AST):")
    for i, (team, pra, note) in enumerate(pra_list, 1):
        if note:
            print(f"{i:2d}. {team:20s} PRA: {pra:.2f}  [{note}]")
        else:
            print(f"{i:2d}. {team:20s} PRA: {pra:.2f}")

def get_combined_stats_rankings(stat_combination):
    """
    Get combined statistics rankings by adding individual stat rankings
    stat_combination: list of stats to combine (e.g., ['PTS', 'REB'] for PTS + REB)
    """
    print(f"Analyzing combined stats: {' + '.join(stat_combination)}")
    
    # Map component abbreviations to URL-friendly names
    component_url_map = {
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
    
    # Create URLs for individual components
    stat_url_template = 'https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-{}-per-game-this-season'
    url_map = {comp: stat_url_template.format(component_url_map.get(comp, comp.lower())) for comp in stat_combination}
    
    # Use the corrected function that uses individual URLs
    combined_list = get_general_combined_team_rankings(stat_combination, url_map)
    
    # Convert to the format expected by the rest of the code
    all_team_data = {}
    combined_rankings = []
    
    for i, (team, value, note) in enumerate(combined_list, 1):
        combined_rankings.append((i, team, value))
        
        # Also create the detailed data structure
        if team not in all_team_data:
            all_team_data[team] = {}
        all_team_data[team]['combined'] = {
            'rank': i,
            'value': value,
            'total_teams': len(combined_list)
        }
    
    return combined_rankings, all_team_data

def calculate_combined_rankings(team_data, stat_combination):
    """
    Calculate combined rankings by adding individual stat values
    """
    combined_scores = {}
    
    for team, stats in team_data.items():
        total_value = 0
        available_stats = 0
        
        for stat in stat_combination:
            if stat in stats:
                total_value += stats[stat]['value']
                available_stats += 1
        
        if available_stats > 0:
            # Average the values for fair comparison
            combined_scores[team] = total_value / available_stats
        else:
            combined_scores[team] = 0
    
    # Sort by combined value (higher = worse defense, allows more)
    sorted_teams = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Create final rankings
    rankings = []
    for i, (team, combined_value) in enumerate(sorted_teams, 1):
        rankings.append((i, team, combined_value))
    
    return rankings

def print_combined_rankings(stat_combination):
    """
    Print combined statistics rankings
    """
    combination_name = ' + '.join(stat_combination)
    
    print("=" * 80)
    print(f"COMBINED STATISTICS RANKINGS: {combination_name}")
    print("=" * 80)
    print(f"Ranking teams by combined {combination_name} allowed")
    print("(Lower rank = allows more combined offensive production)")
    print()
    
    combined_rankings, detailed_data = get_combined_stats_rankings(stat_combination)
    
    if not combined_rankings:
        print("No data available")
        return
    
    print(f"COMBINED {combination_name} RANKINGS (Worst to Best):")
    print("-" * 60)
    
    for rank, team, combined_value in combined_rankings:
        print(f"{rank:2d}. {team:15s} (Combined: {combined_value:.2f})")
    
    print()
    print("DETAILED BREAKDOWN BY INDIVIDUAL STATISTIC:")
    print("-" * 60)
    
    # Show detailed breakdown for top 10 teams
    for rank, team, combined_value in combined_rankings[:10]:
        print(f"\n{rank}. {team} (Combined {combination_name}: {combined_value:.2f})")
        print("   Individual Values:")
        
        if team in detailed_data:
            for stat in stat_combination:
                if stat in detailed_data[team]:
                    data = detailed_data[team][stat]
                    stat_rank = data['rank']
                    stat_value = data['value']
                    total_teams = data['total_teams']
                    print(f"     {stat:3s}: #{stat_rank:2d}/{total_teams} ({stat_value:.2f})")

def analyze_multiple_combinations():
    """
    Analyze multiple combined statistics
    """
    combinations = [
        ['PTS', 'REB'],           # Points + Rebounds
        ['PTS', 'AST'],           # Points + Assists
        ['PTS', 'REB', 'AST'],    # Points + Rebounds + Assists
        ['PTS', 'FGM'],           # Points + Field Goals Made
        ['PTS', '3PM'],           # Points + 3-Pointers Made
        ['PTS', 'FTM'],           # Points + Free Throws Made
        ['REB', 'AST'],           # Rebounds + Assists
        ['FGM', '3PM', 'FTM'],    # All Shooting Stats
        ['PTS', 'REB', 'AST', 'FGM'],  # Comprehensive Offense
    ]
    
    for combination in combinations:
        print_combined_rankings(combination)
        print("\n" + "="*80 + "\n")

def interactive_combination_analyzer():
    """
    Interactive analyzer for custom combinations
    """
    print("=" * 80)
    print("INTERACTIVE COMBINED STATISTICS ANALYZER")
    print("=" * 80)
    print("Available statistics: PTS, REB, AST, FGM, 3PM, FTM, FGA, 3PA, FTA")
    print("Enter statistics separated by spaces (e.g., 'PTS REB' for PTS + REB)")
    print("Type 'quit' to exit")
    print()
    
    while True:
        user_input = input("Enter statistics to combine: ").strip().upper()
        
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            continue
        
        # Parse the input
        stats = user_input.split()
        
        # Validate stats
        valid_stats = ['PTS', 'REB', 'AST', 'FGM', '3PM', 'FTM', 'FGA', '3PA', 'FTA']
        invalid_stats = [stat for stat in stats if stat not in valid_stats]
        
        if invalid_stats:
            print(f"Invalid statistics: {', '.join(invalid_stats)}")
            print(f"Valid options: {', '.join(valid_stats)}")
            continue
        
        if len(stats) < 2:
            print("Please enter at least 2 statistics to combine")
            continue
        
        print()
        print_combined_rankings(stats)
        print()

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Analyze predefined combinations")
    print("2. Interactive custom combinations")
    print("3. Print PRA allowed teams")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        analyze_multiple_combinations()
    elif choice == "2":
        interactive_combination_analyzer()
    elif choice == "3":
        print_pra_team_rankings()
    else:
        print("Invalid choice. Running predefined combinations...")
        analyze_multiple_combinations() 