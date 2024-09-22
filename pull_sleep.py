import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import requests
import json
import pandas as pd
import os

TOKEN= os.getenv('OURA_TOKEN')

if TOKEN is not None:
    print(f"OURA_TOKEN: {TOKEN}")
else:
    print("OURA_TOKEN is not set.")

HOST = "api.ouraring.com" 

params={ 
    'start_date': '2024-08-01', 
    'end_date': '2024-09-01' 
}
headers = { 
  'Authorization': 'Bearer ' + TOKEN 
}


def pull_sleep():
    url = 'https://api.ouraring.com/v2/usercollection/sleep' 
    response = requests.request('GET', url, headers=headers, params=params) 
    data = response.json()
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return data
    
def extract_sleep(data):
    data_list = data.get('data', [])

    total_sleep = {}
    total_bedtime_start = {}

    for item in data_list:
        total_sleep[item['id']] = [item['bedtime_start'], item['bedtime_end']]
        total_bedtime_start[item['id']] = item['bedtime_start']


    return total_bedtime_start

def plot_data(data):

    keys = list(data.keys())
    timestamps = list(data.values())

    datetime_objects = [datetime.fromisoformat(ts) for ts in timestamps]

    dates = [dt.date() for dt in datetime_objects]
    times = [(dt.hour + dt.minute / 60 + dt.second / 3600) for dt in datetime_objects]  # Time in hours

    colors = ['red' if dt.hour < 5 else 'blue' for dt in datetime_objects]

    plt.figure(figsize=(10, 6))

    plt.scatter(dates, times, marker='o', color=colors)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.xlabel('Date')
    plt.ylabel('Time of Day (Hours)')
    plt.title('Timestamps Plot: Date vs. Time')
    plt.xticks(rotation=90)
    plt.grid(True)

    plt.show()



def main():
    resp = pull_sleep()
    selected_data = extract_sleep(resp)

    print(selected_data)

    plot_data(selected_data)


if __name__ == "__main__":
    main()
