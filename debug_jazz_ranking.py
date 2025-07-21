#!/usr/bin/env python3
"""
Debug script to figure out why Jazz ranking is wrong
"""

from team_defense_scraper import get_team_defense_rankings, get_defense_analysis
from datascrapper import scrape_statmuse

def debug_jazz_ranking():
    """Debug why Jazz is showing wrong rank"""
    
    print("=== Debugging Jazz Ranking Issue ===\n")
    
    # Test with points
    statistic = "PTS"
    
    # Get rankings
    rankings = get_team_defense_rankings(statistic)
    
    print("All rankings:")
    for team, value, rank in rankings:
        print(f"  {rank}. {team}: {value:.2f}")
    
    # Find Jazz specifically
    jazz_rank = None
    for team, value, rank in rankings:
        if "Jazz" in team or "UTA" in team:
            jazz_rank = (team, value, rank)
            break
    
    if jazz_rank:
        print(f"\n🎯 Jazz found: {jazz_rank[0]} ranked #{jazz_rank[2]} with {jazz_rank[1]:.2f}")
    else:
        print("\n❌ Jazz not found in rankings")
    
    # Test with sample player data
    print(f"\n=== Testing with sample data ===")
    
    # Create sample data with Jazz as opponent
    sample_data = [
        ['NAME', 'DATE', 'TM', 'OPP', 'PTS'],
        ['LeBron James', '12/01/2024', 'LAL', 'UTA', '25']
    ]
    
    defense_analysis = get_defense_analysis(sample_data, statistic)
    
    if defense_analysis:
        print(f"Opponent: {defense_analysis['opponent']}")
        print(f"Rank: {defense_analysis['rank']}")
        print(f"Total teams: {defense_analysis['total_teams']}")
        print(f"Value allowed: {defense_analysis['value_allowed']}")
    else:
        print("No defense analysis found")

if __name__ == "__main__":
    debug_jazz_ranking() 