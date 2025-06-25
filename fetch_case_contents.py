import requests
import pandas as pd
import json
import time
import os
from datetime import datetime

def fetch_case_contents():
    """
    Fetch the contents of each case from the Hellcase API.
    
    This function:
    1. Reads case names from data/cases.csv
    2. For each case, makes a request to the Hellcase API to get its content
    3. Saves the response data to a JSON file
    
    Returns:
        str: The filename of the created JSON file, or None if an error occurred
    """
    # Create a directory to store case contents if it doesn't exist
    os.makedirs('data/case_contents', exist_ok=True)
    
    # Read case names from CSV file
    try:
        df = pd.read_csv('data/cases.csv')
        case_names = df['name'].tolist()
        print(f"Found {len(case_names)} cases in the CSV file.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    # Headers for API requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://hellcase.com/',
        'Origin': 'https://hellcase.com'
    }
    
    # Dictionary to store case contents
    case_contents = {}
    
    # Counter for successful and failed requests
    successful = 0
    failed = 0
    
    # Generate timestamp for the output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/case_contents_{timestamp}.json"
    
    # Fetch content for each case
    for i, case_name in enumerate(case_names):
        print(f"Processing case {i+1}/{len(case_names)}: {case_name}")
        
        # Construct API URL
        url = f"https://api.hellcase.com/open/{case_name}"
        
        try:
            # Make API request
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse JSON response
            data = response.json()
            
            # Save individual case content to a file
            case_file = f"data/case_contents/{case_name}.json"
            with open(case_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Add to the combined dictionary
            case_contents[case_name] = data
            successful += 1
            
            # Print success message
            print(f"  Success: Saved content for {case_name}")
            
            # Sleep to avoid overwhelming the API
            time.sleep(1)  # 1 second delay between requests
            
        except requests.exceptions.RequestException as e:
            print(f"  Error making API request for {case_name}: {e}")
            failed += 1
        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON response for {case_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  An unexpected error occurred for {case_name}: {e}")
            failed += 1
        
        # Save the combined data periodically (every 10 cases)
        if (i + 1) % 10 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(case_contents, f, indent=2)
            print(f"Saved progress to {output_file} after {i+1} cases")
    
    # Save the final combined data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(case_contents, f, indent=2)
    
    print(f"\nCompleted processing {len(case_names)} cases:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"Saved all case contents to {output_file}")
    
    return output_file

if __name__ == "__main__":
    fetch_case_contents()