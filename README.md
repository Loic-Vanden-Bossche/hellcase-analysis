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
- numpy
- matplotlib
- seaborn
- tabulate

## Installation

```bash
pip install pandas requests numpy matplotlib seaborn tabulate
```

## Case Simulator CLI Tool

The repository includes a command-line tool for simulating case openings and analyzing case data.

### Prerequisites

Before using the simulator, you need to:
1. Run `hellcase_api.py` to fetch basic case information
2. Run `fetch_case_contents.py` to fetch detailed case contents
3. Run `create_case_contents_csv.py` to create the dataset for analysis

### Usage

The CLI tool provides several commands:

#### List Available Cases

```bash
python case_simulator.py list
```

Filter cases by name:
```bash
python case_simulator.py list --filter "knife"
```

#### Analyze Case Metrics

Analyze a specific case:
```bash
python case_simulator.py analyze "Prisma Case"
```

Analyze top cases by different metrics:
```bash
python case_simulator.py analyze --sort ev-ratio --top 10
python case_simulator.py analyze --sort profit-prob --top 5
python case_simulator.py analyze --sort max-profit --top 5
python case_simulator.py analyze --sort price --top 5
```

Available sort metrics:
- `ev`: Expected Value
- `ev-ratio`: Expected Value to Price Ratio
- `profit-prob`: Probability of Profit
- `max-profit`: Maximum Potential Profit
- `price`: Case Price (lowest first)

#### Get Case Recommendations

Get recommendations for all player types:
```bash
python case_simulator.py recommend
```

Get recommendations for a specific player type:
```bash
python case_simulator.py recommend --type profit
python case_simulator.py recommend --type risk-averse
python case_simulator.py recommend --type high-risk
python case_simulator.py recommend --type budget
```

#### Simulate Case Openings

Simulate opening a case once:
```bash
python case_simulator.py simulate "Prisma Case"
```

Simulate multiple openings:
```bash
python case_simulator.py simulate "Prisma Case" -n 100
```

Simulate with visualization (requires matplotlib):
```bash
python case_simulator.py simulate "Prisma Case" -n 100 --plot
```
