import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def plot_sports_stats(data, parameter, projection, quantitative):
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

    header = data[0]

    try:
        index_to_extract = header.index(parameter)
    except ValueError:
        print(f"Parameter {parameter} not found in header.")
        return

    # Extracting dates, the specified parameter's values, and team abbreviations
    dates = [datetime.strptime(game[header.index('DATE')], '%m/%d/%Y') for game in data[1:] if game[header.index('DATE')]]
    values = [float(game[index_to_extract]) for game in data[1:] if game[index_to_extract]]
    team_abbrs = [game[header.index('TM')] for game in data[1:] if game[header.index('TM')]]

    # Sorting dates, values, and team abbreviations based on dates
    sorted_dates, sorted_values, sorted_team_abbrs = zip(*sorted(zip(dates, values, team_abbrs)))

    x_values = list(range(len(sorted_dates)))

    # Using GridSpec for custom subplot layout
    fig = plt.figure(figsize=(20, 10))
    gs = fig.add_gridspec(2, 4)

    # Bar chart takes up the first two columns
    ax1 = fig.add_subplot(gs[:, :2])
    colors = ['green' if value >= projection else 'red' for value in sorted_values]
    bars = ax1.bar(x_values, sorted_values, width=0.6, color=colors)
    ax1.axhline(y=quantitative, color='purple', linestyle='solid', label=f'Quantitative Line: {quantitative:.2f}')
    ax1.axhline(y=projection, color='yellow', linestyle='dotted', label=f'Projection Line: {projection:.2f}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel(parameter)
    ax1.set_title(f'{parameter} Over Time')
    ax1.set_xticks(x_values)
    ax1.set_xticklabels([date.strftime('%b %d, %Y') for date in sorted_dates], rotation=45, ha='right')
    ax1.legend()
    ax1.grid(False)

    for i, bar in enumerate(bars):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10, color='white')

    # Statistical Analysis
    data = np.array(sorted_values)
    std_dev = np.std(data, ddof=1)
    n = len(data)

    # Confidence Interval Calculation
    t_critical = 2.571  # Critical t-value for 5 degrees of freedom and 95% confidence
    margin_of_error = t_critical * (std_dev / np.sqrt(n))
    conf_interval = (quantitative - margin_of_error, quantitative + margin_of_error)

    # CDF and PDF Calculation for 21.5
    x = projection
    z = (x - quantitative) / std_dev

    def erf(z):
        t = 1.0 / (1.0 + 0.5 * abs(z))
        tau = t * np.exp(-z*z - 1.26551223 + 1.00002368*t + 0.37409196*t*t + 0.09678418*t*t*t - 0.18628806*t*t*t*t + 0.27886807*t*t*t*t*t - 1.13520398*t*t*t*t*t*t + 1.48851587*t*t*t*t*t*t*t - 0.82215223*t*t*t*t*t*t*t*t + 0.17087277*t*t*t*t*t*t*t*t*t)
        return 1 - tau if z >= 0 else tau - 1

    cdf = 0.5 * (1 + erf(z / np.sqrt(2)))

    pdf = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * z**2)

    # Histogram in the third column
    ax2 = fig.add_subplot(gs[0, 2:])
    ax2.hist(data, bins=10, alpha=0.5, color='blue', edgecolor='black')
    ax2.axvline(quantitative, color='purple', linestyle='solid', linewidth=2)
    ax2.axvline(conf_interval[0], color='green', linestyle='dashed', linewidth=2)
    ax2.axvline(conf_interval[1], color='green', linestyle='dashed', linewidth=2)
    ax2.set_title('Histogram of Data')
    ax2.set_xlabel('Value')
    ax2.set_ylabel('Frequency')

    # PDF in the fourth column
    ax3 = fig.add_subplot(gs[1, 2:])
    x_values_pdf = np.linspace(quantitative - 4*std_dev, quantitative + 4*std_dev, 1000)
    pdf_values = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values_pdf - quantitative) / std_dev) ** 2)
    ax3.plot(x_values_pdf, pdf_values, color='blue')
    ax3.axvline(x, color='yellow', linestyle='dashed', linewidth=2)
    ax3.axvline(quantitative, color='purple', linestyle='solid', linewidth=2)
    ax3.fill_between(x_values_pdf, pdf_values, where=(x_values_pdf <= x), color='gray', alpha=0.5)
    ax3.text(projection, 0.02, f"CDF at Projection: {cdf:.4f}", fontsize=12, color='white')
    ax3.set_title('PDF of Normal Distribution')
    ax3.set_xlabel('Value')
    ax3.set_ylabel('Density')

    # Adding text box at the bottom of the figure
    textstr = f"""
    Statistical Analysis of the Given Data 
    Mean: {np.mean(data):.2f}  Std Dev: {std_dev:.2f}  N: {n}  Margin of Error: {margin_of_error:.2f}
    Confidence Interval: [{conf_interval[0]:.2f}, {conf_interval[1]:.2f}] CDF at Projection: {cdf:.4f} PDF at Projection: {pdf:.4f}
    We estimate the chance of it hitting is {(1 - cdf) * 100:.2f}%
    """
    fig.text(0.1, 0.01, textstr, fontsize=12, va='bottom', ha='left', wrap=True)

    plt.tight_layout(rect=[0, 0.14, 1, 0.97])  # Adjust layout to make space for the text box
    plt.show()

