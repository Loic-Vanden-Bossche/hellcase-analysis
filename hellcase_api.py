import requests
import csv
import json
from datetime import datetime

def fetch_hellcase_data():
    """
    Fetch case data from Hellcase API and save it to a CSV file.

    This function:
    1. Makes a request to the Hellcase API endpoint for CS:GO cases
    2. Parses the JSON response
    3. Extracts case data from the 'main_page' section
    4. Saves the data to a CSV file with a timestamp in the filename

    Returns:
        str: The filename of the created CSV file, or None if an error occurred
    """
    # API endpoint
    url = "https://api.hellcase.com/mainpage?game=csgo"

    try:
        # Make the API request with headers that mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://hellcase.com/',
            'Origin': 'https://hellcase.com'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract cases data from the main_page section
        cases = []
        for section in data.get('main_page', []):
            if 'cases_to_show' in section:
                cases.extend(section['cases_to_show'])

        if not cases:
            print("No case data found in the API response.")
            return

        # Extract is_new and is_top from settings dictionary
        for case in cases:
            if 'settings' in case and isinstance(case['settings'], dict):
                # Extract values from settings
                case['is_new'] = case['settings'].get('is_new', False)
                case['is_top'] = case['settings'].get('is_top', False)
                # Remove the settings field to avoid duplication
                del case['settings']

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hellcase_cases_{timestamp}.csv"

        # Collect all possible fields from all cases to ensure we capture all fields
        # This is important because different cases might have different fields
        all_fields = set()
        for case in cases:
            all_fields.update(case.keys())

        # Define CSV headers based on all possible fields and sort them for consistency
        headers = sorted(list(all_fields))

        # Write data to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for case in cases:
                # Handle nested dictionaries by converting them to JSON strings
                # This is necessary because CSV can't directly store nested structures
                for key, value in case.items():
                    if isinstance(value, dict):
                        case[key] = json.dumps(value)
                # Write the case data to the CSV file
                writer.writerow(case)

        print(f"Successfully saved {len(cases)} cases to {filename}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_hellcase_data()
