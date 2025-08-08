import pandas as pd


def simple_mean(data, category):
    num_games = len(data) - 1
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert the 'DATE' column to datetime format for proper sorting
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Sort the DataFrame by date in descending order
    df = df.sort_values(by='DATE', ascending=False).reset_index(drop=True)

    # Get the numeric data for the category
    df[category] = pd.to_numeric(df[category])

    # Ensure there are enough games in the dataset
    if len(df) < num_games:
        raise ValueError(f"Not enough games in the dataset. Required: {num_games}, Provided: {len(df)}")

    # Calculate the simple mean
    mean = df[category][:num_games].mean()

    return mean
