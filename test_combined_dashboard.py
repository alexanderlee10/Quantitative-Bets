from Integrated_Dashboard import IntegratedDashboard

def test_combined_stats():
    """Test if the dashboard can handle combined statistics"""
    dashboard = IntegratedDashboard()
    
    # Test combined statistic detection
    print("Testing combined statistic detection:")
    print(f"PRA is combined: {dashboard.is_combined_statistic('PRA')}")
    print(f"PR is combined: {dashboard.is_combined_statistic('PR')}")
    print(f"PTS is combined: {dashboard.is_combined_statistic('PTS')}")
    
    # Test component extraction
    print("\nTesting component extraction:")
    print(f"PRA components: {dashboard.get_combined_stat_components('PRA')}")
    print(f"PR components: {dashboard.get_combined_stat_components('PR')}")
    print(f"PRA+ components: {dashboard.get_combined_stat_components('PRA+')}")
    
    print("\nCombined statistics supported:")
    print("- PRA (Points + Rebounds + Assists)")
    print("- PR (Points + Rebounds)")
    print("- PA (Points + Assists)")
    print("- RA (Rebounds + Assists)")
    print("- PRA+ (Points + Rebounds + Assists + Field Goals Made)")
    print("- SHOOTING (Field Goals Made + 3-Pointers Made + Free Throws Made)")

if __name__ == "__main__":
    test_combined_stats() 