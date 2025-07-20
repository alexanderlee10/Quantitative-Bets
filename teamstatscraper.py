from datascrapper import scrape_statmuse
import pandas as pd

url = "https://www.statmuse.com/nba/ask/nba-teams-that-gives-up-the-most-assists-this-season"

# Scrape the data from the provided URL
data = scrape_statmuse(url)

def clean_team_nba_data(data):
    # Define which columns to keep (including 'OPP AST')
    columns_to_keep = [
        'TEAM', 'SEASON', 'OPP AST', 'GP', 'MPG', 'PPG', 'RPG', 'APG', 'SPG', 'BPG',
        'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'TOV', 'PF',
          # make sure this is included
    ]

    # Get header and indices of columns to keep
    header = data[0]
    indices_to_keep = [header.index(col) for col in columns_to_keep]

    def clean_row(row):
        try:
            # Keep only selected fields
            cleaned = [row[i] for i in indices_to_keep]

            # Convert to float for calculations
            pts = float(row[header.index('PPG')])
            reb = float(row[header.index('RPG')])
            ast = float(row[header.index('APG')])
            blk = float(row[header.index('BPG')])
            stl = float(row[header.index('SPG')])
        except ValueError:
            return None

        # Calculated advanced metrics
        pts_reb = pts + reb
        pts_ast = pts + ast
        pts_reb_ast = pts + reb + ast
        blk_stl = blk + stl
        reb_ast = reb + ast

        # Add new values
        cleaned.extend([
            round(pts_reb, 1),
            round(pts_ast, 1),
            round(pts_reb_ast, 1),
            round(blk_stl, 1),
            round(reb_ast, 1)
        ])
        return cleaned

    # Clean all rows and drop any that fail
    cleaned_data = [clean_row(row) for row in data[1:] if row]
    cleaned_data = [row for row in cleaned_data if row is not None]

    # Add updated header
    new_columns = ['PTS + REB', 'PTS + AST', 'PTS + REB + AST', 'BLK + STL', 'REB + AST']
    cleaned_data.insert(0, [header[i] for i in indices_to_keep] + new_columns)

    return cleaned_data


t = clean_team_nba_data(data)

for i in t:
    print(i)
