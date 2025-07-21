#!/usr/bin/env python3
"""
Test script to check team defense rankings for all statistics
"""

from team_defense_scraper import get_team_defense_rankings

def test_all_statistics():
    """Test team defense rankings for all available statistics"""
    
    # All the statistics that should work
    statistics = [
        'PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FTM', 'TOV', 
        'FGM', 'FGA', '3PA', 'FTA'
    ]
    
    print("=== Testing Team Defense Rankings for All Statistics ===\n")
    
    for stat in statistics:
        print(f"Testing {stat} (points/rebounds/assists/etc):")
        rankings = get_team_defense_rankings(stat)
        
        if rankings:
            print(f"✅ SUCCESS: Found {len(rankings)} teams")
            print(f"   Top 5 teams that give up the most {stat}:")
            for i, (team, value, rank) in enumerate(rankings[:5]):
                print(f"     {rank}. {team}: {value:.2f}")
        else:
            print(f"❌ FAILED: No rankings found for {stat}")
        
        print()

if __name__ == "__main__":
    test_all_statistics() 