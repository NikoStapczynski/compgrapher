# Compgrapher

[![CI](https://github.com/NikoStapczynski/compgrapher/actions/workflows/ci.yml/badge.svg)](https://github.com/NikoStapczynski/compgrapher/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Compgrapher is a powerful tool that generates floating bar graphs from compensation market data to facilitate employer comparisons. Perfect for HR professionals, compensation analysts, and business leaders who need to visualize and compare salary data across multiple employers.

## 📸 Example Output

<img src="output/svg/Example%20Software%20Engineer.svg" width="60%" alt="Example Software Engineer Compensation">

<img src="output/svg/Example%20Data%20Scientist.svg" width="60%" alt="Example Data Scientist Compensation">

## ✨ Features

- **Multiple Input Formats**: Supports CSV, XLS, XLSX, and ODS files
- **Multiple Output Formats**: Generate HTML reports, PDF, PNG, SVG, JPG, WEBP, and EPS
- **Interactive HTML Reports**: Beautiful, responsive reports with embedded charts and statistics
- **Data Validation**: Automatic detection of data quality issues
- **Configurable**: YAML configuration file for default settings
- **Statistics**: Calculate min, max, median, and mean compensation values
- **Extensible**: Modular architecture for easy customization

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NikoStapczynski/compgrapher.git
cd compgrapher

# Set up virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate PNG graphs from sample data
python main.py --input input/csv/example_table.csv --output png

# Generate HTML report with charts
python main.py --input your_data.csv --output html png

# Specify the client to highlight
python main.py --client "Your Company" --input data.csv --output html pdf png
```

## 📖 Documentation

### Input Data Format

The data file (CSV, XLS, XLSX, or ODS) should have a 'POSITION TITLE' column and columns for each employer with salary data. The data alternates between high and low salary ranges on consecutive rows for each position.

Example structure:

| Row | POSITION TITLE | Employer A | Employer B | Employer C |
|-----|----------------|------------|------------|------------|
| 1   | Software Engineer | 100 | 95 | 105 |
| 2   |                | 80 | 75 | 85 |
| 3   | Data Scientist | 120 | 110 | 115 |
| 4   |                | 90 | 85 | 95 |

- Odd rows: High salary values
- Even rows: Low salary values

### Command Line Options

```
python main.py [OPTIONS]

Options:
  --client NAME       Name of the employer to highlight (default: first in data)
  --input FILE        Path to data file (.csv, .xls, .xlsx, .ods)
  --output FORMAT(s)  Output format(s): html, pdf, png, svg, jpg, jpeg, webp, eps
  --validate          Run data validation checks
  --config FILE       Path to YAML configuration file
  -v, --verbose       Enable verbose output
  -q, --quiet         Suppress output except errors
  -V, --version       Show version information
```

### Output Formats

| Format | Description |
|--------|-------------|
| `html` | Interactive HTML report with embedded charts and statistics |
| `png`  | High-quality raster images |
| `svg`  | Scalable vector graphics (ideal for documents) |
| `pdf`  | Print-ready PDF files |
| `jpg`/`jpeg` | JPEG images |
| `webp` | Modern web-optimized format |
| `eps`  | Encapsulated PostScript (for publishing) |

### Configuration File

Create a `config.yaml` file to set default options:

```yaml
defaults:
  input: input/csv/my_data.csv
  output:
    - png
    - html
  validate: true

graph:
  colors:
    client: '#4CAF50'
    default: '#FFFFFF'
  display:
    show_grid: true
    show_labels: false
```

Use with: `python main.py --config config.yaml`

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html
```

## 📁 Project Structure

```
compgrapher/
├── main.py              # Main entry point
├── cli.py               # Enhanced command-line interface
├── data_parser.py       # Data loading and validation
├── graph_generator.py   # Graph generation with statistics
├── config.yaml          # Default configuration
├── pyproject.toml       # Modern Python packaging
├── requirements.txt     # Dependencies
├── tests/               # Unit tests
│   ├── __init__.py
│   └── test_data_parser.py
├── .github/
│   └── workflows/
│       └── ci.yml       # CI/CD pipeline
├── input/               # Input data files
│   ├── csv/
│   ├── ods/
│   └── xls/
└── output/              # Generated outputs
    ├── html/
    ├── png/
    ├── svg/
    └── pdf/
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Install with development dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run linting
black .
isort .
flake8 .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_data_parser.py
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Roadmap

- [ ] JSON input support
- [ ] Percentile markers (25th, 50th, 75th)
- [ ] Sort employers by median compensation
- [ ] Direct API integration with compensation data providers
- [ ] Batch processing with progress bars
- [ ] Dark mode for HTML reports

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/)
- Inspired by the need for better compensation data visualization

---

**Made with ❤️ by [NikoStapczynski](https://github.com/NikoStapczynski)**
