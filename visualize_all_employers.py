#!/usr/bin/env python3
"""
Multi-Employer Visualization Script
Creates individual visualizations for each employer in the CSV data
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

def load_all_employer_data(csv_file):
    """Load salary data for all employers from CSV file"""
    employers = []
    data_by_employer = {}

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Get header row

        # Extract employer names from headers (skip first column and last few metadata columns)
        employers = headers[2:18]  # Columns 3-18 are the employer columns

        # Initialize data structure
        for employer in employers:
            data_by_employer[employer.strip()] = []

        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue  # Skip empty rows

            position = row[0].strip()

            # Process each employer column (columns 2-17, indices 2-17)
            for i, employer in enumerate(employers):
                salary_value = clean_salary_value(row[i + 2])  # +2 because row[0] is position, row[1] is Dartmouth
                if salary_value is not None:
                    data_by_employer[employer.strip()].append({
                        'position': position,
                        'salary': salary_value
                    })

    return data_by_employer

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

def create_employer_visualization(employer_data, employer_name, output_dir='output'):
    """Create visualization for a single employer"""
    if not employer_data:
        print(f"No valid data for {employer_name}")
        return None

    # Filter data to exclude inspector positions and highest paid positions
    filtered_data = filter_data_for_visualization(employer_data)

    if not filtered_data:
        print(f"No valid data for {employer_name} after filtering")
        return None

    # Extract data for plotting
    positions = [item['position'] for item in filtered_data]
    salaries = [item['salary'] for item in filtered_data]

    # Create figure with appropriate size
    fig_height = max(8, len(positions) * 0.3)  # Dynamic height based on number of positions
    plt.figure(figsize=(12, fig_height))

    # Create horizontal bar chart
    bars = plt.barh(range(len(positions)), salaries, color='skyblue')

    # Customize the plot
    plt.title(f'{employer_name} Salary Data by Position', fontsize=16, pad=20)
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

    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f'{employer_name.replace(" ", "_")}_salaries_{timestamp}'

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

    # Close the plot to free memory
    plt.close()

    # Also create HTML version
    html_path = os.path.join('output/html', f'{base_filename}.html')
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    with open(html_path, 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>{employer_name} Salary Visualization</title>
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
    <h1>{employer_name} Salary Data Visualization</h1>
    <div class="info">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Employer:</strong> {employer_name}</p>
        <p><strong>Positions analyzed:</strong> {len(filtered_data)}</p>
        <p><strong>Salary range:</strong> ${min(salaries):,.2f} - ${max(salaries):,.2f}</p>
    </div>

    <h2>Salary Distribution by Position</h2>
    <img src="../png/{base_filename}.png" alt="{employer_name} Salary Chart">

    <h2>Salary Data Table</h2>
    <table>
        <thead>
            <tr>
                <th>Position</th>
                <th>Salary ($)</th>
            </tr>
        </thead>
        <tbody>
            {''.join(f'<tr><td>{item["position"]}</td><td>${item["salary"]:,.2f}</td></tr>' for item in filtered_data)}
        </tbody>
    </table>
</body>
</html>''')

    saved_files.append(html_path)
    return saved_files

def create_summary_index(employers, timestamp):
    """Create an HTML index page linking to all employer visualizations"""
    index_path = f'output/html/employers_index_{timestamp}.html'
    os.makedirs(os.path.dirname(index_path), exist_ok=True)

    # Generate employer cards
    employer_cards = []
    for employer in sorted(employers):
        employer_filename = employer.replace(" ", "_")
        employer_cards.append(f'''
            <div class="employer-card">
                <h3>{employer}</h3>
                <p>Click to view salary visualization</p>
                <a href="{employer_filename}_salaries_{timestamp}.html" class="btn">View {employer}</a>
            </div>
        ''')

    employers_html = '\n'.join(employer_cards)

    with open(index_path, 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>Multi-Employer Salary Visualizations</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .employer-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .employer-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 5px; background-color: #f9f9f9; }}
        .employer-card h3 {{ margin-top: 0; color: #2c3e50; }}
        .employer-card p {{ margin-bottom: 10px; }}
        .btn {{ display: inline-block; padding: 8px 15px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
        .btn:hover {{ background-color: #2980b9; }}
        .info {{ background-color: #e8f4fc; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-Employer Salary Visualizations</h1>
        <div class="info">
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Employers:</strong> {len(employers)}</p>
            <p><strong>Data Source:</strong> 202601081638_Dartmouth_MA_FY26__Market_Data_Schedule_E_Employees.csv</p>
        </div>

        <h2>Employer Visualizations</h2>
        <div class="employer-grid">
            {employers_html}
        </div>
    </div>
</body>
</html>''')

    return index_path

if __name__ == '__main__':
    print("Multi-Employer Salary Data Visualization")
    print("=" * 50)

    # Path to the CSV file
    csv_file = 'input/csv/202601081638_Dartmouth_MA_FY26__Market_Data_Schedule_E_Employees.csv'

    # Load and process data for all employers
    print(f"Loading data from: {csv_file}")
    employer_data = load_all_employer_data(csv_file)

    print(f"Found data for {len(employer_data)} employers:")
    for employer, data in employer_data.items():
        print(f"  - {employer}: {len(data)} salary records")

    # Generate visualizations for each employer
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    all_output_files = []

    print(f"\nCreating visualizations for each employer...")
    for employer, data in employer_data.items():
        if data:  # Only process employers with data
            print(f"Processing {employer}...")
            output_files = create_employer_visualization(data, employer)
            if output_files:
                all_output_files.extend(output_files)

    # Create summary index page
    if employer_data:
        index_path = create_summary_index(employer_data.keys(), timestamp)
        all_output_files.append(index_path)
        print(f"\nCreated summary index: {index_path}")

    print(f"\nVisualization complete! Created {len(all_output_files)} output files:")
    for file in all_output_files:
        print(f"  - {file}")

    print(f"\nMain summary page: {index_path}")
    print("\nYou can view all results in:")
    print("  - HTML: output/html/ directory")
    print("  - Images: output/png/, output/jpg/, output/svg/ directories")
