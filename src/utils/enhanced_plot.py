import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import numpy as np
from team_defense_scraper import get_defense_analysis, get_team_defense_rankings

def create_enhanced_dashboard(player_data, statistic, projection, quantitative, player_name):
    """
    Creates a comprehensive dashboard showing player stats and team defense analysis
    """
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
    
    header = player_data[0]
    
    try:
        index_to_extract = header.index(statistic)
    except ValueError:
        print(f"Parameter {statistic} not found in header.")
        return
    
    # Extract data
    dates = [datetime.strptime(game[header.index('DATE')], '%m/%d/%Y') for game in player_data[1:] if game[header.index('DATE')]]
    values = [float(game[index_to_extract]) for game in player_data[1:] if game[index_to_extract]]
    team_abbrs = [game[header.index('TM')] for game in player_data[1:] if game[header.index('TM')]]
    opponent_names = [game[header.index('OPP')] for game in player_data[1:] if game[header.index('OPP')]]
    
    # Sort data by date
    sorted_data = sorted(zip(dates, values, team_abbrs, opponent_names))
    sorted_dates, sorted_values, sorted_team_abbrs, sorted_opponent_names = zip(*sorted_data)
    
    x_values = list(range(len(sorted_dates)))
    
    # Get defense analysis early so it's available throughout the function
    defense_analysis = get_defense_analysis(player_data, statistic)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # Create grid layout - compact 2x2 layout
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1], hspace=0.25, wspace=0.25)
    
    # Main player performance chart (top left)
    ax1 = fig.add_subplot(gs[0, 0])
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
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Get team defense rankings
    rankings = get_team_defense_rankings(statistic)
    if rankings:
        # Ensure rankings are sorted by value (worst first) and take top 10
        sorted_rankings = sorted(rankings, key=lambda x: x[1], reverse=True)[:10]
        teams, values, ranks = zip(*sorted_rankings)
        
        # Create clean text-based list instead of bars
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        # Title
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
        
        # Print team names for debugging
        print("Team Defense Rankings (Worst to Best):")
        for i, (rank, team, value) in enumerate(sorted_rankings):
            print(f"  {rank}. {team}: {value:.2f}")
    
    # Statistical Analysis (bottom left) - Using original normal distribution plot
    ax3 = fig.add_subplot(gs[1, 0])
    
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
    ax4 = fig.add_subplot(gs[1, 1])
    
    if defense_analysis:
        # Create a summary box with enhanced opponent ranking info
        ax4.text(0.1, 0.95, f"OPPONENT ANALYSIS", 
                fontsize=16, fontweight='bold', transform=ax4.transAxes, color='yellow')
        
        ax4.text(0.1, 0.85, f"Team: {defense_analysis['opponent']}", 
                fontsize=14, fontweight='bold', transform=ax4.transAxes, color='white')
        
        # Enhanced ranking display
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
    
    fig.text(0.02, 0.02, stats_text, fontsize=10, va='bottom', ha='left', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="black", alpha=0.7))
    
    plt.tight_layout()
    plt.show()

def plot_team_defense_comparison(statistic):
    """
    Creates a standalone plot showing all team defensive rankings for a statistic
    """
    rankings = get_team_defense_rankings(statistic)
    
    if not rankings:
        print(f"No rankings found for {statistic}")
        return
    
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    teams, values, ranks = zip(*rankings)
    
    # Color gradient from blue (worst) to green (best)
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(teams)))
    
    bars = ax.barh(range(len(teams)), values, color=colors, alpha=0.8)
    
    ax.set_yticks(range(len(teams)))
    ax.set_yticklabels([f"{rank}. {team}" for rank, team in zip(ranks, teams)], fontsize=10)
    ax.set_xlabel(f'{statistic} Allowed per Game', fontsize=12)
    ax.set_title(f'NBA Team Defense Rankings - {statistic}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontsize=9, color='white')
    
    plt.tight_layout()
    plt.show() 