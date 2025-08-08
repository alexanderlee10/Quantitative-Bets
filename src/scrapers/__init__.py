"""
Data scraping modules for fetching sports statistics.
"""

from .datascrapper import geturl, scrape_statmuse
from .teamstatscraper import *
from .team_defense_scraper import get_defense_analysis, get_team_defense_rankings
