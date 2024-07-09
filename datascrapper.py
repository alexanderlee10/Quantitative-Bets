import requests
from bs4 import BeautifulSoup
from datetime import datetime


def geturl(league: str, player_name: str, team: str, time_duration: str):
    """Get the URL for StatMuse"""
    return f"https://www.statmuse.com/{league}/ask/{player_name}-vs-{team}-{time_duration}"

# something important for the get_url
# we can leave the team blank if we want the 7 games of any game they played
#time duration is a bit complex but will be easier our combined we will have to figure that out.
# I am thinking the last 6 games of the player and the last 5 games against that team
# "last-5-regular-season-games', "last-5-playoff-games', "playoff-game-log", "combined" the number can alawys be changed

def scrape_statmuse(url):
    """
    Scrapes data from a StatMuse page and returns it as a nested list.
    """
    if "combined" in url:
        data1 = scrape_statmuse(url[:-8] + "last-5-regular-season-games")
        data2 = scrape_statmuse(slice_after_vs(url) + "last-6-games")
        return sort_combined_data(data1 + data2)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table
    table = soup.find('table')
    if not table:
        print("No table found on the page.")
        return []

    # Extract headers
    headers = [header.get_text(strip=True) for header in table.find_all('th')]

    # Extract rows
    rows = table.find_all('tr')
    data = [headers]

    for row in rows[1:]:
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]

        # Skip empty rows and totals
        if any(cell.strip() for cell in row_data) and 'Total' not in row_data:
            data.append(row_data)

    return data


def slice_after_vs(url):
    """Find and slice the URL after 'vs-'"""
    index = url.find("vs-")
    if index != -1:
        return url[:index + len("vs-")]
    return url


def sort_combined_data(nested_list):
    # Find the index of the "DATE" column
    header = nested_list[0]
    date_index = header.index("DATE")

    # Function to parse the date from each row
    def get_date(row):
        try:
            return datetime.strptime(row[date_index], '%m/%d/%Y')
        except ValueError:
            return datetime.min  # Return the smallest date for non-date rows (headers or averages)

    # Separate the header and filter out rows with "Average" and duplicate headers
    header = nested_list[0]
    data = [row for row in nested_list[1:] if row[date_index] and "Average" not in row and row != header]

    # Sort the data by date
    sorted_data = sorted(data, key=get_date)

    # Reconstruct the nested list with the header and sorted data
    sorted_nested_list = [header] + sorted_data

    return sorted_nested_list
