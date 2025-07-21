#!/usr/bin/env python3
"""
Test script to verify dashboard fixes work correctly
"""

from datascrapper import scrape_statmuse
from enhanced_plot import create_enhanced_dashboard
from simplemean import simple_mean
from WMA import weighted_moving_average

def test_dashboard_fix():
    """Test the dashboard with a real player to verify fixes"""
    
    print("=== Testing Dashboard Fixes ===\n")
    
    # Test with a real player
    player_name = "LeBron James"
    statistic = "PTS"
    
    print(f"Testing with: {player_name} - {statistic}")
    
    # Get player data
    url = f"https://www.statmuse.com/nba/ask/{player_name.lower().replace(' ', '-')}-stats-in-last-25-regular-season-games"
    player_data = scrape_statmuse(url)
    if not player_data or len(player_data) < 2:
        print("❌ No player data found")
        return
    
    print(f"✅ Found {len(player_data)-1} games for {player_name}")
    
    # Calculate projections
    try:
        quantitative = simple_mean(player_data, statistic)
        projection = weighted_moving_average(player_data, statistic)
        
        print(f"✅ Mean: {quantitative:.2f}")
        print(f"✅ Projection: {projection:.2f}")
        
        # Create dashboard
        print("\n🎯 Creating Enhanced Dashboard...")
        create_enhanced_dashboard(player_data, statistic, projection, quantitative, player_name)
        
        print("\n✅ Dashboard should now show:")
        print("  📊 Team Defense Rankings (worst first)")
        print("  📈 Opponent Analysis with detailed info")
        print("  🎯 Clear team names and values")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_dashboard_fix() 