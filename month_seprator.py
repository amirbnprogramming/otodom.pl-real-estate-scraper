import pymongo
from pymongo import MongoClient
import csv
from datetime import datetime
from collections import defaultdict

from Utils.constants import mongo_url

# MongoDB connection
client = pymongo.MongoClient(mongo_url)
db = client['api_results']
collection = db['Otodom_collection']

start_date = datetime(2023, 6, 1)
end_date = datetime(2024, 6, 30)

# Retrieve records from MongoDB and convert 'created_at' strings to datetime
cursor = collection.find({})

# Initialize a dictionary to store records grouped by month
records_by_month = {}

# Iterate through cursor and group by month
for record in cursor:
    created_at_str = record['created_at']
    created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')

    if start_date <= created_at <= end_date:
        month_name = created_at.strftime('%B_%Y')  # e.g., 'June_2023'

        if month_name not in records_by_month:
            records_by_month[month_name] = []

        records_by_month[month_name].append(record)

# Iterate through grouped records and save each month's data to a CSV file
for month_name, records in records_by_month.items():
    csv_filename = f'exports/{month_name}.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=records[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(records)

    print(f'Saved {len(records)} records for {month_name} to {csv_filename}')

# Close MongoDB connection
client.close()