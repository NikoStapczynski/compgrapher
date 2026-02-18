"""
conftest.py - Pytest configuration and shared fixtures for Compgrapher tests.

Placing pytest configuration here (rather than inside test files) ensures
the markers and settings apply to the whole test suite regardless of which
file is collected first.
"""


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow-running (deselect with '-m \"not slow\"')",
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests",
    )
