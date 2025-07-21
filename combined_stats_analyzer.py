import requests
from bs4 import BeautifulSoup
import time
import re
from team_defense_scraper import get_team_defense_rankings

def get_combined_stats_rankings(stat_combination):
    """
    Get combined statistics rankings by adding individual stat rankings
    stat_combination: list of stats to combine (e.g., ['PTS', 'REB'] for PTS + REB)
    """
    print(f"Analyzing combined stats: {' + '.join(stat_combination)}")
    
    # Get individual rankings for each stat
    all_team_data = {}
    
    for stat in stat_combination:
        print(f"  Fetching {stat} rankings...")
        rankings = get_team_defense_rankings(stat)
        
        if rankings:
            # Store the data for each team
            for team_name, value, rank in rankings:
                if team_name not in all_team_data:
                    all_team_data[team_name] = {}
                all_team_data[team_name][stat] = {
                    'rank': rank,
                    'value': value,
                    'total_teams': len(rankings)
                }
        
        time.sleep(1)  # Be respectful to the server
    
    # Calculate combined scores
    combined_rankings = calculate_combined_rankings(all_team_data, stat_combination)
    
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
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        analyze_multiple_combinations()
    elif choice == "2":
        interactive_combination_analyzer()
    else:
        print("Invalid choice. Running predefined combinations...")
        analyze_multiple_combinations() 