"""
Quantitative Bets - Sports Analysis Platform
==========================================

A comprehensive sports betting analysis platform with advanced statistical analysis,
real-time data scraping, and interactive dashboards for sports betting decisions.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main components for easy access
try:
    from .dashboards.multi_sport_dashboard import MultiSportDashboard
    from .dashboards.Integrated_Dashboard import IntegratedDashboard
    from .dashboards.Enhanced_Dashboard import EnhancedDashboard
except ImportError:
    # Handle case where modules aren't available
    pass
