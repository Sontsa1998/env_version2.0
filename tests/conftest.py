"""
Pytest configuration and shared fixtures for tests.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_csv_data():
    """Provide sample CSV data for testing."""
    return {
        "student_id": [1, 2, 3, 4, 5],
        "age": [20, 21, 19, 22, 20],
        "gender": ["Male", "Female", "Male", "Female", "Male"],
        "study_hours_per_day": [5.0, 6.0, 4.0, 7.0, 5.5],
        "exam_score": [75.0, 85.0, 70.0, 90.0, 78.0]
    }
