import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import threading
import time

# Import the modules from the integrated dashboard
try:
    # Try relative imports first (when run as package)
    from ..scrapers.datascrapper import geturl, scrape_statmuse
    from ..core.NBBBA import clean_nba_data, get_nba_statistics
    from ..analyzers.simplemean import simple_mean
    from ..analyzers.WMA import weighted_moving_average
    from ..scrapers.team_defense_scraper import get_defense_analysis, get_team_defense_rankings
    from ..analyzers.combined_stats_analyzer import get_combined_stats_rankings, get_general_combined_team_rankings
    INTEGRATED_MODULES_AVAILABLE = True
except ImportError:
    # Fallback to absolute imports (when run directly)
    try:
        import sys
        import os
        
        # Get the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Add the src directory to the path
        src_dir = os.path.join(current_dir, '..')
        project_dir = os.path.join(src_dir, '..')
        
        # Add both src and project root to path
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)
        
        from scrapers.datascrapper import geturl, scrape_statmuse
        from core.NBBBA import clean_nba_data, get_nba_statistics
        from analyzers.simplemean import simple_mean
        from analyzers.WMA import weighted_moving_average
        from scrapers.team_defense_scraper import get_defense_analysis, get_team_defense_rankings
        from analyzers.combined_stats_analyzer import get_combined_stats_rankings, get_general_combined_team_rankings
        INTEGRATED_MODULES_AVAILABLE = True
    except ImportError:
        # Final fallback to direct imports (for backward compatibility)
        try:
            from datascrapper import geturl, scrape_statmuse
            from NBBBA import clean_nba_data, get_nba_statistics
            from simplemean import simple_mean
            from WMA import weighted_moving_average
            from team_defense_scraper import get_defense_analysis, get_team_defense_rankings
            from combined_stats_analyzer import get_combined_stats_rankings, get_general_combined_team_rankings
            INTEGRATED_MODULES_AVAILABLE = True
        except ImportError:
            INTEGRATED_MODULES_AVAILABLE = False
            print("Warning: Some integrated dashboard modules not available. Using sample data.")

class MultiSportDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-Sport Quantitative Betting Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1a1a1a', foreground='white', font=('Arial', 10))
        style.configure('TButton', background='#4a4a4a', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('TCombobox', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        style.configure('TEntry', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        
        # Sport-specific configurations
        self.sports_config = {
            'NBA': {
                'stats': ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FTM', 'TOV', 'PRA', 'PR', 'PA', 'RA'],
                'combined_stats': {
                    'PRA': ['PTS', 'REB', 'AST'],
                    'PR': ['PTS', 'REB'],
                    'PA': ['PTS', 'AST'],
                    'RA': ['REB', 'AST']
                },
                'url_template': 'https://www.statmuse.com/nba/ask/nba-teams-that-give-up-the-most-{}-per-game-this-season',
                'stat_mapping': {
                    'PTS': 'points', 'REB': 'rebounds', 'AST': 'assists', 'STL': 'steals',
                    'BLK': 'blocks', '3PM': '3-pointers', 'FTM': 'free-throws', 'TOV': 'turnovers'
                }
            },
            'NFL': {
                'stats': ['PASS_YDS', 'RUSH_YDS', 'REC_YDS', 'TD', 'INT', 'SACK', 'FUM', 'PRA', 'PR', 'PA'],
                'combined_stats': {
                    'PRA': ['PASS_YDS', 'RUSH_YDS', 'REC_YDS'],
                    'PR': ['PASS_YDS', 'RUSH_YDS'],
                    'PA': ['PASS_YDS', 'REC_YDS']
                },
                'url_template': 'https://www.statmuse.com/nfl/ask/nfl-teams-that-give-up-the-most-{}-per-game-this-season',
                'stat_mapping': {
                    'PASS_YDS': 'passing-yards', 'RUSH_YDS': 'rushing-yards', 'REC_YDS': 'receiving-yards',
                    'TD': 'touchdowns', 'INT': 'interceptions', 'SACK': 'sacks', 'FUM': 'fumbles'
                }
            },
            'NHL': {
                'stats': ['GOALS', 'ASSISTS', 'POINTS', 'PIM', 'SHOTS', 'HITS', 'BLOCKS', 'PRA', 'PA'],
                'combined_stats': {
                    'PRA': ['GOALS', 'ASSISTS', 'POINTS'],
                    'PA': ['GOALS', 'ASSISTS']
                },
                'url_template': 'https://www.statmuse.com/nhl/ask/nhl-teams-that-give-up-the-most-{}-per-game-this-season',
                'stat_mapping': {
                    'GOALS': 'goals', 'ASSISTS': 'assists', 'POINTS': 'points', 'PIM': 'penalty-minutes',
                    'SHOTS': 'shots', 'HITS': 'hits', 'BLOCKS': 'blocks'
                }
            },
            'WNBA': {
                'stats': ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FTM', 'TOV', 'PRA', 'PR', 'PA', 'RA'],
                'combined_stats': {
                    'PRA': ['PTS', 'REB', 'AST'],
                    'PR': ['PTS', 'REB'],
                    'PA': ['PTS', 'AST'],
                    'RA': ['REB', 'AST']
                },
                'url_template': 'https://www.statmuse.com/wnba/ask/wnba-teams-that-give-up-the-most-{}-per-game-this-season',
                'stat_mapping': {
                    'PTS': 'points', 'REB': 'rebounds', 'AST': 'assists', 'STL': 'steals',
                    'BLK': 'blocks', '3PM': '3-pointers', 'FTM': 'free-throws', 'TOV': 'turnovers'
                }
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="Multi-Sport Quantitative Betting Dashboard", 
                              font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='#00ff00')
        title_label.pack(pady=10)
        
        # Create main container
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel for controls
        left_panel = tk.Frame(main_container, bg='#1a1a1a', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel for dashboard
        right_panel = tk.Frame(main_container, bg='#1a1a1a')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.setup_controls(left_panel)
        self.setup_dashboard(right_panel)
        
    def setup_controls(self, parent):
        # Sport Selection
        sport_frame = tk.LabelFrame(parent, text="Sport Selection", fg="white", bg="#1a1a1a", font=("Arial", 12, "bold"))
        sport_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.sport_var = tk.StringVar(value="NBA")
        for sport in self.sports_config.keys():
            tk.Radiobutton(sport_frame, text=sport, variable=self.sport_var, value=sport,
                          fg="white", bg="#1a1a1a", selectcolor="#404040",
                          command=self.on_sport_change).pack(anchor=tk.W, padx=10, pady=2)
        
        # Player Information Section
        player_frame = tk.LabelFrame(parent, text="Player Information", 
                                   font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='white')
        player_frame.pack(fill='x', pady=10, padx=10)
        
        # Player name
        tk.Label(player_frame, text="Player Name:", bg='#1a1a1a', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.player_name_entry = tk.Entry(player_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.player_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Team name
        tk.Label(player_frame, text="Team Name:", bg='#1a1a1a', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.team_name_entry = tk.Entry(player_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.team_name_entry.insert(0, "Any")
        self.team_name_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Time duration
        tk.Label(player_frame, text="Time Duration:", bg='#1a1a1a', fg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.time_duration_var = tk.StringVar(value="Last 5 Regular Games")
        time_duration_combo = ttk.Combobox(player_frame, textvariable=self.time_duration_var, 
                                         values=('Last 5 Regular Games', 'Last 7 Regular Games', 'Last 10 Regular Games', 
                                                'Playoff Game Log', 'Last 5 Playoff Games', 'combined'))
        time_duration_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Configure grid weights
        player_frame.columnconfigure(1, weight=1)
        
        # Statistics & Analysis Section
        analysis_frame = tk.LabelFrame(parent, text="Statistics & Analysis", 
                                     font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='white')
        analysis_frame.pack(fill='x', pady=10, padx=10)
        
        # Statistic selection
        tk.Label(analysis_frame, text="Statistic:", bg='#1a1a1a', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.statistic_var = tk.StringVar(value="PTS")
        self.statistic_combo = ttk.Combobox(analysis_frame, textvariable=self.statistic_var, 
                                          values=self.get_available_stats())
        self.statistic_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Projection
        tk.Label(analysis_frame, text="Projection:", bg='#1a1a1a', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.projection_entry = tk.Entry(analysis_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.projection_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Quantitative analysis
        tk.Label(analysis_frame, text="Analysis Method:", bg='#1a1a1a', fg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.quantitative_var = tk.StringVar(value="Mean")
        quantitative_combo = ttk.Combobox(analysis_frame, textvariable=self.quantitative_var, 
                                        values=('Mean', 'WMA'))
        quantitative_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Configure grid weights
        analysis_frame.columnconfigure(1, weight=1)
        
        # Submit Button Section
        button_frame = tk.Frame(parent, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=20)
        
        # Submit button
        self.submit_btn = tk.Button(button_frame, text="Generate Dashboard", 
                                  command=self.generate_dashboard, 
                                  bg='#00aa00', fg='white', font=('Arial', 14, 'bold'),
                                  height=2, width=25)
        self.submit_btn.pack(expand=True, pady=20)
        
        # Status Section
        status_frame = tk.LabelFrame(parent, text="Status", 
                                   font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='white')
        status_frame.pack(fill='x', pady=10, padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready - Enter player name to start")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, 
                                   bg='#1a1a1a', fg='#ffff00', font=('Arial', 10), wraplength=350)
        self.status_label.pack(pady=10, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
    def setup_dashboard(self, parent):
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 8), facecolor='#1a1a1a')
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Show placeholder
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder when no data is available"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor('#1a1a1a')
        ax.text(0.5, 0.5, 'Click "Generate Dashboard" to see the analysis', 
               ha='center', va='center', transform=ax.transAxes, 
               fontsize=16, color='white')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
        
    def on_sport_change(self):
        # Update available statistics based on selected sport
        self.statistic_combo['values'] = self.get_available_stats()
        self.statistic_var.set(self.get_available_stats()[0])  # Set to first available stat
        
    def get_available_stats(self):
        sport = self.sport_var.get()
        return self.sports_config[sport]['stats']
        
    def generate_dashboard(self):
        """Generate the dashboard when submit button is clicked"""
        self.submit_btn.config(state='disabled')
        self.status_var.set("Generating dashboard...")
        self.progress.start()
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=self._generate_dashboard_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_dashboard_thread(self):
        """Thread function for generating dashboard"""
        try:
            # Get input values
            sport = self.sport_var.get()
            player_name = self.player_name_entry.get().strip()
            team = self.team_name_entry.get().strip()
            time_duration = self.time_duration_var.get()
            statistic = self.statistic_var.get()
            
            try:
                projection = float(self.projection_entry.get())
            except ValueError:
                self.root.after(0, lambda: self.status_var.set("ERROR: Please enter a valid projection number"))
                return
                
            quantitative_analysis = self.quantitative_var.get()
            
            if not player_name:
                self.root.after(0, lambda: self.status_var.set("ERROR: Please enter a player name"))
                return
                
            # Update status
            self.root.after(0, lambda: self.status_var.set(f"Fetching data for {player_name}..."))
            
            # Get data based on availability of integrated modules
            if INTEGRATED_MODULES_AVAILABLE and sport == "NBA":
                # Use real data scraping for NBA
                url = geturl("nba", player_name, team, time_duration)
                data = scrape_statmuse(url)
                
                if not data:
                    self.root.after(0, lambda: self.status_var.set("ERROR: No data found for this player"))
                    return
                    
                player_data = clean_nba_data(data)
            else:
                # Use sample data for other sports or when modules not available
                player_data = self.get_sample_data(sport, player_name)
            
            if not player_data or len(player_data) < 2:
                self.root.after(0, lambda: self.status_var.set("ERROR: No valid data found"))
                return
                
            # Calculate quantitative value
            if quantitative_analysis == "WMA":
                quantitative_value = self.calculate_wma(player_data, statistic)
            else:
                quantitative_value = self.calculate_quantitative(player_data, statistic, "Mean")
            
            # Get defense analysis
            defense_analysis = self.get_defense_analysis(sport, player_data, statistic)
            
            # Create dashboard
            self.root.after(0, lambda: self.create_dashboard(player_data, statistic, projection, quantitative_value, player_name, defense_analysis, sport))
            
            # Update status
            self.root.after(0, lambda: self.status_var.set(f"Dashboard generated successfully for {player_name} ({sport})"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_var.set(f"ERROR: {error_msg}"))
        finally:
            self.root.after(0, lambda: self.submit_btn.config(state='normal'))
            self.root.after(0, self.progress.stop)
            
    def is_combined_statistic(self, statistic):
        """Check if statistic is a combined statistic"""
        return '+' in statistic or statistic in ['PRA', 'PR', 'PA', 'RA']
        
    def get_combined_stat_components(self, statistic):
        """Get components for combined statistics"""
        sport = self.sport_var.get()
        if statistic in self.sports_config[sport]['combined_stats']:
            return self.sports_config[sport]['combined_stats'][statistic]
        elif '+' in statistic:
            return [comp.strip() for comp in statistic.split('+')]
        return [statistic]
        
    def calculate_wma(self, player_data, statistic):
        """Calculate Weighted Moving Average"""
        if not INTEGRATED_MODULES_AVAILABLE:
            return self.calculate_quantitative(player_data, statistic, "Mean")
            
        header = player_data[0]
        
        if self.is_combined_statistic(statistic):
            components = self.get_combined_stat_components(statistic)
            combined_values = []
            
            for game in player_data[1:]:
                game_total = 0
                for comp in components:
                    try:
                        comp_index = header.index(comp)
                        game_total += float(game[comp_index])
                    except (ValueError, IndexError):
                        continue
                combined_values.append(game_total)
            values = combined_values
        else:
            try:
                stat_index = header.index(statistic)
                values = [float(game[stat_index]) for game in player_data[1:] if game[stat_index]]
            except (ValueError, IndexError):
                return 0
                
        if not values:
            return 0
            
        return weighted_moving_average(values)
        
    def get_sample_data(self, sport, player_name):
        """Generate sample data for the selected sport"""
        if sport == "NBA":
            return [
                ['', '', 'NAME', 'DATE', 'TM', '', 'OPP', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'TS%', 'OREB', 'DREB', 'TOV', 'PF', '+/-'],
                ['1', '', 'Stephen CurryS. Curry', '2/13/2025', 'GSW', '@', 'HOU', '35', '27', '5', '3', '0', '0', '7', '17', '41.2', '5', '13', '38.5', '8', '9', '88.9', '64.4', '1', '4', '1', '2', '+7'],
                ['2', '', 'Stephen CurryS. Curry', '2/21/2025', 'GSW', '@', 'SAC', '31', '20', '1', '6', '2', '0', '7', '13', '53.8', '4', '9', '44.4', '2', '2', '100.0', '72.0', '0', '1', '1', '0', '0'],
                ['3', '', 'Stephen CurryS. Curry', '2/23/2025', 'GSW', 'vs', 'DAL', '29', '30', '4', '7', '1', '0', '12', '20', '60.0', '3', '8', '37.5', '3', '3', '100.0', '70.4', '0', '4', '2', '3', '+14'],
                ['4', '', 'Stephen CurryS. Curry', '2/25/2025', 'GSW', 'vs', 'CHA', '24', '15', '4', '6', '1', '0', '6', '14', '42.9', '2', '9', '22.2', '1', '1', '100.0', '51.9', '0', '4', '2', '2', '+26'],
                ['5', '', 'Stephen CurryS. Curry', '2/27/2025', 'GSW', '@', 'ORL', '34', '56', '4', '3', '2', '0', '16', '25', '64.0', '12', '19', '63.2', '12', '12', '100.0', '92.5', '0', '4', '4', '0', '+15']
            ]
        elif sport == "NFL":
            return [
                ['', '', 'NAME', 'DATE', 'TM', '', 'OPP', 'PASS_YDS', 'RUSH_YDS', 'REC_YDS', 'TD', 'INT', 'SACK', 'FUM'],
                ['1', '', 'Patrick MahomesP. Mahomes', '2/13/2025', 'KC', '@', 'HOU', '285', '15', '0', '3', '0', '2', '0'],
                ['2', '', 'Patrick MahomesP. Mahomes', '2/21/2025', 'KC', '@', 'BUF', '320', '25', '0', '2', '1', '1', '0'],
                ['3', '', 'Patrick MahomesP. Mahomes', '2/23/2025', 'KC', 'vs', 'BAL', '298', '12', '0', '4', '0', '3', '1'],
                ['4', '', 'Patrick MahomesP. Mahomes', '2/25/2025', 'KC', 'vs', 'CIN', '275', '18', '0', '2', '1', '2', '0'],
                ['5', '', 'Patrick MahomesP. Mahomes', '2/27/2025', 'KC', '@', 'NE', '310', '22', '0', '3', '0', '1', '0']
            ]
        elif sport == "NHL":
            return [
                ['', '', 'NAME', 'DATE', 'TM', '', 'OPP', 'GOALS', 'ASSISTS', 'POINTS', 'PIM', 'SHOTS', 'HITS', 'BLOCKS'],
                ['1', '', 'Connor McDavidC. McDavid', '2/13/2025', 'EDM', '@', 'CGY', '1', '2', '3', '0', '4', '1', '0'],
                ['2', '', 'Connor McDavidC. McDavid', '2/21/2025', 'EDM', '@', 'VAN', '0', '3', '3', '2', '3', '0', '1'],
                ['3', '', 'Connor McDavidC. McDavid', '2/23/2025', 'EDM', 'vs', 'TOR', '2', '1', '3', '0', '5', '1', '0'],
                ['4', '', 'Connor McDavidC. McDavid', '2/25/2025', 'EDM', 'vs', 'WPG', '1', '2', '3', '0', '4', '0', '1'],
                ['5', '', 'Connor McDavidC. McDavid', '2/27/2025', 'EDM', '@', 'MTL', '0', '3', '3', '0', '3', '1', '0']
            ]
        elif sport == "WNBA":
            return [
                ['', '', 'NAME', 'DATE', 'TM', '', 'OPP', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%'],
                ['1', '', 'Breanna StewartB. Stewart', '2/13/2025', 'NYL', '@', 'CON', '35', '25', '8', '4', '1', '2', '9', '18', '50.0', '2', '5', '40.0', '5', '6', '83.3'],
                ['2', '', 'Breanna StewartB. Stewart', '2/21/2025', 'NYL', '@', 'WAS', '32', '22', '7', '3', '2', '1', '8', '16', '50.0', '1', '4', '25.0', '5', '5', '100.0'],
                ['3', '', 'Breanna StewartB. Stewart', '2/23/2025', 'NYL', 'vs', 'CHI', '34', '28', '9', '5', '1', '2', '10', '19', '52.6', '3', '6', '50.0', '5', '6', '83.3'],
                ['4', '', 'Breanna StewartB. Stewart', '2/25/2025', 'NYL', 'vs', 'DAL', '31', '20', '6', '4', '1', '1', '7', '15', '46.7', '2', '4', '50.0', '4', '5', '80.0'],
                ['5', '', 'Breanna StewartB. Stewart', '2/27/2025', 'NYL', '@', 'PHX', '33', '26', '8', '3', '2', '1', '9', '17', '52.9', '2', '5', '40.0', '6', '7', '85.7']
            ]
        
    def calculate_quantitative(self, player_data, statistic, method):
        """Calculate quantitative value based on method"""
        if len(player_data) < 2:
            return 0
            
        header = player_data[0]
        values = []
        
        # Handle combined statistics
        if self.is_combined_statistic(statistic):
            components = self.get_combined_stat_components(statistic)
            for game in player_data[1:]:
                game_total = 0
                for comp in components:
                    try:
                        comp_index = header.index(comp)
                        game_total += float(game[comp_index])
                    except (ValueError, IndexError):
                        continue
                values.append(game_total)
        else:
            try:
                stat_index = header.index(statistic)
                values = [float(game[stat_index]) for game in player_data[1:] if game[stat_index]]
            except (ValueError, IndexError):
                return 0
        
        if not values:
            return 0
            
        if method.lower() == "mean":
            return np.mean(values)
        elif method.lower() == "median":
            return np.median(values)
        elif method.lower() == "mode":
            return max(set(values), key=values.count)
        else:
            return np.mean(values)
            
    def get_defense_analysis(self, sport, player_data, statistic):
        """Get defense analysis for the opponent"""
        if not player_data or len(player_data) < 2:
            return None
            
        header = player_data[0]
        if 'OPP' not in header:
            return None
            
        opp_index = header.index('OPP')
        opponent = player_data[1][opp_index]
        
        # Simulate defense analysis (in real implementation, this would scrape sport-specific data)
        return {
            'opponent': opponent,
            'rank': 2,
            'total_teams': 30,
            'value_allowed': 120.44,
            'difficulty': "Easy",
            'color': "green",
            'rank_percentage': 6.7
        }
        
    def create_dashboard(self, player_data, statistic, projection, quantitative, player_name, defense_analysis, sport):
        """Create the integrated dashboard"""
        self.fig.clear()
        
        # Set dark theme
        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
        
        # Ensure figure background matches the dark theme
        self.fig.patch.set_facecolor('#1a1a1a')
        
        header = player_data[0]
        
        # Handle combined statistics
        if self.is_combined_statistic(statistic):
            # Calculate combined statistic from individual components
            components = self.get_combined_stat_components(statistic)
            combined_values = []
            
            for game in player_data[1:]:
                game_total = 0
                valid_components = 0
                
                for comp in components:
                    try:
                        comp_index = header.index(comp)
                        game_total += float(game[comp_index])
                        valid_components += 1
                    except (ValueError, IndexError):
                        continue
                
                if valid_components > 0:
                    combined_values.append(game_total)
                else:
                    combined_values.append(0)
            
            # Use combined values instead of single statistic
            values = combined_values
            index_to_extract = None  # Not needed for combined stats
        else:
            # Handle individual statistics
            try:
                index_to_extract = header.index(statistic)
            except ValueError:
                self.status_var.set(f"Parameter {statistic} not found in header.")
                return
        
        # Extract data
        dates = [datetime.strptime(game[header.index('DATE')], '%m/%d/%Y') for game in player_data[1:] if game[header.index('DATE')]]
        
        if self.is_combined_statistic(statistic):
            # Use pre-calculated combined values
            values = combined_values
        else:
            # Extract individual statistic values
            values = [float(game[index_to_extract]) for game in player_data[1:] if game[index_to_extract]]
        
        team_abbrs = [game[header.index('TM')] for game in player_data[1:] if game[header.index('TM')]]
        opponent_names = [game[header.index('OPP')] for game in player_data[1:] if game[header.index('OPP')]]
        
        # Sort data by date
        sorted_data = sorted(zip(dates, values, team_abbrs, opponent_names))
        sorted_dates, sorted_values, sorted_team_abbrs, sorted_opponent_names = zip(*sorted_data)
        
        x_values = list(range(len(sorted_dates)))
        
        # Create grid layout
        gs = self.fig.add_gridspec(2, 2, height_ratios=[1.2, 1], hspace=0.25, wspace=0.25)
        
        # Main player performance chart (top left)
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.set_facecolor('#1a1a1a')
        
        # Color-coded bars (green for hits, red for misses)
        colors = ['green' if value >= projection else 'red' for value in sorted_values]
        bars = ax1.bar(x_values, sorted_values, width=0.6, color=colors, alpha=0.8)
        
        # Add lines
        ax1.axhline(y=quantitative, color='purple', linestyle='solid', linewidth=2, 
                   label=f'Average: {quantitative:.2f}')
        ax1.axhline(y=projection, color='yellow', linestyle='dotted', linewidth=2, 
                   label=f'Projection: {projection:.2f}')
        
        ax1.set_xlabel('Recent Games', fontsize=11)
        ax1.set_ylabel(statistic, fontsize=11)
        ax1.set_title(f'{player_name} - {statistic} Performance', fontsize=13, fontweight='bold')
        ax1.set_xticks(x_values)
        ax1.set_xticklabels([date.strftime('%m/%d') for date in sorted_dates], rotation=45, ha='right', fontsize=9)
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, 
                    f'{yval:.1f}\nvs {sorted_opponent_names[i]}', 
                    ha='center', va='bottom', fontsize=9, color='white')
        
        # Team Defense Rankings (top right)
        ax2 = self.fig.add_subplot(gs[0, 1])
        ax2.set_facecolor('#1a1a1a')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        # Title
        title = f'{sport} Team Defense Rankings\n(Worst to Best)'
        ax2.text(0.5, 0.95, title, fontsize=12, fontweight='bold', ha='center', va='top', transform=ax2.transAxes, color='white')
        
        # Simulate team rankings
        teams = ['Jazz', 'Wizards', 'Bulls', 'Hawks', 'Pelicans', 'Nuggets', 'Grizzlies', 'Spurs', 'Suns', '76ers']
        values = [121.23, 120.44, 119.37, 119.32, 119.26, 116.87, 116.85, 116.68, 116.62, 115.84]
        
        y_start = 0.85
        y_spacing = 0.07
        for i, (team, value) in enumerate(zip(teams, values)):
            y_pos = y_start - (i * y_spacing)
            color = 'yellow' if (defense_analysis and team == defense_analysis['opponent']) else 'white'
            fontweight = 'bold' if (defense_analysis and team == defense_analysis['opponent']) else 'normal'
            team_text = f"{i+1}. {team}: {value:.2f}"
            ax2.text(0.05, y_pos, team_text, fontsize=10, color=color, fontweight=fontweight, transform=ax2.transAxes)
        
        # Statistical Analysis (bottom left)
        ax3 = self.fig.add_subplot(gs[1, 0])
        ax3.set_facecolor('#1a1a1a')
        
        data = np.array(sorted_values)
        std_dev = np.std(data, ddof=1)
        n = len(data)
        
        # Confidence Interval Calculation
        t_critical = 2.571
        margin_of_error = t_critical * (std_dev / np.sqrt(n))
        conf_interval = (quantitative - margin_of_error, quantitative + margin_of_error)
        
        # CDF and PDF Calculation
        x = projection
        z = (x - quantitative) / std_dev
        
        def erf(z):
            t = 1.0 / (1.0 + 0.5 * abs(z))
            tau = t * np.exp(-z*z - 1.26551223 + 1.00002368*t + 0.37409196*t*t + 0.09678418*t*t*t - 0.18628806*t*t*t*t + 0.27886807*t*t*t*t*t - 1.13520398*t*t*t*t*t*t + 1.48851587*t*t*t*t*t*t*t - 0.82215223*t*t*t*t*t*t*t*t + 0.17087277*t*t*t*t*t*t*t*t*t)
            return 1 - tau if z >= 0 else tau - 1
        
        cdf = 0.5 * (1 + erf(z / np.sqrt(2)))
        pdf = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * z**2)
        
        # Normal Distribution PDF Plot
        x_values_pdf = np.linspace(quantitative - 4*std_dev, quantitative + 4*std_dev, 1000)
        pdf_values = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values_pdf - quantitative) / std_dev) ** 2)
        ax3.plot(x_values_pdf, pdf_values, color='blue', linewidth=2)
        ax3.axvline(x, color='yellow', linestyle='dashed', linewidth=2, label=f'Projection: {projection:.2f}')
        ax3.axvline(quantitative, color='purple', linestyle='solid', linewidth=2, label=f'Mean: {quantitative:.2f}')
        ax3.fill_between(x_values_pdf, pdf_values, where=(x_values_pdf <= x), color='gray', alpha=0.5)
        ax3.text(projection, 0.02, f"CDF at Projection: {cdf:.4f}", fontsize=10, color='white')
        ax3.set_title('Normal Distribution PDF', fontsize=11, fontweight='bold')
        ax3.set_xlabel(statistic, fontsize=10)
        ax3.set_ylabel('Density', fontsize=10)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)
        
        # Opponent Analysis (bottom right)
        ax4 = self.fig.add_subplot(gs[1, 1])
        ax4.set_facecolor('#1a1a1a')
        
        if defense_analysis:
            ax4.text(0.1, 0.95, f"OPPONENT ANALYSIS", 
                    fontsize=16, fontweight='bold', transform=ax4.transAxes, color='yellow')
            ax4.text(0.1, 0.85, f"Team: {defense_analysis['opponent']}", 
                    fontsize=14, fontweight='bold', transform=ax4.transAxes, color='white')
            
            total_teams = defense_analysis['total_teams']
            rank_text = f"#{defense_analysis['rank']} of {total_teams} teams"
            ax4.text(0.1, 0.75, f"Rank in {statistic} Defense: {rank_text}", 
                    fontsize=12, transform=ax4.transAxes, color='cyan')
            ax4.text(0.1, 0.65, f"Allows: {defense_analysis['value_allowed']:.2f} {statistic}/game", 
                    fontsize=12, transform=ax4.transAxes, color='white')
            
            difficulty_color = defense_analysis['color']
            difficulty_text = f"Difficulty: {defense_analysis['difficulty']} (#{defense_analysis['rank']} worst)"
            ax4.text(0.1, 0.55, difficulty_text, 
                    fontsize=12, fontweight='bold', transform=ax4.transAxes, color=difficulty_color)
            
            # Hit probability
            hit_prob = (1 - cdf) * 100
            ax4.text(0.1, 0.45, f"Hit Probability: {hit_prob:.1f}%", 
                    fontsize=12, transform=ax4.transAxes, color='white')
            
            # Recommendation
            if hit_prob > 60:
                recommendation = "STRONG BET"
                rec_color = "green"
            elif hit_prob > 40:
                recommendation = "MODERATE BET"
                rec_color = "orange"
            else:
                recommendation = "AVOID BET"
                rec_color = "red"
            
            ax4.text(0.1, 0.35, f"Recommendation: {recommendation}", 
                    fontsize=14, fontweight='bold', transform=ax4.transAxes, color=rec_color)
        
        # Footer with summary
        footer_text = f"Player: {player_name} | Sport: {sport} | Statistic: {statistic} | Games Analyzed: {len(sorted_values)}"
        if defense_analysis:
            footer_text += f" | Opponent: {defense_analysis['opponent']} (#{defense_analysis['rank']} worst {statistic} defense)"
        
        self.fig.text(0.02, 0.02, footer_text, fontsize=10, color='white', transform=self.fig.transFigure)
        
        # Additional stats
        stats_text = f"Mean: {quantitative:.2f} | Std Dev: {std_dev:.2f} | Hit Rate: {((np.array(sorted_values) >= projection).sum() / len(sorted_values) * 100):.1f}%"
        self.fig.text(0.02, 0.04, stats_text, fontsize=10, color='white', transform=self.fig.transFigure)
        
        conf_text = f"Confidence Interval: [{conf_interval[0]:.2f}, {conf_interval[1]:.2f}] | CDF at Projection: {cdf:.4f}"
        self.fig.text(0.02, 0.06, conf_text, fontsize=10, color='white', transform=self.fig.transFigure)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MultiSportDashboard()
    app.run() 