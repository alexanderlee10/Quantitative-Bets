# Quantitative-Bets

Quantitative-Bets is a collection of small utilities for pulling and plotting player statistics from [StatMuse](https://www.statmuse.com/). The project focuses on quickly visualizing recent performances and running simple quantitative analysis (mean and weighted mean) to aid sports betting decisions.

## Running the GUI

The repository includes a Tkinter based GUI (`GUI 2.py`) that allows users to choose a league, player, and statistic, then plot the recent game logs. To start the GUI run:

```bash
python "GUI 2.py"
```

The GUI requires an environment with graphical display support. When running headless (e.g. on a server without a display) you will receive an error like `no display name and no $DISPLAY environment variable`.

The application scrapes game data from StatMuse, so an active internet connection is required.

## Python version

The codebase is developed and tested with **Python 3.11**. Python 3.10 or later is recommended.

## Installing dependencies

Install the required packages with pip:

```bash
pip install -r requirements.txt
```

## Usage tips

1. Launch the GUI as shown above.
2. Select a league (NBA, NFL, NHL, or MLB).
3. Enter a player name, team (or "Any"), time duration, and statistic.
4. Optionally adjust the projection line and choose a quantitative analysis method.
5. Press **Generate Plot** to fetch data from StatMuse and visualize recent results.

The script will automatically compute hit rates and display statistics such as the mean or weighted moving average alongside a bar chart of recent games.

