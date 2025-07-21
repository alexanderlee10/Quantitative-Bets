import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datascrapper import geturl, scrape_statmuse
from NBBBA import clean_nba_data, get_nba_statistics
from simplemean import simple_mean
from WMA import weighted_moving_average
from enhanced_plot import create_enhanced_dashboard, plot_team_defense_comparison
from team_defense_scraper import get_defense_analysis, get_team_defense_rankings

class EnhancedDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NBA Enhanced Betting Dashboard")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        style.configure('TButton', background='#4a4a4a', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('TCombobox', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        style.configure('TEntry', background='#4a4a4a', foreground='white', fieldbackground='#4a4a4a')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="NBA Enhanced Betting Dashboard", 
                              font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#00ff00')
        title_label.pack(pady=10)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Player Information Section
        player_frame = tk.LabelFrame(main_frame, text="Player Information", 
                                   font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='white')
        player_frame.pack(fill='x', pady=10, padx=10)
        
        # Player name
        tk.Label(player_frame, text="Player Name:", bg='#2b2b2b', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.player_name_entry = tk.Entry(player_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.player_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Team name
        tk.Label(player_frame, text="Team Name:", bg='#2b2b2b', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.team_name_entry = tk.Entry(player_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.team_name_entry.insert(0, "Any")
        self.team_name_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Time duration
        tk.Label(player_frame, text="Time Duration:", bg='#2b2b2b', fg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.time_duration_var = tk.StringVar(value="Last 5 Regular Games")
        time_duration_combo = ttk.Combobox(player_frame, textvariable=self.time_duration_var, 
                                         values=('Last 5 Regular Games', 'Last 7 Regular Games', 'Last 10 Regular Games', 
                                                'Playoff Game Log', 'Last 5 Playoff Games', 'combined'))
        time_duration_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Configure grid weights
        player_frame.columnconfigure(1, weight=1)
        
        # Statistics and Analysis Section
        analysis_frame = tk.LabelFrame(main_frame, text="Statistics & Analysis", 
                                     font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='white')
        analysis_frame.pack(fill='x', pady=10, padx=10)
        
        # Statistic selection
        tk.Label(analysis_frame, text="Statistic:", bg='#2b2b2b', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.statistic_var = tk.StringVar(value="PTS")
        self.statistic_combo = ttk.Combobox(analysis_frame, textvariable=self.statistic_var, 
                                          values=get_nba_statistics())
        self.statistic_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Projection
        tk.Label(analysis_frame, text="Projection:", bg='#2b2b2b', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.projection_entry = tk.Entry(analysis_frame, bg='#4a4a4a', fg='white', font=('Arial', 10))
        self.projection_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Quantitative analysis
        tk.Label(analysis_frame, text="Analysis Method:", bg='#2b2b2b', fg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.quantitative_var = tk.StringVar(value="Mean")
        quantitative_combo = ttk.Combobox(analysis_frame, textvariable=self.quantitative_var, 
                                        values=('Mean', 'WMA'))
        quantitative_combo.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Configure grid weights
        analysis_frame.columnconfigure(1, weight=1)
        
        # Buttons Section
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill='x', pady=20)
        
        # Single button for both dashboards
        self.generate_btn = tk.Button(button_frame, text="Generate Complete Analysis", 
                                    command=self.generate_complete_analysis, 
                                    bg='#00aa00', fg='white', font=('Arial', 14, 'bold'),
                                    height=3, width=30)
        self.generate_btn.pack(expand=True, pady=20)
        
        # Status and Results Section
        results_frame = tk.LabelFrame(main_frame, text="Analysis Results", 
                                    font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='white')
        results_frame.pack(fill='both', expand=True, pady=10, padx=10)
        
        # Text widget for results
        self.results_text = tk.Text(results_frame, bg='#1e1e1e', fg='#00ff00', 
                                   font=('Consolas', 10), height=15)
        scrollbar = tk.Scrollbar(results_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = tk.Label(main_frame, textvariable=self.progress_var, 
                                      bg='#2b2b2b', fg='#ffff00', font=('Arial', 10))
        self.progress_label.pack(pady=5)
        
    def log_message(self, message):
        """Add message to results text widget"""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update()
        
    def generate_complete_analysis(self):
        """Generate both player dashboard and team rankings in separate thread"""
        self.generate_btn.config(state='disabled')
        self.progress_var.set("Generating complete analysis...")
        self.results_text.delete(1.0, tk.END)
        
        # Start processing in separate thread
        thread = threading.Thread(target=self._generate_complete_analysis_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_complete_analysis_thread(self):
        """Thread function for generating both dashboards"""
        try:
            # Get input values
            player_name = self.player_name_entry.get().strip()
            team = self.team_name_entry.get().strip()
            time_duration = self.time_duration_var.get()
            statistic = self.statistic_var.get()
            
            try:
                projection = float(self.projection_entry.get())
            except ValueError:
                self.log_message("ERROR: Please enter a valid projection number")
                return
                
            quantitative_analysis = self.quantitative_var.get()
            
            if not player_name:
                self.log_message("ERROR: Please enter a player name")
                return
                
            self.log_message(f"Analyzing {player_name} for {statistic}...")
            
            # Get URL and scrape data
            url = geturl("nba", player_name, team, time_duration)
            self.log_message(f"Fetching data from: {url}")
            
            data = scrape_statmuse(url)
            if not data:
                self.log_message("ERROR: No data found for this player/query")
                return
                
            self.log_message(f"Found {len(data)-1} games of data")
            
            # Clean NBA data
            cleaned_data = clean_nba_data(data)
            if not cleaned_data:
                self.log_message("ERROR: Failed to clean data")
                return
                
            self.log_message("Data cleaned successfully")
            
            # Calculate quantitative analysis
            if quantitative_analysis == 'Mean':
                quantitative_value = simple_mean(cleaned_data, statistic)
            elif quantitative_analysis == 'WMA':
                quantitative_value = weighted_moving_average(cleaned_data, statistic)
            else:
                quantitative_value = simple_mean(cleaned_data, statistic)
                
            self.log_message(f"{quantitative_analysis}: {quantitative_value:.2f}")
            
            # Get team defense analysis
            self.log_message("Analyzing opponent defense...")
            defense_analysis = get_defense_analysis(cleaned_data, statistic)
            
            if defense_analysis:
                self.log_message(f"Next opponent: {defense_analysis['opponent']}")
                self.log_message(f"Defense rank: {defense_analysis['rank']}/{defense_analysis['total_teams']}")
                self.log_message(f"Difficulty: {defense_analysis['difficulty']}")
                self.log_message(f"Allows: {defense_analysis['value_allowed']} {statistic}")
            else:
                self.log_message("No opponent defense data available")
            
            # Calculate hit probability
            values = [float(game[cleaned_data[0].index(statistic)]) for game in cleaned_data[1:]]
            hit_rate = (sum(1 for v in values if v >= projection) / len(values)) * 100
            
            self.log_message(f"Hit rate: {hit_rate:.1f}%")
            
            # Generate enhanced dashboard
            self.log_message("Generating enhanced dashboard...")
            create_enhanced_dashboard(cleaned_data, statistic, projection, quantitative_value, player_name)
            
            # Generate team defense rankings
            self.log_message("Generating team defense rankings...")
            plot_team_defense_comparison(statistic)
            
            self.log_message("Complete analysis generated successfully!")
            
        except Exception as e:
            self.log_message(f"ERROR: {str(e)}")
        finally:
            self.generate_btn.config(state='normal')
            self.rankings_btn.config(state='normal')
            self.progress_var.set("Ready")
            

    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedDashboard()
    app.run() 