#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Case Simulator CLI Tool

This script provides a command-line interface for simulating case openings
and analyzing case data from Hellcase.
"""

import argparse
import pandas as pd
import numpy as np
import json
import os
import random
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """
    Load the necessary data files for analysis and simulation.
    
    Returns:
        tuple: (cases_df, case_contents_df) - DataFrames containing case data and case contents
    """
    # Check if data files exist
    if not os.path.exists('data/cases.csv'):
        print("Error: data/cases.csv not found. Please run hellcase_api.py first.")
        return None, None
    
    if not os.path.exists('data/case_contents_dataset.csv'):
        print("Error: data/case_contents_dataset.csv not found. Please run create_case_contents_csv.py first.")
        return None, None
    
    # Load data
    cases_df = pd.read_csv('data/cases.csv')
    case_contents_df = pd.read_csv('data/case_contents_dataset.csv')
    
    return cases_df, case_contents_df

def calculate_ev_metrics(cases_df, case_contents_df):
    """
    Calculate expected value metrics for all cases.
    
    Args:
        cases_df (DataFrame): DataFrame containing case data
        case_contents_df (DataFrame): DataFrame containing case contents data
    
    Returns:
        DataFrame: DataFrame with expected value metrics for each case
    """
    case_ev = []
    
    for case_name in case_contents_df['case_name'].unique():
        case_items = case_contents_df[case_contents_df['case_name'] == case_name]
        
        # Calculate expected value (sum of item price * probability)
        ev = 0
        if 'odds' in case_items.columns and 'sub_steam_price_en' in case_items.columns:
            ev = (case_items['odds'] * case_items['sub_steam_price_en']).sum()
        
        # Get case price from the cases dataframe
        case_price = cases_df[cases_df['name'] == case_name]['price'].values[0] if case_name in cases_df['name'].values else None
        
        case_ev.append({
            'Case Name': case_name,
            'Expected Value': ev,
            'Case Price': case_price,
            'EV Ratio': ev / case_price if case_price else None
        })
    
    ev_df = pd.DataFrame(case_ev)
    ev_df = ev_df.dropna().sort_values('EV Ratio', ascending=False)
    
    return ev_df

def calculate_risk_metrics(cases_df, case_contents_df, top_cases=None):
    """
    Calculate risk metrics for cases.
    
    Args:
        cases_df (DataFrame): DataFrame containing case data
        case_contents_df (DataFrame): DataFrame containing case contents data
        top_cases (list, optional): List of case names to calculate metrics for. If None, calculate for all cases.
    
    Returns:
        DataFrame: DataFrame with risk metrics for each case
    """
    risk_metrics = []
    
    # If top_cases is None, use all cases
    if top_cases is None:
        top_cases = case_contents_df['case_name'].unique()
    
    for case_name in top_cases:
        case_items = case_contents_df[case_contents_df['case_name'] == case_name]
        
        if 'odds' in case_items.columns and 'sub_steam_price_en' in case_items.columns:
            # Calculate variance and standard deviation
            expected_value = (case_items['odds'] * case_items['sub_steam_price_en']).sum()
            variance = (case_items['odds'] * (case_items['sub_steam_price_en'] - expected_value)**2).sum()
            std_dev = np.sqrt(variance)
            
            # Calculate probability of profit
            case_price = cases_df[cases_df['name'] == case_name]['price'].values[0] if case_name in cases_df['name'].values else 0
            
            # Check if odds need normalization (if sum of all odds > 1)
            total_odds = case_items['odds'].sum()
            if total_odds > 1:
                # Normalize the odds so they sum to 1
                normalized_odds = case_items['odds'] / total_odds
                # Calculate probability using normalized odds
                prob_profit = normalized_odds[case_items['sub_steam_price_en'] > case_price].sum() * 100
            else:
                # If odds are already normalized or sum to less than 1, use them directly
                prob_profit = case_items[case_items['sub_steam_price_en'] > case_price]['odds'].sum() * 100
            
            # Calculate max potential profit
            max_item_value = case_items['sub_steam_price_en'].max()
            max_profit = max_item_value - case_price
            
            risk_metrics.append({
                'Case Name': case_name,
                'Expected Value': expected_value,
                'Standard Deviation': std_dev,
                'Coefficient of Variation': std_dev / expected_value if expected_value else float('inf'),
                'Probability of Profit (%)': prob_profit,
                'Max Potential Profit': max_profit
            })
    
    risk_df = pd.DataFrame(risk_metrics)
    
    return risk_df

def get_recommendations(ev_df, risk_df, cases_df, player_type='profit'):
    """
    Get case recommendations based on player type.
    
    Args:
        ev_df (DataFrame): DataFrame with expected value metrics
        risk_df (DataFrame): DataFrame with risk metrics
        cases_df (DataFrame): DataFrame with case data
        player_type (str): Type of player to get recommendations for
            ('profit', 'risk-averse', 'high-risk', 'budget', 'all')
    
    Returns:
        DataFrame: DataFrame with recommended cases
    """
    if player_type == 'profit':
        # For profit-focused players: highest EV Ratio
        return ev_df.head(5)
    
    elif player_type == 'risk-averse':
        # For risk-averse players: highest probability of profit and lowest coefficient of variation
        prob_profit_df = risk_df.sort_values('Probability of Profit (%)', ascending=False).head(5)
        low_var_df = risk_df.sort_values('Coefficient of Variation').head(5)
        return pd.concat([prob_profit_df, low_var_df]).drop_duplicates()
    
    elif player_type == 'high-risk':
        # For high-risk players: highest max potential profit
        return risk_df.sort_values('Max Potential Profit', ascending=False).head(5)
    
    elif player_type == 'budget':
        # For budget-conscious players: affordable cases with decent EV
        budget_cases = cases_df[cases_df['price'] < 5]['name'].tolist()
        budget_ev = ev_df[ev_df['Case Name'].isin(budget_cases)].sort_values('EV Ratio', ascending=False).head(5)
        return budget_ev
    
    elif player_type == 'all':
        # Return all recommendations
        recommendations = {
            'Profit-Focused': get_recommendations(ev_df, risk_df, cases_df, 'profit'),
            'Risk-Averse': get_recommendations(ev_df, risk_df, cases_df, 'risk-averse'),
            'High-Risk': get_recommendations(ev_df, risk_df, cases_df, 'high-risk'),
            'Budget': get_recommendations(ev_df, risk_df, cases_df, 'budget')
        }
        return recommendations
    
    else:
        print(f"Unknown player type: {player_type}")
        return None

def simulate_case_opening(case_name, cases_df, case_contents_df, num_openings=1):
    """
    Simulate opening a specific case a number of times.
    
    Args:
        case_name (str): Name of the case to simulate
        cases_df (DataFrame): DataFrame containing case data
        case_contents_df (DataFrame): DataFrame containing case contents data
        num_openings (int): Number of case openings to simulate
    
    Returns:
        dict: Results of the simulation
    """
    # Get case items and their odds
    case_items = case_contents_df[case_contents_df['case_name'] == case_name]
    
    if case_items.empty:
        print(f"Error: Case '{case_name}' not found in the dataset.")
        return None
    
    # Get case price
    case_price = cases_df[cases_df['name'] == case_name]['price'].values[0] if case_name in cases_df['name'].values else 0
    
    # Check if odds need normalization
    total_odds = case_items['odds'].sum()
    if total_odds > 1:
        # Normalize the odds so they sum to 1
        case_items = case_items.copy()
        case_items['odds'] = case_items['odds'] / total_odds
    
    # Prepare for simulation
    items = []
    odds = []
    prices = []
    
    for _, item in case_items.iterrows():
        if pd.notna(item['odds']) and pd.notna(item['sub_steam_price_en']):
            items.append(f"{item['weapon_name']} | {item['skin_name']} ({item['sub_steam_short_exterior']})")
            odds.append(item['odds'])
            prices.append(item['sub_steam_price_en'])
    
    # Normalize odds if they don't sum to 1
    odds_sum = sum(odds)
    if abs(odds_sum - 1) > 0.01:  # Allow for small floating-point errors
        odds = [o / odds_sum for o in odds]
    
    # Simulate openings
    results = []
    total_cost = case_price * num_openings
    total_value = 0
    
    for _ in range(num_openings):
        # Randomly select an item based on odds
        item_index = random.choices(range(len(items)), weights=odds, k=1)[0]
        item_name = items[item_index]
        item_price = prices[item_index]
        
        results.append({
            'Item': item_name,
            'Value': item_price,
            'Profit': item_price - case_price
        })
        
        total_value += item_price
    
    # Calculate summary statistics
    total_profit = total_value - total_cost
    profit_items = sum(1 for r in results if r['Profit'] > 0)
    profit_percentage = (profit_items / num_openings) * 100 if num_openings > 0 else 0
    
    # Return simulation results
    return {
        'case_name': case_name,
        'num_openings': num_openings,
        'total_cost': total_cost,
        'total_value': total_value,
        'total_profit': total_profit,
        'profit_percentage': profit_percentage,
        'roi': (total_profit / total_cost) * 100 if total_cost > 0 else 0,
        'items': results
    }

def display_simulation_results(results):
    """
    Display the results of a case opening simulation.
    
    Args:
        results (dict): Results of the simulation
    """
    if not results:
        return
    
    print(f"\n=== Simulation Results for {results['case_name']} ===")
    print(f"Number of openings: {results['num_openings']}")
    print(f"Total cost: ${results['total_cost']:.2f}")
    print(f"Total value: ${results['total_value']:.2f}")
    print(f"Total profit/loss: ${results['total_profit']:.2f}")
    print(f"ROI: {results['roi']:.2f}%")
    print(f"Profitable items: {results['profit_percentage']:.2f}%")
    
    # Display item distribution if there are multiple openings
    if results['num_openings'] > 1:
        # Count item occurrences
        item_counts = {}
        for item in results['items']:
            item_name = item['Item']
            if item_name in item_counts:
                item_counts[item_name] += 1
            else:
                item_counts[item_name] = 1
        
        # Sort by count (descending)
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        
        print("\nItem Distribution:")
        table_data = []
        for item_name, count in sorted_items:
            percentage = (count / results['num_openings']) * 100
            table_data.append([item_name, count, f"{percentage:.2f}%"])
        
        print(tabulate(table_data, headers=["Item", "Count", "Percentage"], tablefmt="grid"))
    
    # Display all items if requested or if there are few openings
    if results['num_openings'] <= 10:
        print("\nItems Received:")
        table_data = []
        for i, item in enumerate(results['items'], 1):
            table_data.append([i, item['Item'], f"${item['Value']:.2f}", f"${item['Profit']:.2f}"])
        
        print(tabulate(table_data, headers=["#", "Item", "Value", "Profit/Loss"], tablefmt="grid"))

def plot_simulation_results(results):
    """
    Plot the results of a case opening simulation.
    
    Args:
        results (dict): Results of the simulation
    """
    if not results or results['num_openings'] <= 1:
        return
    
    # Set up the figure
    plt.figure(figsize=(12, 8))
    
    # Extract profit/loss values
    profits = [item['Profit'] for item in results['items']]
    
    # Plot profit/loss distribution
    plt.subplot(2, 1, 1)
    sns.histplot(profits, kde=True)
    plt.axvline(x=0, color='r', linestyle='--', label='Break-even')
    plt.axvline(x=np.mean(profits), color='g', linestyle='-', label=f'Mean: ${np.mean(profits):.2f}')
    plt.title(f'Profit/Loss Distribution for {results["case_name"]} ({results["num_openings"]} openings)')
    plt.xlabel('Profit/Loss ($)')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Plot cumulative profit/loss
    plt.subplot(2, 1, 2)
    cumulative_profit = np.cumsum(profits)
    plt.plot(range(1, len(cumulative_profit) + 1), cumulative_profit)
    plt.axhline(y=0, color='r', linestyle='--', label='Break-even')
    plt.title('Cumulative Profit/Loss Over Time')
    plt.xlabel('Number of Openings')
    plt.ylabel('Cumulative Profit/Loss ($)')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    """Main function to handle command-line arguments and execute the appropriate action."""
    parser = argparse.ArgumentParser(description='Case Simulator CLI Tool')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Simulate command
    simulate_parser = subparsers.add_parser('simulate', help='Simulate case openings')
    simulate_parser.add_argument('case_name', help='Name of the case to simulate')
    simulate_parser.add_argument('-n', '--num', type=int, default=1, help='Number of case openings to simulate')
    simulate_parser.add_argument('--plot', action='store_true', help='Plot the simulation results')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze case metrics')
    analyze_parser.add_argument('case_name', nargs='?', help='Name of the case to analyze (optional)')
    analyze_parser.add_argument('--top', type=int, default=10, help='Number of top cases to display')
    analyze_parser.add_argument('--sort', choices=['ev', 'ev-ratio', 'profit-prob', 'max-profit', 'price'], 
                               default='ev-ratio', help='Sort metric')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get case recommendations')
    recommend_parser.add_argument('--type', choices=['profit', 'risk-averse', 'high-risk', 'budget', 'all'], 
                                 default='all', help='Player type for recommendations')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available cases')
    list_parser.add_argument('--filter', help='Filter cases by name (case-insensitive)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load data
    cases_df, case_contents_df = load_data()
    if cases_df is None or case_contents_df is None:
        return
    
    # Calculate metrics
    ev_df = calculate_ev_metrics(cases_df, case_contents_df)
    
    # Execute the appropriate command
    if args.command == 'simulate':
        results = simulate_case_opening(args.case_name, cases_df, case_contents_df, args.num)
        if results:
            display_simulation_results(results)
            if args.plot and args.num > 1:
                plot_simulation_results(results)
    
    elif args.command == 'analyze':
        if args.case_name:
            # Analyze a specific case
            case_ev = ev_df[ev_df['Case Name'] == args.case_name]
            if case_ev.empty:
                print(f"Error: Case '{args.case_name}' not found in the dataset.")
                return
            
            risk_df = calculate_risk_metrics(cases_df, case_contents_df, [args.case_name])
            
            print(f"\n=== Analysis for {args.case_name} ===")
            print(f"Case Price: ${case_ev['Case Price'].values[0]:.2f}")
            print(f"Expected Value: ${case_ev['Expected Value'].values[0]:.2f}")
            print(f"EV Ratio: {case_ev['EV Ratio'].values[0]:.2f}")
            
            if not risk_df.empty:
                print(f"Standard Deviation: ${risk_df['Standard Deviation'].values[0]:.2f}")
                print(f"Coefficient of Variation: {risk_df['Coefficient of Variation'].values[0]:.2f}")
                print(f"Probability of Profit: {risk_df['Probability of Profit (%)'].values[0]:.2f}%")
                print(f"Max Potential Profit: ${risk_df['Max Potential Profit'].values[0]:.2f}")
        else:
            # Analyze top cases
            if args.sort == 'ev':
                sorted_df = ev_df.sort_values('Expected Value', ascending=False).head(args.top)
                print(f"\n=== Top {args.top} Cases by Expected Value ===")
                print(tabulate(sorted_df[['Case Name', 'Expected Value', 'Case Price', 'EV Ratio']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            elif args.sort == 'ev-ratio':
                sorted_df = ev_df.sort_values('EV Ratio', ascending=False).head(args.top)
                print(f"\n=== Top {args.top} Cases by EV Ratio ===")
                print(tabulate(sorted_df[['Case Name', 'Expected Value', 'Case Price', 'EV Ratio']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            elif args.sort == 'profit-prob' or args.sort == 'max-profit':
                risk_df = calculate_risk_metrics(cases_df, case_contents_df, ev_df['Case Name'].tolist())
                
                if args.sort == 'profit-prob':
                    sorted_df = risk_df.sort_values('Probability of Profit (%)', ascending=False).head(args.top)
                    print(f"\n=== Top {args.top} Cases by Probability of Profit ===")
                    print(tabulate(sorted_df[['Case Name', 'Probability of Profit (%)', 'Expected Value', 'Coefficient of Variation']], 
                                  headers='keys', tablefmt='grid', floatfmt='.2f'))
                else:
                    sorted_df = risk_df.sort_values('Max Potential Profit', ascending=False).head(args.top)
                    print(f"\n=== Top {args.top} Cases by Maximum Potential Profit ===")
                    print(tabulate(sorted_df[['Case Name', 'Max Potential Profit', 'Expected Value', 'Probability of Profit (%)']], 
                                  headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            elif args.sort == 'price':
                sorted_df = cases_df.sort_values('price').head(args.top)
                print(f"\n=== Top {args.top} Cases by Lowest Price ===")
                print(tabulate(sorted_df[['name', 'price']], 
                              headers=['Case Name', 'Price'], tablefmt='grid', floatfmt='.2f'))
    
    elif args.command == 'recommend':
        risk_df = calculate_risk_metrics(cases_df, case_contents_df, ev_df['Case Name'].tolist())
        
        if args.type == 'all':
            recommendations = get_recommendations(ev_df, risk_df, cases_df, 'all')
            
            print("\n=== Case Recommendations ===")
            
            print("\nFor Profit-Focused Players:")
            print(tabulate(recommendations['Profit-Focused'][['Case Name', 'Expected Value', 'Case Price', 'EV Ratio']], 
                          headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            print("\nFor Risk-Averse Players:")
            print(tabulate(recommendations['Risk-Averse'][['Case Name', 'Probability of Profit (%)', 'Coefficient of Variation']], 
                          headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            print("\nFor High-Risk Players:")
            print(tabulate(recommendations['High-Risk'][['Case Name', 'Max Potential Profit', 'Expected Value']], 
                          headers='keys', tablefmt='grid', floatfmt='.2f'))
            
            print("\nFor Budget-Conscious Players:")
            print(tabulate(recommendations['Budget'][['Case Name', 'Case Price', 'EV Ratio']], 
                          headers='keys', tablefmt='grid', floatfmt='.2f'))
        else:
            recommendations = get_recommendations(ev_df, risk_df, cases_df, args.type)
            
            print(f"\n=== Case Recommendations for {args.type.capitalize()} Players ===")
            
            if args.type == 'profit':
                print(tabulate(recommendations[['Case Name', 'Expected Value', 'Case Price', 'EV Ratio']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
            elif args.type == 'risk-averse':
                print(tabulate(recommendations[['Case Name', 'Probability of Profit (%)', 'Coefficient of Variation']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
            elif args.type == 'high-risk':
                print(tabulate(recommendations[['Case Name', 'Max Potential Profit', 'Expected Value']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
            elif args.type == 'budget':
                print(tabulate(recommendations[['Case Name', 'Case Price', 'EV Ratio']], 
                              headers='keys', tablefmt='grid', floatfmt='.2f'))
    
    elif args.command == 'list':
        if args.filter:
            filtered_cases = cases_df[cases_df['name'].str.contains(args.filter, case=False)]
            print(f"\n=== Cases Matching '{args.filter}' ===")
            print(tabulate(filtered_cases[['name', 'price']], 
                          headers=['Case Name', 'Price'], tablefmt='grid', floatfmt='.2f'))
        else:
            print("\n=== All Available Cases ===")
            print(tabulate(cases_df[['name', 'price']].sort_values('name'), 
                          headers=['Case Name', 'Price'], tablefmt='grid', floatfmt='.2f'))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()