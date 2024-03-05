##
# Step 1
# Get the data from site and save it to csv file
##

import requests
import csv
from bs4 import BeautifulSoup
import re
from datetime import datetime


#type ='am'
year = '2024'

Time_AM = {
    "code": "A",
    "label": "midday",
}

Time_PM = {
    "code": "P",
    "label": "evening",
}

Times = {'am' : Time_AM, 'pm' : Time_PM}

time_sets = ['am', 'pm']

if (year == '2019'):
    exit()

for t in time_sets:
    type = t
    URL = f"https://www.lotteryleaf.com/on/daily-keno-{Times[type]['label']}/{year}"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    winning_numbers = soup.find_all('ul', class_='nbr-grp')
    dates = soup.find_all('td', class_='win-nbr-date')

    dates.pop(0)  # remove date title

    if winning_numbers:
        csv_filename = f"data/Keno/scraping/extracted_numbers_{Times[type]['label']}_{year}.csv"
        header = ['PlayDate', 'AP'] + [f'N{i:02d}' for i in range(1, 21)]
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            for idx, winning_number in enumerate(winning_numbers):
                date_element = re.sub(r'[^a-zA-Z0-9 ]', '', dates[idx].text.strip()) if dates[idx] else ""
                date_element = datetime.strptime(date_element, "%b %d %Y")
                date_element = date_element.strftime("%Y-%m-%d")
                row_data = [date_element] + [Times[type]['code']] + winning_number.text.split()  # Assuming winning_number is a space-separated string
                # Write the row to the CSV file
                csv_writer.writerow(row_data)
        print(f"Writing to CSV file complete -{year} {Times[type]['label']}")

    else:
        print("No ul element found with class 'nbr-grp'.")
