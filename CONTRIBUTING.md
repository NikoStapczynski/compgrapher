# Contributing to Compgrapher

First off, thank you for considering contributing to Compgrapher! It's people like you that make Compgrapher such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Quick Start

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/compgrapher.git
   cd compgrapher
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs. what actually happened
- **Environment details** (OS, Python version, etc.)
- **Sample data** if possible (anonymized)
- **Error messages** or logs

Use this template:
```markdown
## Bug Description
A clear description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Compgrapher version: [e.g., 1.0.0]

## Additional Context
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How would you implement it?
- **Alternatives considered**: What other approaches did you consider?

### Your First Contribution

Look for issues labeled:
- `good first issue` - Simple issues for newcomers
- `help wanted` - Issues where we need community help
- `documentation` - Help improve our docs

## Development Setup

### Install Development Dependencies

```bash
pip install -e .[dev]
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `isort` - Import sorter
- `flake8` - Linter
- `mypy` - Type checker
- `pre-commit` - Git hooks

### Set Up Pre-commit Hooks

```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_data_parser.py

# Run tests matching a pattern
pytest -k "test_validation"
```

### Code Formatting

```bash
# Format code
black .

# Sort imports
isort .

# Check style without changing
black --check .
isort --check .
```

### Type Checking

```bash
mypy . --ignore-missing-imports
```

## Style Guidelines

### Python Style

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: 100 characters max
- **Imports**: Use absolute imports, sorted by `isort`
- **Quotes**: Double quotes for strings
- **Docstrings**: Google style

Example:
```python
def calculate_statistics(data: pd.DataFrame, validate: bool = True) -> Dict[str, float]:
    """
    Calculate salary statistics from compensation data.
    
    Args:
        data: DataFrame containing salary information with columns
            'salary_min' and 'salary_max'.
        validate: Whether to validate input data before processing.
    
    Returns:
        Dictionary containing calculated statistics:
            - 'mean': Average salary
            - 'median': Median salary
            - 'min': Minimum salary
            - 'max': Maximum salary
    
    Raises:
        ValueError: If required columns are missing.
        DataValidationError: If validation fails and validate=True.
    
    Example:
        >>> df = pd.DataFrame({'salary_min': [50, 60], 'salary_max': [70, 80]})
        >>> stats = calculate_statistics(df)
        >>> print(stats['mean'])
        65.0
    """
    if validate:
        _validate_data(data)
    
    # Implementation...
```

### File Organization

```
compgrapher/
├── main.py              # Main entry point
├── cli.py               # Command-line interface
├── data_parser.py       # Data loading and parsing
├── graph_generator.py   # Graph generation logic
├── config.yaml          # Default configuration
├── tests/
│   ├── __init__.py
│   ├── test_data_parser.py
│   ├── test_graph_generator.py
│   └── conftest.py      # Shared fixtures
├── input/               # Sample input data
├── output/              # Generated outputs
└── docs/                # Documentation
```

### Testing Guidelines

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Include edge cases and error conditions

```python
class TestDataValidation:
    """Tests for data validation functionality."""
    
    def test_validate_accepts_valid_data(self, sample_data):
        """Valid data should pass validation without warnings."""
        warnings = validate_data(sample_data)
        assert len(warnings) == 0
    
    def test_validate_catches_negative_salary(self):
        """Negative salary values should generate warnings."""
        invalid_data = {'Position A': {'Employer': (-100, 50)}}
        warnings = validate_data(invalid_data)
        assert any("negative" in w.lower() for w in warnings)
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

```
feat(graph): add support for percentile markers

Add optional 25th, 50th, and 75th percentile lines to graphs.
Enable with --show-percentiles flag.

Closes #42
```

```
fix(parser): handle empty cells in CSV files

Previously, empty cells caused ValueError. Now they are
treated as missing data and logged as warnings.
```

## Pull Request Process

### Before Submitting

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Run the full test suite** and ensure it passes
4. **Update the README** if needed
5. **Add a changelog entry** if applicable

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
```

### Review Process

1. Submit your PR against the `develop` branch (or `main` if no develop branch)
2. Fill out the PR template completely
3. Wait for CI checks to pass
4. Address reviewer feedback
5. Once approved, a maintainer will merge

### After Your PR is Merged

- Delete your branch
- Update your local repository:
  ```bash
  git checkout main
  git pull upstream main
  git branch -d your-branch-name
  ```

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to Compgrapher! 🎉
