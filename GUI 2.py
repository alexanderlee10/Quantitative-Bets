import tkinter as tk
from tkinter import ttk
import importlib
from plot import plot_sports_stats
from datascrapper import geturl, scrape_statmuse
from NBBBA import clean_nba_data, get_nba_statistics
from simplemean import simple_mean
from WMA import weighted_moving_average
from nhl import clean_nhl_data, get_nhl_player_statistics, get_nhl_goalie_statistics
from MLB import clean_mlb_data, get_mlb_hitter_statistics, get_mlb_pitcher_statistics

# Create the main window
root = tk.Tk()
root.title("QB AKA Quantitative Bets")

# Create a label and dropdown for the league
league_label = tk.Label(root, text="League:")
league_label.grid(row=0, column=0)
league_var = tk.StringVar(value="NBA")
league_dropdown = ttk.Combobox(root, textvariable=league_var)
league_dropdown['values'] = ('NBA', 'NFL', 'NHL', 'MLB')
league_dropdown.grid(row=0, column=1)

# Create a label and text input for the player name
player_name_label = tk.Label(root, text="Player Name:")
player_name_label.grid(row=1, column=0)
player_name_entry = tk.Entry(root)
player_name_entry.grid(row=1, column=1)

# Create a label and text input for the team name
team_name_label = tk.Label(root, text="Team Name:")
team_name_label.grid(row=2, column=0)
team_name_entry = tk.Entry(root)
team_name_entry.insert(0, "Any")
team_name_entry.grid(row=2, column=1)

# Create a label and dropdown for the time duration
time_duration_label = tk.Label(root, text="Time Duration:")
time_duration_label.grid(row=3, column=0)
time_duration_var = tk.StringVar(value="combined")
time_duration_dropdown = ttk.Combobox(root, textvariable=time_duration_var)
time_duration_dropdown['values'] = ('Last 5 Regular Games', 'Playoff Game Log', 'combined', 'Game Log', 'Last 5 Games', 'Last 7 Playoff Games')
time_duration_dropdown.grid(row=3, column=1)

# Create a label and radio buttons for the position (only for NHL and MLB)
position_label = tk.Label(root, text="Position:")
position_label.grid(row=4, column=0)
position_var = tk.StringVar(value="Player")

nhl_player_radio = tk.Radiobutton(root, text="Player", variable=position_var, value="Player")
nhl_goalie_radio = tk.Radiobutton(root, text="Goalie", variable=position_var, value="Goalie")
mlb_hitter_radio = tk.Radiobutton(root, text="Hitter", variable=position_var, value="Hitter")
mlb_pitcher_radio = tk.Radiobutton(root, text="Pitcher", variable=position_var, value="Pitcher")

nhl_player_radio.grid(row=4, column=1)
nhl_goalie_radio.grid(row=4, column=2)
mlb_hitter_radio.grid(row=4, column=1)
mlb_pitcher_radio.grid(row=4, column=2)

# Initially hide the position radio buttons
nhl_player_radio.grid_remove()
nhl_goalie_radio.grid_remove()
mlb_hitter_radio.grid_remove()
mlb_pitcher_radio.grid_remove()

# Create a label and dropdown for the statistic
statistic_label = tk.Label(root, text="Statistic:")
statistic_label.grid(row=5, column=0)
statistic_var = tk.StringVar(value="PTS")
statistic_dropdown = ttk.Combobox(root, textvariable=statistic_var)
statistic_dropdown.grid(row=5, column=1)

# Create a label and text input for the projection
projection_label = tk.Label(root, text="Projection:")
projection_label.grid(row=6, column=0)
projection_entry = tk.Entry(root)
projection_entry.grid(row=6, column=1)

# Create a label and dropdown for the quantitative analysis
quantitative_label = tk.Label(root, text="Quantitative Analysis:")
quantitative_label.grid(row=7, column=0)
quantitative_var = tk.StringVar(value="Mean")
quantitative_dropdown = ttk.Combobox(root, textvariable=quantitative_var)
quantitative_dropdown['values'] = ('Mean', 'WMA', 'K-Means Clustering')
quantitative_dropdown.grid(row=7, column=1)

def update_statistic_options(*args):
    league = league_var.get()

    if league == 'NHL':
        position_label.grid()
        nhl_player_radio.grid()
        nhl_goalie_radio.grid()
        mlb_hitter_radio.grid_remove()
        mlb_pitcher_radio.grid_remove()
        position_var.set('Player')
    elif league == 'MLB':
        position_label.grid()
        nhl_player_radio.grid_remove()
        nhl_goalie_radio.grid_remove()
        mlb_hitter_radio.grid()
        mlb_pitcher_radio.grid()
        position_var.set('Hitter')
    else:
        position_label.grid_remove()
        nhl_player_radio.grid_remove()
        nhl_goalie_radio.grid_remove()
        mlb_hitter_radio.grid_remove()
        mlb_pitcher_radio.grid_remove()

    try:
        if league == 'NHL':
            if position_var.get().lower() == 'goalie':
                get_statistics = get_nhl_goalie_statistics
            else:
                get_statistics = get_nhl_player_statistics
        elif league == 'MLB':
            if position_var.get().lower() == 'pitcher':
                get_statistics = get_mlb_pitcher_statistics
            else:
                get_statistics = get_mlb_hitter_statistics
        elif league == 'NBA':
            get_statistics = get_nba_statistics
        else:
            # Add logic for other leagues
            get_statistics = None

        if get_statistics:
            stat_options = get_statistics()
            statistic_var.set(stat_options[0])
            statistic_dropdown['values'] = stat_options
    except ImportError:
        print(f"Module for {league} not found.")
    except AttributeError:
        print(f"Function to get statistics for {league} not found.")

# Update statistic options when the league or position changes
league_var.trace('w', update_statistic_options)
position_var.trace('w', update_statistic_options)


def calculate_hit_rate(data, category, projection):
    hits = 0
    total = len(data) - 1

    for game in data[1:]:
        value = float(game[data[0].index(category)])
        if value >= projection:
            hits += 1

    hit_rate = hits / total
    return hit_rate * 100  # Return as percentage


# Function to handle button click
def on_button_click():
    league = league_var.get()
    player_name = player_name_entry.get()
    team = team_name_entry.get()
    time_duration = time_duration_var.get()
    statistic = statistic_var.get()
    projection = float(projection_entry.get())
    quantitative_analysis = quantitative_var.get()

    url = geturl(league.lower(), player_name, team, time_duration)
    data = scrape_statmuse(url)

    if not data:
        print("No data found.")
        return

    if league == 'NBA':
        cleaned_data = clean_nba_data(data)
    elif league == 'NHL':
        position = position_var.get().lower()
        cleaned_data = clean_nhl_data(data, position)
    elif league == 'MLB':
        position = position_var.get().lower()
        cleaned_data = clean_mlb_data(data, position)
    # Add elif blocks for other leagues and their cleaning functions

    if not cleaned_data:
        print("No cleaned data available.")
        return

    print(f"Cleaned Data Header: {cleaned_data[0]}")  # Debug print
    print(f"Statistic to Plot: {statistic}")  # Debug print

    t = 0
    if quantitative_analysis == 'Mean':
        t = simple_mean(cleaned_data, statistic)
    elif quantitative_analysis == 'WMA':
        t = weighted_moving_average(cleaned_data, statistic)  # Assuming this function is defined
    elif quantitative_analysis == 'K-Means Clustering':
        # Perform k-means clustering
        pass  # Add the logic for k-means clustering

    plot_sports_stats(cleaned_data, statistic, projection, t)


# Create a button to trigger data processing and plotting
button = tk.Button(root, text="Generate Plot", command=on_button_click)
button.grid(row=8, columnspan=2)

# Initial update to set the correct statistic options
update_statistic_options()

# Run the application
root.mainloop()
