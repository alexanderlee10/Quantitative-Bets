def clean_mlb_data(data, position):
    # Print the header to debug the available columns
    header = data[0]

    # Define columns to keep for hitters and pitchers
    hitter_columns = ['NAME', 'DATE', 'TM', 'OPP', 'SO', 'R', 'RBI', 'H', 'BB', 'SB', '2B', 'HR', 'TB', 'CS', '3B', 'HBP']
    pitcher_columns = ['NAME', 'DATE', 'TM', 'OPP', 'ER', 'IP', 'H', 'BB', 'SO', 'DEC']

    if position == 'hitter':
        columns_to_keep = hitter_columns
        additional_columns = ['Hitter Fantasy Score']
    else:
        columns_to_keep = pitcher_columns
        additional_columns = ['Pitcher Fantasy Score', 'Pitching Outs']

    # Map columns to standard names for easier access
    column_map = {
        'NAME': 'NAME',
        'DATE': 'DATE',
        'TM': 'TM',
        'OPP': 'OPP',
        'SO': 'Strikeouts',
        'R': 'Runs',
        'RBI': 'RBIs',
        'H': 'Hits',
        'BB': 'Walks',
        'SB': 'Stolen Bases',
        '2B': 'Doubles',
        'HR': 'Home Runs',
        'TB': 'Total Bases',
        'ER': 'Earned Runs Allowed',
        'IP': 'Innings Pitched',
        'DEC': 'Decision',
        'H': 'Hits Allowed',
        'BB': 'Walks Allowed',
        'SO': 'Strikeouts',
        'CS': 'Caught Stealing',
        '3B': 'Triples',
        'HBP': 'Hit By Pitch'
    }

    # Get indices of columns to keep based on mapped names
    indices_to_keep = {col: header.index(col) if col in header else None for col in columns_to_keep}

    # Function to clean a row and add new columns
    def clean_row(row):
        cleaned_row = [row[indices_to_keep[col]] if indices_to_keep[col] is not None else 0 for col in columns_to_keep]

        if position == 'hitter':
            try:
                # Extract values to calculate new columns
                singles = int(row[header.index('H')]) - (int(row[header.index('2B')]) + int(row[header.index('HR')]))
                doubles = int(row[header.index('2B')])
                triples = int(row[header.index('3B')]) if '3B' in header else 0
                home_runs = int(row[header.index('HR')])
                runs = int(row[header.index('R')])
                rbis = int(row[header.index('RBI')])
                walks = int(row[header.index('BB')])
                hbp = int(row[header.index('HBP')]) if 'HBP' in header else 0
                stolen_bases = int(row[header.index('SB')])
                caught_stealing = int(row[header.index('CS')]) if 'CS' in header else 0

                # Calculate fantasy score
                fantasy_score = (singles + 2*doubles + 3*triples + 4*home_runs + runs + rbis + walks + hbp + 2*stolen_bases - caught_stealing)
                cleaned_row.append(fantasy_score)
            except ValueError:
                # Handle cases where conversion to int fails
                return None

        elif position == 'pitcher':
            try:
                # Extract values to calculate new columns
                innings_pitched = float(row[header.index('IP')])
                wins = 1 if row[header.index('DEC')] == 'W' else 0
                saves = 1 if row[header.index('DEC')] == 'SV' else 0
                earned_runs = int(row[header.index('ER')])

                # Calculate fantasy score
                fantasy_score = (wins*4 + saves*2 + int(innings_pitched) + (innings_pitched - int(innings_pitched))*3 - earned_runs)
                pitching_outs = int(innings_pitched) * 3 + (innings_pitched - int(innings_pitched)) * 10

                cleaned_row.append(fantasy_score)
                cleaned_row.append(pitching_outs)
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


def get_mlb_hitter_statistics():
    return ['Strikeouts', 'Runs', 'RBIs', 'Hits', 'Walks', 'Hitter Fantasy Score', 'Stolen Bases', 'Doubles', 'Home Runs', 'Total Bases', 'Caught Stealing', 'Triples', 'Hit By Pitch']

def get_mlb_pitcher_statistics():
    return ['Earned Runs Allowed', 'Pitching Outs', 'Pitcher Fantasy Score', 'Walks Allowed', 'Hits Allowed', 'Strikeouts']
