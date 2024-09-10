import csv
from datetime import datetime

from Constants import csv_filename, csv_header

start_date = datetime(2023, 6, 1) # June 2023
end_date = datetime(2024, 6, 30)  # June 2024
records_by_month = {}

# Open the CSV file for reading
with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    # Skip the first row (header row)
    next(reader, None)

    # Iterate over each row starting from the second row
    for row in reader:
        created_at_str = row[-4]
        created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
        if start_date <= created_at <= end_date:
            month_name = created_at.strftime('%B_%Y')
            if month_name not in records_by_month:
                records_by_month[month_name] = []
            records_by_month[month_name].append(row)

# Iterate through grouped records and save each month's data to a CSV file
for month_name, records in records_by_month.items():
    csv_filename = f'exports/{month_name}.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        writer.writerows(records)

    print(f'Saved {len(records)} records for {month_name} to {csv_filename}')

