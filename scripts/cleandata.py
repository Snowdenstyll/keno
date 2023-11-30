import os
import csv
import re
import requests
from bs4 import BeautifulSoup
import operator

year='2023'
# Function to switch between 'P' and 'A'
def switch_ap(current_ap):
    return 'A' if current_ap == 'P' else 'P'

# Function to get the last 'AP' value from a CSV file
def get_last_ap(csv_filename):
    try:
        with open(csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            last_row = list(reader)[-1]
            return last_row[1] if last_row else 'P'  # Default to 'P' if the file is empty
    except FileNotFoundError:
        return 'P'  # Default to 'P' if the file doesn't exist

# Your existing code...

# Ensure the directories exist, create them if not
output_directory = 'data/scraping/'
os.makedirs(output_directory, exist_ok=True)

# File paths for the existing CSV files
evening_csv_filename = os.path.join(output_directory, f'extracted_numbers_evening_{year}.csv')
midday_csv_filename = os.path.join(output_directory, f'extracted_numbers_midday_{year}.csv')

# Get the last 'AP' values from the existing CSV files
last_evening_ap = get_last_ap(evening_csv_filename)
last_midday_ap = get_last_ap(midday_csv_filename)

# Determine the starting 'AP' for the new CSV file
starting_ap = switch_ap(last_midday_ap)

evening_list = list
midday_list = list

with open(evening_csv_filename, newline='') as csvfile:
    evening_csv = csv.reader(csvfile, quotechar='|')
    evening_list = list(evening_csv)
    evening_list.pop(0)

with open(midday_csv_filename, newline='') as csvfile:
    midday_csv = csv.reader(csvfile, quotechar='|')
    midday_list = list(midday_csv)
    midday_list.pop(0)

length = len(list(midday_list))

csv_filename = f"data/formatted/{year}.csv"
header = ['PlayDate', 'AP'] + [f'N{i:02d}' for i in range(1, 21)]

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    index_balancer = 0
    for idx in range(length):
        row_data_evening = evening_list[idx - index_balancer]
        row_data_midday = midday_list[idx]
        if (row_data_evening[0] != row_data_midday[0]):
            index_balancer+=1
            row_data_evening = []

        csv_writer.writerow(row_data_evening)
        csv_writer.writerow(row_data_midday)