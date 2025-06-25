import csv

# Open the most recent CSV file
filename = "data/cases.csv"

with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Print the headers (column names)
    print("CSV Headers:")
    print(reader.fieldnames)
    
    # Print the first row to verify the data
    first_row = next(reader, None)
    if first_row:
        print("\nFirst row data:")
        for key, value in first_row.items():
            print(f"{key}: {value}")