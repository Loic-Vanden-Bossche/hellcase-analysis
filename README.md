# Hellcase Case Contents Fetcher

This project contains scripts to fetch and analyze CS:GO case data from Hellcase.

## Overview

The project consists of two main components:

1. A script to fetch basic case information from the Hellcase main page API
2. A script to fetch detailed contents of each case using the case names from the first step

## Files

- `hellcase_api.py`: Fetches basic case information from the Hellcase main page API and saves it to a CSV file
- `fetch_case_contents.py`: Fetches detailed contents of each case using the case names from the CSV file
- `data/cases.csv`: Contains basic information about all cases
- `data/case_contents/`: Directory containing individual JSON files for each case's contents
- `data/case_contents_[timestamp].json`: Combined JSON file containing all case contents

## Usage

### Fetching Basic Case Information

```python
python hellcase_api.py
```

This will fetch basic information about all cases from the Hellcase main page API and save it to a CSV file.

### Fetching Case Contents

```python
python fetch_case_contents.py
```

This will:
1. Read case names from `data/cases.csv`
2. For each case, make a request to the Hellcase API to get its content
3. Save each case's content to an individual JSON file in the `data/case_contents` directory
4. Save all case contents to a combined JSON file with a timestamp in the filename

## Data Structure

### Case Information (CSV)

The `cases.csv` file contains basic information about each case, including:
- `name`: The case identifier used in API requests
- `locale_name`: The display name of the case
- `price`: The current price of the case
- `price_old`: The original price of the case (if discounted)
- `is_new`: Whether the case is marked as new
- `is_top`: Whether the case is marked as top
- And many other attributes...

### Case Contents (JSON)

Each case content JSON file contains detailed information about the items in the case, including:
- `itemlist`: List of items that can be obtained from the case
- `items_without_chances`: List of items without drop chances
- `shards`: List of shards that can be obtained
- And other case metadata...

For each item in `itemlist`, the data includes:
- `item_name`: The name of the item
- `weapon_name`: The weapon type
- `skin_name`: The skin name
- `rarity`: The rarity of the item
- `items`: List of variations of the item with different conditions and StatTrak status
- And other item attributes...

## Requirements

- Python 3.6+
- pandas
- requests

## Installation

```bash
pip install pandas requests
```