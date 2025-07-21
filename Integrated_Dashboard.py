import tkinter as tk
from tkinter import ttk, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
from datascrapper import geturl, scrape_statmuse
from NBBBA import clean_nba_data, get_nba_statistics
from simplemean import simple_mean
from WMA import weighted_moving_average
from team_defense_scraper import get_defense_analysis, get_team_defense_rankings
from combined_stats_analyzer import get_combined_stats_rankings

class IntegratedDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NBA Integrated Betting Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1a1a1a', foreground='white', font=('Arial', 10))
        style.configure('TButton', background='#4a4a4a', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('TCombobox', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        style.configure('TEntry', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="NBA Integrated Betting Dashboard", 
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
        
        # Statistics and Analysis Section
        analysis_frame = tk.LabelFrame(parent, text="Statistics & Analysis", 
                                     font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='white')
        analysis_frame.pack(fill='x', pady=10, padx=10)
        
        # Statistic selection
        tk.Label(analysis_frame, text="Statistic:", bg='#1a1a1a', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.statistic_var = tk.StringVar(value="PTS")
        self.statistic_combo = ttk.Combobox(analysis_frame, textvariable=self.statistic_var, 
                                          values=get_nba_statistics())
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
        
        # Initial placeholder
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
            
            # Get URL and scrape data
            url = geturl("nba", player_name, team, time_duration)
            data = scrape_statmuse(url)
            
            if not data:
                self.root.after(0, lambda: self.status_var.set("ERROR: No data found for this player"))
                return
                
            # Clean NBA data
            cleaned_data = clean_nba_data(data)
            if not cleaned_data:
                self.root.after(0, lambda: self.status_var.set("ERROR: Failed to clean data"))
                return
                
            # Calculate quantitative analysis
            if quantitative_analysis == 'Mean':
                quantitative_value = simple_mean(cleaned_data, statistic)
            elif quantitative_analysis == 'WMA':
                quantitative_value = weighted_moving_average(cleaned_data, statistic)
            else:
                quantitative_value = simple_mean(cleaned_data, statistic)
                
            # Get team defense analysis
            defense_analysis = get_defense_analysis(cleaned_data, statistic)
            
            # Update status
            self.root.after(0, lambda: self.status_var.set(f"Generating dashboard for {player_name}..."))
            
            # Create dashboard
            self.root.after(0, lambda: self.create_dashboard(cleaned_data, statistic, projection, quantitative_value, player_name, defense_analysis))
            
            # Update status
            self.root.after(0, lambda: self.status_var.set(f"Dashboard generated successfully for {player_name}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"ERROR: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.submit_btn.config(state='normal'))
            self.root.after(0, self.progress.stop)
            
    def is_combined_statistic(self, statistic):
        """Check if the statistic is a combined statistic like PRA, PR, etc."""
        combined_stats = {
            'PRA': ['PTS', 'REB', 'AST'],
            'PR': ['PTS', 'REB'],
            'PA': ['PTS', 'AST'],
            'RA': ['REB', 'AST'],
            'PRA+': ['PTS', 'REB', 'AST', 'FGM'],
            'SHOOTING': ['FGM', '3PM', 'FTM']
        }
        return statistic.upper() in combined_stats
    
    def get_combined_stat_components(self, statistic):
        """Get the component statistics for a combined statistic"""
        combined_stats = {
            'PRA': ['PTS', 'REB', 'AST'],
            'PR': ['PTS', 'REB'],
            'PA': ['PTS', 'AST'],
            'RA': ['REB', 'AST'],
            'PRA+': ['PTS', 'REB', 'AST', 'FGM'],
            'SHOOTING': ['FGM', '3PM', 'FTM']
        }
        return combined_stats.get(statistic.upper(), [])
    
    def create_dashboard(self, player_data, statistic, projection, quantitative, player_name, defense_analysis):
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
        
        # Get team defense rankings
        if self.is_combined_statistic(statistic):
            # Use combined stats analyzer for combined statistics
            components = self.get_combined_stat_components(statistic)
            combined_rankings, detailed_data = get_combined_stats_rankings(components)
            if combined_rankings:
                # Take top 10 teams that allow most combined production
                sorted_rankings = combined_rankings[:10]
                teams = [team for _, team, _ in sorted_rankings]
                values = [value for _, _, value in sorted_rankings]
                ranks = [rank for rank, _, _ in sorted_rankings]
            else:
                sorted_rankings = []
        else:
            # Use regular team defense rankings for individual statistics
            rankings = get_team_defense_rankings(statistic)
            if rankings:
                # Ensure rankings are sorted by value (worst first) and take top 10
                sorted_rankings = sorted(rankings, key=lambda x: x[1], reverse=True)[:10]
                teams, values, ranks = zip(*sorted_rankings)
            else:
                sorted_rankings = []
            
            # Create clean text-based list instead of bars
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')
            
            # Title
            if self.is_combined_statistic(statistic):
                components = self.get_combined_stat_components(statistic)
                title = f'Combined {statistic} Defense Rankings\n(Worst to Best)'
                subtitle = f'Components: {" + ".join(components)}'
                ax2.text(0.5, 0.95, title, 
                        fontsize=12, fontweight='bold', ha='center', va='top', transform=ax2.transAxes, color='white')
                ax2.text(0.5, 0.90, subtitle, 
                        fontsize=9, ha='center', va='top', transform=ax2.transAxes, color='cyan')
            else:
                ax2.text(0.5, 0.95, 'Team Defense Rankings\n(Worst to Best)', 
                        fontsize=12, fontweight='bold', ha='center', va='top', transform=ax2.transAxes, color='white')
            
            # Show opponent info if not in top 10
            if defense_analysis and defense_analysis['rank'] > 10:
                total_teams = defense_analysis['total_teams']
                note = f" (Note: {total_teams}/30 teams found)" if total_teams < 30 else ""
                ax2.text(0.02, 0.98, f"{defense_analysis['opponent']}: #{defense_analysis['rank']} of {total_teams}{note}", 
                        fontsize=10, fontweight='bold', color='yellow', 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7))
            
            # Display team rankings as text
            y_start = 0.85
            y_spacing = 0.07
            
            for i, (team, value, rank) in enumerate(sorted_rankings):
                y_pos = y_start - (i * y_spacing)
                
                # Highlight opponent if in top 10
                if defense_analysis and team == defense_analysis['opponent']:
                    color = 'yellow'
                    fontweight = 'bold'
                else:
                    color = 'white'
                    fontweight = 'normal'
                
                # Team name and value
                team_text = f"{rank}. {team}: {value:.2f}"
                ax2.text(0.05, y_pos, team_text, fontsize=10, color=color, fontweight=fontweight, transform=ax2.transAxes)
        
        # Statistical Analysis (bottom left) - Using original normal distribution plot
        ax3 = self.fig.add_subplot(gs[1, 0])
        ax3.set_facecolor('#1a1a1a')
        
        data = np.array(sorted_values)
        std_dev = np.std(data, ddof=1)
        n = len(data)
        
        # Confidence Interval Calculation
        t_critical = 2.571  # Critical t-value for 5 degrees of freedom and 95% confidence
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
        
        # Normal Distribution PDF Plot (from original plot.py)
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
            # Create a summary box with enhanced opponent ranking info
            ax4.text(0.1, 0.95, f"OPPONENT ANALYSIS", 
                    fontsize=16, fontweight='bold', transform=ax4.transAxes, color='yellow')
            
            ax4.text(0.1, 0.85, f"Team: {defense_analysis['opponent']}", 
                    fontsize=14, fontweight='bold', transform=ax4.transAxes, color='white')
            
            # Enhanced ranking display
            if self.is_combined_statistic(statistic):
                components = self.get_combined_stat_components(statistic)
                ax4.text(0.1, 0.75, f"Combined {statistic} Defense Analysis", 
                        fontsize=12, transform=ax4.transAxes, color='cyan')
                ax4.text(0.1, 0.65, f"Components: {' + '.join(components)}", 
                        fontsize=10, transform=ax4.transAxes, color='white')
                ax4.text(0.1, 0.55, f"Note: Combined stats analysis available", 
                        fontsize=10, transform=ax4.transAxes, color='yellow')
            else:
                total_teams = defense_analysis['total_teams']
                rank_text = f"#{defense_analysis['rank']} of {total_teams} teams"
                if total_teams < 30:
                    rank_text += f" (Note: {total_teams}/30 teams found)"
                ax4.text(0.1, 0.75, f"Rank in {statistic} Defense: {rank_text}", 
                        fontsize=12, transform=ax4.transAxes, color='cyan')
                
                ax4.text(0.1, 0.65, f"Allows: {defense_analysis['value_allowed']:.2f} {statistic}/game", 
                        fontsize=12, transform=ax4.transAxes, color='white')
            
            # Difficulty indicator with ranking context
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
            
            # Additional context
            if defense_analysis['rank'] <= 5:
                context = f"⚠️ {defense_analysis['opponent']} is among the WORST {statistic} defenses"
                context_color = "red"
            elif defense_analysis['rank'] <= 10:
                context = f"⚠️ {defense_analysis['opponent']} is in the bottom 10 for {statistic} defense"
                context_color = "orange"
            elif defense_analysis['rank'] >= 25:
                context = f"⚠️ {defense_analysis['opponent']} is among the BEST {statistic} defenses"
                context_color = "green"
            else:
                context = f"ℹ️ {defense_analysis['opponent']} has average {statistic} defense"
                context_color = "white"
            
            ax4.text(0.1, 0.25, context, 
                    fontsize=10, transform=ax4.transAxes, color=context_color)
            
            # Add more detailed analysis
            if defense_analysis['rank'] <= 3:
                detail = f"🔥 {defense_analysis['opponent']} gives up the MOST {statistic} in the league!"
                detail_color = "red"
            elif defense_analysis['rank'] <= 8:
                detail = f"🔥 {defense_analysis['opponent']} is in the bottom 25% for {statistic} defense"
                detail_color = "orange"
            elif defense_analysis['rank'] >= 28:
                detail = f"❌ {defense_analysis['opponent']} is one of the BEST {statistic} defenses"
                detail_color = "green"
            else:
                detail = f"ℹ️ {defense_analysis['opponent']} has middle-tier {statistic} defense"
                detail_color = "white"
            
            ax4.text(0.1, 0.15, detail, 
                    fontsize=10, transform=ax4.transAxes, color=detail_color)
            
        else:
            ax4.text(0.5, 0.5, "No opponent data available", 
                    fontsize=12, ha='center', va='center', transform=ax4.transAxes, color='white')
        
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        ax4.set_title('Opponent Analysis', fontsize=12, fontweight='bold', pad=20)
        
        # Add overall statistics text with opponent info
        opponent_info = ""
        if defense_analysis:
            opponent_info = f" | Opponent: {defense_analysis['opponent']} (#{defense_analysis['rank']} worst {statistic} defense)"
        
        stats_text = f"""
        Player: {player_name} | Statistic: {statistic} | Games Analyzed: {len(sorted_values)}{opponent_info}
        Mean: {quantitative:.2f} | Std Dev: {std_dev:.2f} | Hit Rate: {(sum(1 for v in sorted_values if v >= projection) / len(sorted_values) * 100):.1f}%
        Confidence Interval: [{conf_interval[0]:.2f}, {conf_interval[1]:.2f}] | CDF at Projection: {cdf:.4f}
        """
        
        self.fig.text(0.02, 0.02, stats_text, fontsize=10, va='bottom', ha='left', 
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="black", alpha=0.7))
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = IntegratedDashboard()
    app.run() 