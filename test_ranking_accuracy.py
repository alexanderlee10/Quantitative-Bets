#!/usr/bin/env python3
"""
Test script to verify ranking accuracy
"""

from team_defense_scraper import get_team_defense_rankings

def test_ranking_accuracy():
    """Test ranking accuracy for different statistics"""
    
    print("=== Testing Ranking Accuracy ===\n")
    
    # Test with points
    statistic = "PTS"
    print(f"Testing {statistic} rankings:")
    
    rankings = get_team_defense_rankings(statistic)
    
    if rankings:
        print(f"\n✅ Found {len(rankings)} teams")
        print(f"Total teams should be 30 (NBA has 30 teams)")
        
        print(f"\nTop 10 worst defenses:")
        for i, (team, value, rank) in enumerate(rankings[:10]):
            print(f"  {rank}. {team}: {value:.2f}")
        
        print(f"\nBottom 10 best defenses:")
        for i, (team, value, rank) in enumerate(rankings[-10:]):
            print(f"  {rank}. {team}: {value:.2f}")
        
        # Check for any ranking issues
        print(f"\n🔍 Ranking Analysis:")
        print(f"  - Highest value: {rankings[0][1]:.2f} ({rankings[0][0]})")
        print(f"  - Lowest value: {rankings[-1][1]:.2f} ({rankings[-1][0]})")
        print(f"  - Rank 1 should be: {rankings[0][0]} (worst defense)")
        print(f"  - Rank {len(rankings)} should be: {rankings[-1][0]} (best defense)")
        
        # Verify ranking order
        values = [rank[1] for rank in rankings]
        is_descending = all(values[i] >= values[i+1] for i in range(len(values)-1))
        print(f"  - Rankings in descending order: {'✅' if is_descending else '❌'}")
        
    else:
        print("❌ No rankings found")

if __name__ == "__main__":
    test_ranking_accuracy() 