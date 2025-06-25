import json
import pandas as pd
import os

def create_case_contents_csv():
    """
    Process the case_contents.json file and create a CSV dataset with sub-items and their parent data.
    
    This function:
    1. Reads the case_contents.json file
    2. Extracts parent item data and sub-item data
    3. Combines them into a single dataset
    4. Saves the result as a CSV file
    
    Returns:
        str: The filename of the created CSV file, or None if an error occurred
    """
    # Path to the case_contents.json file
    json_file = 'data/case_contents.json'
    
    # Output CSV file path
    output_file = 'data/case_contents_dataset.csv'
    
    try:
        # Read the JSON file
        print(f"Reading {json_file}...")
        with open(json_file, 'r', encoding='utf-8') as f:
            case_contents = json.load(f)
        
        print(f"Successfully loaded {json_file}")
        
        # List to store all items with their parent data
        all_items = []
        
        # Process each case
        for case_name, case_data in case_contents.items():
            print(f"Processing case: {case_name}")
            
            # Check if itemlist exists in the case data
            if 'itemlist' not in case_data:
                print(f"Warning: No itemlist found for case {case_name}")
                continue
            
            # Process each parent item in the case
            for parent_item in case_data['itemlist']:
                # Extract parent item data
                parent_data = {
                    'case_name': case_name,
                    'item_name': parent_item.get('item_name', ''),
                    'weapon_name': parent_item.get('weapon_name', ''),
                    'skin_name': parent_item.get('skin_name', ''),
                    'rarity': parent_item.get('rarity', ''),
                    'steam_type': parent_item.get('steam_type', ''),
                    'steam_itemtype': parent_item.get('steam_itemtype', ''),
                    'steam_exterior': parent_item.get('steam_exterior', ''),
                    'steam_short_exterior': parent_item.get('steam_short_exterior', ''),
                    'is_stattrak': parent_item.get('is_stattrak', False),
                    'steam_is_souvenir': parent_item.get('steam_is_souvenir', False),
                    'steam_market_hash_name': parent_item.get('steam_market_hash_name', ''),
                    'steam_image': parent_item.get('steam_image', ''),
                    'is_shard': parent_item.get('is_shard', False),
                    'game': parent_item.get('game', '')
                }
                
                # Check if the parent item has sub-items
                if 'items' in parent_item and parent_item['items']:
                    # Process each sub-item
                    for sub_item in parent_item['items']:
                        # Create a copy of parent data
                        item_data = parent_data.copy()
                        
                        # Add sub-item specific data
                        item_data.update({
                            'is_sub_item': True,
                            'min': sub_item.get('min', 0),
                            'max': sub_item.get('max', 0),
                            'odds': sub_item.get('odds', 0),
                            'sub_steam_exterior': sub_item.get('steam_exterior', ''),
                            'sub_steam_short_exterior': sub_item.get('steam_short_exterior', ''),
                            'sub_is_stattrak': sub_item.get('is_stattrak', False),
                            'sub_rarity': sub_item.get('rarity', ''),
                            'sub_steam_image': sub_item.get('steam_image', ''),
                            'sub_game': sub_item.get('game', ''),
                            'sub_steam_price_en': sub_item.get('steam_price_en', 0)
                        })
                        
                        # Add to the list of all items
                        all_items.append(item_data)
                else:
                    # If there are no sub-items, add the parent item as is
                    parent_data['is_sub_item'] = False
                    all_items.append(parent_data)
        
        # Create a DataFrame from the list of items
        df = pd.DataFrame(all_items)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"Successfully created CSV dataset with {len(df)} items")
        print(f"Saved to {output_file}")
        
        return output_file
    
    except FileNotFoundError:
        print(f"Error: File {json_file} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    create_case_contents_csv()