def clean_nba_data(data):
    # Indices of columns to keep
    columns_to_keep = ['NAME', 'DATE', 'TM', 'OPP', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'TOV', 'PF']

    # Get indices of columns to keep from header
    header = data[0]
    indices_to_keep = [header.index(col) for col in columns_to_keep]

    # Function to clean a row and add new columns
    def clean_row(row):
        cleaned_row = [row[i] for i in indices_to_keep]

        try:
            # Extract values to calculate new columns
            pts = int(row[header.index('PTS')])
            reb = int(row[header.index('REB')])
            ast = int(row[header.index('AST')])
            blk = int(row[header.index('BLK')])
            stl = int(row[header.index('STL')])
        except ValueError:
            # Handle cases where conversion to int fails
            return None

        # Calculate new columns
        pts_reb = pts + reb
        pts_ast = pts + ast
        pts_reb_ast = pts + reb + ast
        blk_stl = blk + stl
        reb_ast = reb + ast

        # Append new columns to the cleaned row
        cleaned_row.extend([pts_reb, pts_ast, pts_reb_ast, blk_stl, reb_ast])

        return cleaned_row

    # Clean data, skipping the header row
    cleaned_data = [clean_row(row) for row in data[1:] if row and 'Average' not in row]

    # Remove any rows that failed to process
    cleaned_data = [row for row in cleaned_data if row is not None]

    # Add new headers for the additional columns
    new_columns = ['PTS + REB', 'PTS + AST', 'PTS + REB + AST', 'BLK + STL', 'REB + AST']
    cleaned_data.insert(0, [header[i] for i in indices_to_keep] + new_columns)

    return cleaned_data

def get_nba_statistics():
    return ['MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'TOV', 'PF', 'PTS + REB', 'PTS + AST', 'PTS + REB + AST', 'BLK + STL', 'REB + AST']
