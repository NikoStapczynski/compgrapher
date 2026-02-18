"""
test_data_parser.py - Unit tests for the data parser module

This module provides comprehensive tests for data loading, cleaning,
parsing, and validation functionality.
"""
import os
import tempfile
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import pytest

from data_parser import CompensationDataParser, DataValidationError


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_csv_data():
    """Create sample CSV data for testing."""
    return """POSITION TITLE,Employer A,Employer B,Employer C
Software Engineer,100,95,105
,80,75,85
Data Scientist,120,110,115
,90,85,95
Project Manager,90,85,95
,70,65,75
"""


@pytest.fixture
def sample_csv_file(sample_csv_data, tmp_path):
    """Create a temporary CSV file with sample data."""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(sample_csv_data)
    return str(csv_file)


@pytest.fixture
def malformed_csv_data():
    """Create malformed CSV data for error testing."""
    return """POSITION TITLE,Employer A,Employer B
Software Engineer,invalid,95
,80,75
"""


@pytest.fixture
def malformed_csv_file(malformed_csv_data, tmp_path):
    """Create a temporary malformed CSV file."""
    csv_file = tmp_path / "malformed_data.csv"
    csv_file.write_text(malformed_csv_data)
    return str(csv_file)


@pytest.fixture
def empty_csv_file(tmp_path):
    """Create an empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("POSITION TITLE,Employer A\n")
    return str(csv_file)


@pytest.fixture
def sample_compensation_data():
    """Sample parsed compensation data for validation tests."""
    return {
        'Software Engineer': {
            'Employer A': (80.0, 100.0),
            'Employer B': (75.0, 95.0),
            'Employer C': (85.0, 105.0),
        },
        'Data Scientist': {
            'Employer A': (90.0, 120.0),
            'Employer B': (85.0, 110.0),
        }
    }


# ============================================================================
# Initialization Tests
# ============================================================================

class TestParserInitialization:
    """Tests for parser initialization."""
    
    def test_init_with_valid_csv(self, sample_csv_file):
        """Test initialization with a valid CSV file."""
        parser = CompensationDataParser(sample_csv_file)
        assert parser.filepath.exists()
        assert parser.filepath.suffix == '.csv'
    
    def test_init_with_nonexistent_file(self):
        """Test that FileNotFoundError is raised for missing files."""
        with pytest.raises(FileNotFoundError):
            CompensationDataParser("/nonexistent/path/file.csv")
    
    def test_init_with_unsupported_format(self, tmp_path):
        """Test that ValueError is raised for unsupported formats."""
        txt_file = tmp_path / "data.txt"
        txt_file.write_text("some data")
        
        with pytest.raises(ValueError) as exc_info:
            CompensationDataParser(str(txt_file))
        
        assert "Unsupported file format" in str(exc_info.value)
    
    def test_supported_formats(self):
        """Test that all expected formats are supported."""
        expected_formats = {'.csv', '.xls', '.xlsx', '.ods'}
        assert CompensationDataParser.SUPPORTED_FORMATS == expected_formats


# ============================================================================
# Data Loading Tests
# ============================================================================

class TestDataLoading:
    """Tests for data loading functionality."""
    
    def test_load_csv_data(self, sample_csv_file):
        """Test loading data from CSV file."""
        parser = CompensationDataParser(sample_csv_file)
        df = parser.load_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 6  # 6 rows in sample data
        assert 'POSITION TITLE' in df.columns
    
    def test_load_empty_file(self, empty_csv_file):
        """Test loading an empty CSV file."""
        parser = CompensationDataParser(empty_csv_file)
        df = parser.load_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


# ============================================================================
# Data Cleaning Tests
# ============================================================================

class TestDataCleaning:
    """Tests for data cleaning functionality."""
    
    def test_clean_removes_bad_columns(self, tmp_path):
        """Test that summary columns are removed during cleaning."""
        csv_content = """POSITION TITLE,Employer A,Comp Average,Comp Data Points
Software Engineer,100,97.5,3
,80,,
"""
        csv_file = tmp_path / "with_summary.csv"
        csv_file.write_text(csv_content)
        
        parser = CompensationDataParser(str(csv_file))
        df = parser.load_data()
        cleaned_df = parser.clean_data(df)
        
        assert 'Comp Average' not in cleaned_df.columns
        assert 'Comp Data Points' not in cleaned_df.columns
        assert 'Employer A' in cleaned_df.columns
    
    def test_clean_removes_nan_titles(self, sample_csv_file):
        """Test that rows with NaN titles are removed."""
        parser = CompensationDataParser(sample_csv_file)
        df = parser.load_data()
        cleaned_df = parser.clean_data(df)
        
        # After cleaning, all rows should have valid titles
        # Note: Empty strings are different from NaN
        assert cleaned_df['POSITION TITLE'].notna().all()


# ============================================================================
# Data Parsing Tests
# ============================================================================

class TestDataParsing:
    """Tests for compensation data parsing."""
    
    def test_parse_compensation_data(self, sample_csv_file):
        """Test parsing compensation data into structured format."""
        parser = CompensationDataParser(sample_csv_file)
        df = parser.load_data()
        cleaned_df = parser.clean_data(df)
        comp_data = parser.parse_compensation_data(cleaned_df)
        
        assert isinstance(comp_data, dict)
        assert 'Software Engineer' in comp_data
        assert 'Data Scientist' in comp_data
    
    def test_parsed_data_structure(self, sample_csv_file):
        """Test the structure of parsed compensation data."""
        parser = CompensationDataParser(sample_csv_file)
        df = parser.load_data()
        cleaned_df = parser.clean_data(df)
        comp_data = parser.parse_compensation_data(cleaned_df)
        
        for position, employers in comp_data.items():
            assert isinstance(employers, dict)
            for employer, salary_range in employers.items():
                assert isinstance(salary_range, tuple)
                assert len(salary_range) == 2
                low, high = salary_range
                assert isinstance(low, float)
                assert isinstance(high, float)


# ============================================================================
# Validation Tests
# ============================================================================

class TestDataValidation:
    """Tests for data validation functionality."""
    
    def test_validate_valid_data(self, sample_compensation_data):
        """Test validation passes for valid data."""
        # validate_data is a @staticmethod — no instance needed.
        warnings = CompensationDataParser.validate_data(sample_compensation_data)

        # Valid data should have no warnings
        assert len(warnings) == 0

    def test_validate_low_exceeds_high(self):
        """Test validation catches when low > high."""
        invalid_data = {
            'Position A': {
                'Employer A': (100.0, 80.0),  # Invalid: low > high
            }
        }

        warnings = CompensationDataParser.validate_data(invalid_data)

        assert len(warnings) > 0
        assert any("Low value" in w and "exceeds high value" in w for w in warnings)

    def test_validate_negative_values(self):
        """Test validation catches negative salary values."""
        invalid_data = {
            'Position A': {
                'Employer A': (-10.0, 80.0),  # Invalid: negative value
            }
        }

        warnings = CompensationDataParser.validate_data(invalid_data)

        assert len(warnings) > 0
        assert any("Negative compensation" in w for w in warnings)

    def test_validate_empty_position(self):
        """Test validation catches positions with no data."""
        invalid_data = {
            'Position A': {},  # Empty
        }

        warnings = CompensationDataParser.validate_data(invalid_data)

        assert len(warnings) > 0
        assert any("no compensation data" in w for w in warnings)


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for full processing pipeline."""
    
    def test_full_process_pipeline(self, sample_csv_file):
        """Test the complete processing pipeline."""
        parser = CompensationDataParser(sample_csv_file)
        comp_data, warnings = parser.process(validate=True)
        
        assert isinstance(comp_data, dict)
        assert len(comp_data) > 0
        assert isinstance(warnings, list)
    
    def test_process_without_validation(self, sample_csv_file):
        """Test processing without validation."""
        parser = CompensationDataParser(sample_csv_file)
        comp_data, warnings = parser.process(validate=False)
        
        assert isinstance(comp_data, dict)
        assert warnings == []


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_single_position(self, tmp_path):
        """Test parsing with only one position."""
        csv_content = """POSITION TITLE,Employer A,Employer B
Single Position,100,95
,80,75
"""
        csv_file = tmp_path / "single_position.csv"
        csv_file.write_text(csv_content)
        
        parser = CompensationDataParser(str(csv_file))
        comp_data, _ = parser.process()
        
        assert len(comp_data) == 1
        assert 'Single Position' in comp_data
    
    def test_single_employer(self, tmp_path):
        """Test parsing with only one employer."""
        csv_content = """POSITION TITLE,Employer A
Position A,100
,80
Position B,120
,90
"""
        csv_file = tmp_path / "single_employer.csv"
        csv_file.write_text(csv_content)
        
        parser = CompensationDataParser(str(csv_file))
        comp_data, _ = parser.process()
        
        for position in comp_data.values():
            assert len(position) == 1
    
    def test_missing_salary_data(self, tmp_path):
        """Test handling of missing salary data."""
        csv_content = """POSITION TITLE,Employer A,Employer B
Position A,100,
,80,
"""
        csv_file = tmp_path / "missing_data.csv"
        csv_file.write_text(csv_content)
        
        parser = CompensationDataParser(str(csv_file))
        comp_data, _ = parser.process()
        
        # Employer B should be excluded due to missing data
        if 'Position A' in comp_data:
            assert 'Employer B' not in comp_data['Position A']


# ============================================================================
# Performance Tests (Optional)
# ============================================================================

@pytest.mark.slow
class TestPerformance:
    """Performance tests for large datasets."""
    
    def test_large_dataset(self, tmp_path):
        """Test parsing a large dataset."""
        # Generate large CSV
        rows = []
        rows.append("POSITION TITLE," + ",".join([f"Employer {i}" for i in range(50)]))
        
        for pos_num in range(100):
            # High row
            high_values = ",".join([str(100 + pos_num) for _ in range(50)])
            rows.append(f"Position {pos_num},{high_values}")
            # Low row
            low_values = ",".join([str(80 + pos_num) for _ in range(50)])
            rows.append(f",{low_values}")
        
        csv_file = tmp_path / "large_data.csv"
        csv_file.write_text("\n".join(rows))
        
        parser = CompensationDataParser(str(csv_file))
        comp_data, _ = parser.process()
        
        assert len(comp_data) == 100


# ============================================================================
# CLI Tests
# ============================================================================

class TestCLI:
    """Tests for CLI module if available."""
    
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        try:
            from cli import create_parser, __version__
            assert __version__ is not None
        except ImportError:
            pytest.skip("CLI module not available")
    
    def test_cli_parser_creation(self):
        """Test CLI parser can be created."""
        try:
            from cli import create_parser
            parser = create_parser()
            assert parser is not None
        except ImportError:
            pytest.skip("CLI module not available")
    
    def test_cli_help(self):
        """Test CLI help message."""
        try:
            from cli import create_parser
            parser = create_parser()
            # This should not raise an exception
            help_text = parser.format_help()
            assert 'compgrapher' in help_text
        except ImportError:
            pytest.skip("CLI module not available")


# ============================================================================
# Graph Generator Tests
# ============================================================================

class TestGraphGenerator:
    """Tests for graph generator module if available."""
    
    def test_graph_generator_import(self):
        """Test that graph generator module can be imported."""
        try:
            from graph_generator import GraphGenerator, GraphConfig
            assert GraphConfig is not None
            assert GraphGenerator is not None
        except ImportError:
            pytest.skip("Graph generator module not available")
    
    def test_graph_config_defaults(self):
        """Test GraphConfig default values."""
        try:
            from graph_generator import GraphConfig
            config = GraphConfig()
            assert config.show_grid is True
            assert config.dpi == 100
            assert config.output_dir == 'output'
        except ImportError:
            pytest.skip("Graph generator module not available")
    
    def test_graph_generator_initialization(self):
        """Test GraphGenerator initialization."""
        try:
            from graph_generator import GraphGenerator, GraphConfig
            config = GraphConfig(show_labels=True)
            generator = GraphGenerator(config)
            assert generator.config.show_labels is True
        except ImportError:
            pytest.skip("Graph generator module not available")


# pytest markers are registered in tests/conftest.py.
