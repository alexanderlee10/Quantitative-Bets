def clean_nhl_data(data, position):
    # Print the header to debug the available columns
    header = data[0]

    # Define columns to keep for players and goalies
    player_columns = ['NAME', 'DATE', 'TM', 'OPP', 'G', 'A', 'P', 'S', 'TOI', 'FOW', 'HIT', 'BKS']
    goalie_columns = ['NAME', 'DATE', 'TM', 'OPP', 'SV', 'MIN']

    if position == 'player':
        columns_to_keep = player_columns
        additional_columns = ['SOG + BS']
    else:
        columns_to_keep = goalie_columns
        additional_columns = []

    # Map columns to standard names for easier access
    column_map = {
        'NAME': 'NAME',
        'DATE': 'DATE',
        'TM': 'TM',
        'OPP': 'OPP',
        'SV': 'Saves',  # Rename SV to Saves
        'MIN': 'Time On Ice',  # Rename MIN to Time On Ice
        'P': 'Points',
        'G': 'Goals',
        'S': 'Shots On Goal',
        'A': 'Assists',
        'TOI': 'Time On Ice',
        'FOW': 'Faceoffs Won',
        'HIT': 'Hits',
        'BKS': 'Blocked Shots'
    }

    # Get indices of columns to keep based on mapped names
    indices_to_keep = {col: header.index(col) if col in header else None for col in columns_to_keep}

    # Function to clean a row and add new columns
    def clean_row(row):
        cleaned_row = [row[indices_to_keep[col]] if indices_to_keep[col] is not None else 0 for col in columns_to_keep]

        if position == 'player':
            try:
                # Extract values to calculate new columns
                sog = int(row[header.index('S')]) if 'S' in header else 0
                bs = int(row[header.index('BKS')]) if 'BKS' in header else 0

                # Calculate new columns
                sog_bs = sog + bs
                cleaned_row.append(sog_bs)
            except ValueError:
                # Handle cases where conversion to int fails
                return None

        return cleaned_row

    # Clean data, skipping the header row
    cleaned_data = [clean_row(row) for row in data[1:] if row and 'Average' not in row]

    # Remove any rows that failed to process
    cleaned_data = [row for row in cleaned_data if row is not None]

    # Rename the headers
    renamed_headers = [column_map.get(col, col) for col in columns_to_keep] + additional_columns
    cleaned_data.insert(0, renamed_headers)

    return cleaned_data


def get_nhl_player_statistics():
    return ['Points', 'Goals', 'Shots On Goal', 'Assists', 'Time On Ice', 'Faceoffs Won', 'Hits', 'Blocked Shots', 'SOG + BS']

def get_nhl_goalie_statistics():
    return ['Saves', 'Time On Ice']
