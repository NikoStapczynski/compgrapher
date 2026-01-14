#!/usr/bin/env python3
"""
Visualization script for Dartmouth CSV data
Creates a bar chart showing Dartmouth salaries by position
"""

import csv
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime

def clean_salary_value(value):
    """Clean and convert salary values to numeric format"""
    if not value or value.strip() == '':
        return None

    # Remove dollar signs and commas
    clean_val = value.strip().replace('$', '').replace(',', '')

    # Handle "per inspection" or similar text
    if 'per' in clean_val.lower():
        # Extract just the numeric part
        match = re.search(r'(\d+\.?\d*)', clean_val)
        if match:
            return float(match.group(1))
        return None

    try:
        return float(clean_val)
    except ValueError:
        return None

def load_dartmouth_data(csv_file):
    """Load Dartmouth salary data from CSV file"""
    data = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row

        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue  # Skip empty rows

            position = row[0].strip()
            dartmouth_salary = clean_salary_value(row[1])

            if dartmouth_salary is not None:
                data.append({
                    'position': position,
                    'salary': dartmouth_salary
                })

    return data

def filter_data_for_visualization(data):
    """Filter data to exclude inspector positions and highest paid positions"""
    # Define positions to exclude
    inspector_positions = [
        'Alternate Building Inspector',
        'Alternate Gas/Plumbing Inspector',
        'Alternate Wire Inspector'
    ]

    # Filter out inspector positions
    filtered_data = [item for item in data if item['position'] not in inspector_positions]

    # Sort by salary to identify highest paid positions
    filtered_data.sort(key=lambda x: x['salary'], reverse=True)

    # Remove the 2 highest paid positions
    if len(filtered_data) > 2:
        filtered_data = filtered_data[2:]

    # Sort by salary for visualization (ascending order)
    filtered_data.sort(key=lambda x: x['salary'])

    return filtered_data

def create_visualization(data, output_dir='output'):
    """Create visualization of Dartmouth salary data"""
    if not data:
        print("No valid data to visualize")
        return

    # Sort data by salary for better visualization
    data.sort(key=lambda x: x['salary'])

    # Extract data for plotting
    positions = [item['position'] for item in data]
    salaries = [item['salary'] for item in data]

    # Create figure with larger size to accommodate many positions
    plt.figure(figsize=(15, 10))

    # Create horizontal bar chart (better for many categories)
    bars = plt.barh(range(len(positions)), salaries, color='skyblue')

    # Customize the plot
    plt.title('Dartmouth Salary Data by Position', fontsize=16, pad=20)
    plt.xlabel('Salary ($)', fontsize=12)
    plt.ylabel('Position', fontsize=12)

    # Set y-ticks and labels
    plt.yticks(range(len(positions)), positions, fontsize=8)
    plt.xticks(fontsize=10)

    # Add value labels on each bar
    for i, (bar, salary) in enumerate(zip(bars, salaries)):
        plt.text(salary, i, f'${salary:,.2f}',
                 va='center', fontsize=8)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f'dartmouth_salaries_{timestamp}'

    # Save in multiple formats
    formats = [
        ('png', 'output/png'),
        ('jpg', 'output/jpg'),
        ('svg', 'output/svg')
    ]

    saved_files = []

    for fmt, output_path in formats:
        os.makedirs(output_path, exist_ok=True)
        filepath = os.path.join(output_path, f'{base_filename}.{fmt}')
        plt.savefig(filepath, format=fmt, dpi=300, bbox_inches='tight')
        saved_files.append(filepath)
        print(f'Saved {fmt.upper()} visualization to: {filepath}')

    # Also create HTML version
    html_path = os.path.join('output/html', f'{base_filename}.html')
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    with open(html_path, 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>Dartmouth Salary Visualization</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .info {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        img {{ max-width: 100%; height: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Dartmouth Salary Data Visualization</h1>
    <div class="info">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Data source:</strong> {os.path.basename(csv_file)}</p>
        <p><strong>Positions analyzed:</strong> {len(data)}</p>
        <p><strong>Salary range:</strong> ${min(salaries):,.2f} - ${max(salaries):,.2f}</p>
    </div>

    <h2>Salary Distribution by Position</h2>
    <img src="../png/{base_filename}.png" alt="Dartmouth Salary Chart">

    <h2>Salary Data Table</h2>
    <table>
        <thead>
            <tr>
                <th>Position</th>
                <th>Salary ($)</th>
            </tr>
        </thead>
        <tbody>
            {''.join(f'<tr><td>{item["position"]}</td><td>${item["salary"]:,.2f}</td></tr>' for item in data)}
        </tbody>
    </table>
</body>
</html>''')

    saved_files.append(html_path)
    print(f'Saved HTML visualization to: {html_path}')

    return saved_files

if __name__ == '__main__':
    print("Dartmouth Salary Data Visualization")
    print("=" * 40)

    # Path to the Dartmouth CSV file
    csv_file = 'input/csv/202601081638_Dartmouth_MA_FY26__Market_Data_Schedule_E_Employees.csv'

    # Load and process data
    print(f"Loading data from: {csv_file}")
    dartmouth_data = load_dartmouth_data(csv_file)
    print(f"Loaded {len(dartmouth_data)} valid salary records")

    if dartmouth_data:
        # Filter data to exclude inspector positions and highest paid positions
        filtered_data = filter_data_for_visualization(dartmouth_data)
        excluded_count = len(dartmouth_data) - len(filtered_data)
        print(f"Filtered data: {len(filtered_data)} positions after excluding {excluded_count} positions")

        # Create visualizations with filtered data
        print("\nCreating visualizations...")
        output_files = create_visualization(filtered_data)

        print(f"\nVisualization complete! Created {len(output_files)} output files:")
        for file in output_files:
            print(f"  - {file}")

        print("\nYou can view the results in:")
        print("  - HTML: output/html/ directory")
        print("  - Images: output/png/, output/jpg/, output/svg/ directories")
    else:
        print("No valid salary data found to visualize")
