import pandas as pd
from datetime import datetime


def weighted_moving_average(data, category):
    num_games = len(data) - 1

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert the 'DATE' column to datetime format for proper sorting
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Sort the DataFrame by date in descending order
    df = df.sort_values(by='DATE', ascending=False).reset_index(drop=True)

    # Get the numeric data for the category
    df[category] = pd.to_numeric(df[category])

    # Generate weights dynamically decreasing by 0.5
    weights = [num_games - 0.5 * i for i in range(num_games)]

    # Ensure there are enough games in the dataset
    if len(df) < num_games:
        raise ValueError(f"Not enough games in the dataset. Required: {num_games}, Provided: {len(df)}")

    # Calculate the weighted sum
    wma = (df[category][:num_games].values * weights).sum() / sum(weights)

    return wma

