#!/usr/bin/env python3
"""
Quick Start Script for Quantitative Bets
=======================================

This script provides a simple way to test the multi-sport dashboard
without going through the main menu.
"""

import sys
import os
import subprocess

def quick_start():
    """Quick start the multi-sport dashboard"""
    print("🚀 Quick Starting Multi-Sport Dashboard...")
    print("=" * 50)
    
    try:
        # Method 1: Try to run the dashboard directly from its location
        dashboard_path = os.path.join('src', 'dashboards', 'multi_sport_dashboard.py')
        if os.path.exists(dashboard_path):
            print("✅ Found dashboard file, launching...")
            subprocess.run([sys.executable, dashboard_path])
            return
        else:
            print(f"❌ Dashboard file not found at: {dashboard_path}")
            
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        print("\n🔧 Manual instructions:")
        print("1. Open terminal/command prompt")
        print("2. Navigate to the project directory")
        print("3. Run: cd src/dashboards")
        print("4. Run: python multi_sport_dashboard.py")
        
    print("\n📊 Dashboard Features:")
    print("- Multi-sport support (NBA, NFL, NHL, WNBA)")
    print("- Real-time data scraping from StatMuse")
    print("- Advanced statistical analysis")
    print("- Color-coded performance indicators")
    print("- Probability calculations and betting recommendations")

if __name__ == "__main__":
    quick_start()
