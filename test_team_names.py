#!/usr/bin/env python3
"""
Test script to debug team name extraction from StatMuse
"""

from team_defense_scraper import get_team_defense_rankings

def test_team_extraction():
    """Test team name extraction for different statistics"""
    
    print("=== Testing Team Name Extraction ===\n")
    
    # Test with rebounds
    print("Testing REB (rebounds):")
    rankings = get_team_defense_rankings('REB')
    
    if rankings:
        print(f"\nFound {len(rankings)} teams:")
        for i, (team, value, rank) in enumerate(rankings[:10]):  # Show top 10
            print(f"  {rank}. {team}: {value:.2f}")
    else:
        print("No rankings found!")
    
    print("\n" + "="*50 + "\n")
    
    # Test with points
    print("Testing PTS (points):")
    rankings = get_team_defense_rankings('PTS')
    
    if rankings:
        print(f"\nFound {len(rankings)} teams:")
        for i, (team, value, rank) in enumerate(rankings[:10]):  # Show top 10
            print(f"  {rank}. {team}: {value:.2f}")
    else:
        print("No rankings found!")

if __name__ == "__main__":
    test_team_extraction() 