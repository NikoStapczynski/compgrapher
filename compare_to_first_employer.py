#!/usr/bin/env python3
"""
Generic First Employer Comparison Visualization Script
Creates visualizations comparing the first employer in CSV to other employers
"""

import csv
import matplotlib.pyplot as plt
import os
import re
import numpy as np
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

def load_comparison_data(csv_file):
    """Load salary data for all employers dynamically"""
    position_data = {}
    town_colors = {}

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Get header row

        # Find all employer columns (skip first column which is position titles)
        # Skip the last few columns that are metadata (ERI, Comp Data Points, 60th Percentile)
        employer_headers = headers[1:-3] if len(headers) > 3 else headers[1:]

        # Create town indices for all employers
        town_indices = {}
        for i, header in enumerate(employer_headers):
            clean_header = header.strip()
            town_indices[clean_header] = i + 1  # +1 because headers[0] is position

        # Assign colors to each employer
        colors = plt.cm.tab20.colors  # Use a color map with distinct colors
        for i, employer in enumerate(employer_headers):
            clean_employer = employer.strip()
            town_colors[clean_employer] = colors[i % len(colors)]

        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue  # Skip empty rows

            position = row[0].strip()

            # Skip inspector positions as requested
            if position in ['Alternate Building Inspector', 'Alternate Gas/Plumbing Inspector', 'Alternate Wire Inspector']:
                continue

            position_data[position] = {}

            # Extract data for each employer
            for employer, col_idx in town_indices.items():
                salary_value = clean_salary_value(row[col_idx])
                if salary_value is not None:
                    position_data[position][employer] = salary_value

    return position_data, town_colors

def filter_highest_paid_positions(position_data):
    """Filter out the 2 highest paid positions from the dataset"""
    # Calculate average salary for each position across all towns
    position_averages = []
    for position, town_salaries in position_data.items():
        if town_salaries:  # Only consider positions with data
            avg_salary = sum(town_salaries.values()) / len(town_salaries)
            position_averages.append((position, avg_salary))

    # Sort by average salary and exclude top 2
    position_averages.sort(key=lambda x: x[1], reverse=True)
    positions_to_exclude = [pos[0] for pos in position_averages[:2]] if len(position_averages) >= 2 else []

    # Filter the data
    filtered_data = {pos: data for pos, data in position_data.items()
                    if pos not in positions_to_exclude and len(data) > 1}

    return filtered_data

def create_comparison_visualization(position_data, town_colors):
    """Create comparison visualization showing first employer vs other employers"""
    if not position_data:
        print("No valid data to visualize")
        return None

    # Identify the first employer (baseline)
    first_employer = list(town_colors.keys())[0] if town_colors else None
    if not first_employer:
        print("No employers found")
        return None

    # Sort positions by first employer salary (ascending)
    positions = [pos for pos in position_data.keys() if first_employer in position_data[pos]]
    positions.sort(key=lambda pos: position_data[pos].get(first_employer, 0))

    if not positions:
        print(f"No positions with {first_employer} data found")
        return None

    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f'{first_employer.replace(" ", "_").lower()}_comparison_{timestamp}'

    # Create figure with appropriate size
    fig_height = max(12, len(positions) * 0.8)  # Better spacing
    plt.figure(figsize=(20, fig_height))

    # Set up the plot - use integer positions for cleaner separation
    y_positions = list(range(len(positions)))

    # Plot each employer's data as separate bars
    bar_width = 0.8 / len(town_colors)  # Divide space equally
    employer_list = list(town_colors.keys())

    for i, employer in enumerate(employer_list):
        employer_salaries = [position_data[pos].get(employer, 0) for pos in positions]

        # Simple positioning: each employer gets a portion of each position's space
        x_positions = [y + i * bar_width for y in y_positions]

        color = town_colors[employer]
        bars = plt.bar(x_positions, employer_salaries, width=bar_width,
                      label=employer, color=color, alpha=0.8, edgecolor='black', linewidth=0.5)

        # Add value labels on bars (only for non-zero values)
        for j, (bar, salary) in enumerate(zip(bars, employer_salaries)):
            if salary > 0:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                        f'${salary:,.0f}', ha='center', va='bottom', fontsize=7, rotation=90)

    # Customize the plot
    plt.title(f'{first_employer} Salary Comparison with Other Employers', fontsize=16, pad=20, fontweight='bold')
    plt.ylabel('Salary ($)', fontsize=12)
    plt.xlabel('Position', fontsize=12)

    # Set x-ticks and labels with better positioning
    plt.xticks(y_positions, positions, rotation=45, ha='right', fontsize=10)

    # Add horizontal grid lines for salary reference
    plt.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)

    # Add vertical lines to separate position groups
    ax = plt.gca()
    for i in range(len(positions) - 1):
        ax.axvline(x=i + 0.5, color='gray', linewidth=1, alpha=0.5, linestyle='-')

    # Position legend below the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=min(len(employer_list), 4),
              fontsize=10, title_fontsize=12)

    # Adjust layout to accommodate legend
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for legend

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
        print(f'Saved {fmt.upper()} comparison visualization to: {filepath}')

    # Close the plot to free memory
    plt.close()

    # Create detailed HTML report
    html_path = os.path.join('output/html', f'{base_filename}.html')
    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    # Generate comparison table data
    comparison_table = []
    for pos in positions:
        row = [pos]
        for town in town_colors.keys():
            salary = position_data[pos].get(town, '-')
            if isinstance(salary, (int, float)):
                row.append(f'${salary:,.2f}')
            else:
                row.append('-')
        comparison_table.append(row)

    # Generate difference analysis
    difference_analysis = []
    for pos in positions:
        first_employer_salary = position_data[pos].get(first_employer, 0)
        if first_employer_salary > 0:
            for employer in town_colors.keys():
                if employer != first_employer:
                    other_salary = position_data[pos].get(employer, 0)
                    if other_salary > 0:
                        difference = other_salary - first_employer_salary
                        percentage = (difference / first_employer_salary) * 100 if first_employer_salary > 0 else 0
                        difference_analysis.append({
                            'position': pos,
                            'employer': employer,
                            'first_employer': first_employer,
                            'first_employer_salary': first_employer_salary,
                            'other': other_salary,
                            'difference': difference,
                            'percentage': percentage,
                            'employer_color': town_colors.get(employer, '#000000')
                        })

    # Create color mapping for HTML
    town_color_map = {town: f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
                     for town, (r, g, b) in town_colors.items()}

    # Build HTML rows for difference analysis
    difference_rows = []
    for item in difference_analysis:
        pos_class = 'positive' if item["difference"] > 0 else 'negative'
        perc_class = 'positive' if item["percentage"] > 0 else 'negative'

        first_employer_fmt = f"${item['first_employer_salary']:,.2f}"
        other_fmt = f"${item['other']:,.2f}"
        difference_fmt = f"${item['difference']:,.2f}"
        percentage_fmt = f"{item['percentage']:+.1f}%"

        employer_color = town_color_map.get(item["employer"], "#000000")
        row = f'''
        <tr>
            <td>{item["position"]}</td>
            <td style="color: {employer_color}; font-weight: bold;">{item["employer"]}</td>
            <td>{first_employer_fmt}</td>
            <td>{other_fmt}</td>
            <td class="{pos_class}">{difference_fmt}</td>
            <td class="{perc_class}">{percentage_fmt}</td>
        </tr>
        '''
        difference_rows.append(row)

    difference_html = '\n'.join(difference_rows)

    with open(html_path, 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head>
    <title>{first_employer} Salary Comparison</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .info {{ background-color: #e8f4fc; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .highlight {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; }}
        img {{ max-width: 100%; height: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; position: sticky; top: 0; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .positive {{ color: #27ae60; font-weight: bold; }}
        .negative {{ color: #e74c3c; font-weight: bold; }}
        .comparison-grid {{ display: flex; flex-direction: column; gap: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{first_employer} Salary Comparison Analysis</h1>
        <div class="info">
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Data Source:</strong> 202601081638_Dartmouth_MA_FY26__Market_Data_Schedule_E_Employees.csv</p>
            <p><strong>Positions Compared:</strong> {len(positions)}</p>
            <p><strong>Employers Included:</strong> {len(town_colors)}</p>
        </div>

        <div class="highlight">
            <h2>📊 Visual Comparison</h2>
            <p>This chart shows {first_employer} salaries compared to other employers for the same positions.</p>
            <p>Bars are grouped by position, with each employer represented by a different color.</p>
        </div>

        <img src="../png/{base_filename}.png" alt="{first_employer} Salary Comparison Chart">

        <div class="comparison-grid">
            <div>
                <h2>📋 Detailed Salary Comparison</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Position</th>
                            {''.join(f'<th style="color: {town_color_map.get(employer, "#000000")}; font-weight: bold;">{employer}</th>' for employer in town_colors.keys())}
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'<tr><td>{row[0]}</td>{"".join(f"<td>{cell}</td>" for cell in row[1:])}</tr>' for row in comparison_table)}
                    </tbody>
                </table>
            </div>

            <div>
                <h2>💰 Difference Analysis</h2>
                <p>Comparison of {first_employer} salaries vs other employers:</p>
                <table>
                    <thead>
                        <tr>
                            <th>Position</th>
                            <th>Employer</th>
                            <th>{first_employer}</th>
                            <th>Other Employer</th>
                            <th>Difference</th>
                            <th>% Diff</th>
                        </tr>
                    </thead>
                    <tbody>
                        {difference_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="highlight">
            <h2>📈 Key Insights</h2>
            <ul>
                <li><strong>{first_employer} positions analyzed:</strong> {len(positions)}</li>
                <li><strong>Comparison employers:</strong> {', '.join(f'<span style="color: {town_color_map.get(employer, "#000000")}; font-weight: bold;">{employer}</span>' for employer in town_colors.keys())}</li>
                <li><strong>Positions with complete data:</strong> {sum(1 for pos in positions if len(position_data[pos]) == len(town_colors))}</li>
                <li><strong>Analysis includes:</strong> Salary differences and percentage variations</li>
            </ul>
        </div>
    </div>
</body>
</html>''')

    saved_files.append(html_path)
    print(f'Saved HTML comparison report to: {html_path}')

    return saved_files

if __name__ == '__main__':
    # Path to the CSV file
    csv_file = 'input/csv/202601081638_Dartmouth_MA_FY26__Market_Data_Schedule_E_Employees.csv'

    # Load and process comparison data to identify first employer
    position_data, town_colors = load_comparison_data(csv_file)
    first_employer = list(town_colors.keys())[0] if town_colors else "Unknown"

    print(f"{first_employer} Salary Comparison Visualization")
    print("=" * (len(first_employer) + 30))

    # Load and process comparison data
    print(f"Loading comparison data from: {csv_file}")

    original_count = len(position_data)
    print(f"Loaded data for {original_count} positions across {len(town_colors)} employers")

    # Filter out highest paid positions
    filtered_data = filter_highest_paid_positions(position_data)
    filtered_count = len(filtered_data)
    print(f"Filtered to {filtered_count} positions after excluding top 2 highest paid")

    if filtered_data:
        # Create comparison visualizations
        print("\nCreating comparison visualizations...")
        output_files = create_comparison_visualization(filtered_data, town_colors)

        if output_files:
            print(f"\nComparison visualization complete! Created {len(output_files)} output files:")
            for file in output_files:
                print(f"  - {file}")

            print(f"\nMain comparison report: {output_files[-1]}")
            print("\nKey insights:")
            print(f"- {first_employer} salaries shown alongside comparable employer salaries")
            print("- Color-coded bars for easy employer identification")
            print("- Detailed HTML report with difference analysis")
            print("- Interactive tables showing exact salary comparisons")
        else:
            print("No comparison visualizations were created")
    else:
        print("No valid data for comparison after filtering")
