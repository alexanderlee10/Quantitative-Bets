#!/usr/bin/env python3
"""
Demo script for the Enhanced NBA Betting Dashboard
This script demonstrates the key features of the enhanced dashboard
"""

from enhanced_plot import create_enhanced_dashboard, plot_team_defense_comparison
from team_defense_scraper import get_team_defense_rankings, get_defense_analysis
from datascrapper import geturl, scrape_statmuse
from NBBBA import clean_nba_data
from simplemean import simple_mean

def demo_player_analysis():
    """Demo function to analyze a player"""
    print("=== NBA Enhanced Betting Dashboard Demo ===\n")
    
    # Example player analysis
    player_name = "LeBron James"
    team = "Any"
    time_duration = "Last 5 Regular Games"
    statistic = "PTS"
    projection = 25.0
    
    print(f"Analyzing {player_name} for {statistic}...")
    
    # Get data
    url = geturl("nba", player_name, team, time_duration)
    print(f"URL: {url}")
    
    data = scrape_statmuse(url)
    if not data:
        print("No data found!")
        return
    
    print(f"Found {len(data)-1} games of data")
    
    # Clean data
    cleaned_data = clean_nba_data(data)
    if not cleaned_data:
        print("Failed to clean data!")
        return
    
    # Calculate mean
    mean_value = simple_mean(cleaned_data, statistic)
    print(f"Mean {statistic}: {mean_value:.2f}")
    
    # Get defense analysis
    defense_analysis = get_defense_analysis(cleaned_data, statistic)
    if defense_analysis:
        print(f"\nOpponent Analysis:")
        print(f"  Next opponent: {defense_analysis['opponent']}")
        print(f"  Defense rank: {defense_analysis['rank']}/{defense_analysis['total_teams']}")
        print(f"  Difficulty: {defense_analysis['difficulty']}")
        print(f"  Allows: {defense_analysis['value_allowed']} {statistic}")
    
    # Generate dashboard
    print("\nGenerating enhanced dashboard...")
    create_enhanced_dashboard(cleaned_data, statistic, projection, mean_value, player_name)

def demo_team_rankings():
    """Demo function to show team defense rankings"""
    print("\n=== Team Defense Rankings Demo ===\n")
    
    statistic = "PTS"
    print(f"Loading team defense rankings for {statistic}...")
    
    rankings = get_team_defense_rankings(statistic)
    if rankings:
        print(f"Found rankings for {len(rankings)} teams:")
        for i, (team, value, rank) in enumerate(rankings[:10]):  # Show top 10
            print(f"  {rank}. {team}: {value}")
    
    # Show the plot
    plot_team_defense_comparison(statistic)

def main():
    """Main demo function"""
    try:
        # Demo 1: Player Analysis
        demo_player_analysis()
        
        # Demo 2: Team Rankings
        demo_team_rankings()
        
        print("\n=== Demo Complete ===")
        print("The enhanced dashboard provides:")
        print("1. Player performance analysis with recent game data")
        print("2. Team defense rankings for the selected statistic")
        print("3. Opponent difficulty assessment")
        print("4. Hit probability calculations")
        print("5. Comprehensive visualizations")
        
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main() 