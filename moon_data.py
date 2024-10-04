import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def scrape_url(target_url):
    r = requests.get(target_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table')

    # Extract all rows (tr) from the table
    rows = table.find_all('tr')

    # Extract header cells (th) or data cells (td) from each row
    table_data = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        table_data.append(row_data)

    return table_data



def scrape_moon_phase_card(url):
    # Send a GET request to the URL
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the moon phases card div
    moon_phase_cards = soup.find_all('div', class_='moon-phases-card')

    # Extract data from each card
    moon_data = []
    for card in moon_phase_cards:
        phase_name = card.find('h3').get_text(strip=True)  # Extract phase name
        phase_date = card.find('div', class_='moon-phases-card__date').get_text(strip=True)  # Extract date
        phase_time = card.find('div', class_='moon-phases-card__time').get_text(strip=True)  # Extract time

        moon_data.append({
            'Moon Phase': phase_name,
            'Date': phase_date,
            'Time': phase_time
        })

    return moon_data

def main():
    url1 = "https://www.timeanddate.com/moon/phases/?year=2024"
    data = scrape_moon_phase_card(url1)
    print(data)
    # Write the data to a JSON file
    with open('moon_phases.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Data has been written to moon_phases.json")



if __name__ == "__main__":
    main()

