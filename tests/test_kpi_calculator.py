"""
Unit tests for kpi_calculator module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_manager import DatabaseManager
from kpi_calculator import KPICalculator


class TestKPICalculator:
    """Tests for KPICalculator class."""
    
    @pytest.fixture
    def db_manager(self):
        """Create an in-memory database manager with sample data."""
        db = DatabaseManager(":memory:")
        df = pd.DataFrame({
            "student_id": [1, 2, 3, 4, 5],
            "gender": ["Male", "Female", "Male", "Female", "Male"],
            "age": [25, 30, 35, 28, 32],
            "study_hours_per_day": [5.0, 6.0, 4.0, 7.0, 5.5],
            "attendance_percentage": [85.0, 90.0, 75.0, 95.0, 80.0],
            "sleep_hours": [7.0, 8.0, 6.0, 8.5, 7.5],
            "exam_score": [85.0, 90.0, 78.0, 92.0, 88.0]
        })
        db.import_data(df, "student_habits_performance")
        return db
    
    @pytest.fixture
    def kpi_calculator(self, db_manager):
        """Create a KPICalculator instance."""
        return KPICalculator(db_manager)
    
    def test_calculate_kpi_1_scores_by_group(self, kpi_calculator):
        """Test calculating average scores by group."""
        result = kpi_calculator.calculate_kpi_1_scores_by_group()
        assert not result.empty
        assert "group" in result.columns
        assert "average_score" in result.columns
        assert "count" in result.columns
    
    def test_calculate_kpi_2_study_correlation(self, kpi_calculator):
        """Test calculating study hours correlation."""
        result = kpi_calculator.calculate_kpi_2_study_correlation()
        assert not result.empty
        assert "study_hours" in result.columns
        assert "exam_score" in result.columns
    
    def test_calculate_kpi_3_attendance_impact(self, kpi_calculator):
        """Test calculating attendance impact."""
        result = kpi_calculator.calculate_kpi_3_attendance_impact()
        assert not result.empty
        assert "attendance_range" in result.columns
        assert "average_score" in result.columns
    
    def test_calculate_kpi_4_sleep_performance(self, kpi_calculator):
        """Test calculating sleep performance relationship."""
        result = kpi_calculator.calculate_kpi_4_sleep_performance()
        assert not result.empty
        assert "sleep_hours" in result.columns
        assert "exam_score" in result.columns
    
    def test_calculate_correlation_coefficient(self, kpi_calculator):
        """Test calculating Pearson correlation coefficient."""
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([2, 4, 6, 8, 10])
        corr = kpi_calculator.calculate_correlation_coefficient(x, y)
        assert corr == pytest.approx(1.0, abs=0.01)  # Perfect positive correlation
    
    def test_calculate_correlation_coefficient_negative(self, kpi_calculator):
        """Test calculating negative correlation."""
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([10, 8, 6, 4, 2])
        corr = kpi_calculator.calculate_correlation_coefficient(x, y)
        assert corr == pytest.approx(-1.0, abs=0.01)  # Perfect negative correlation
    
    def test_calculate_correlation_coefficient_insufficient_data(self, kpi_calculator):
        """Test correlation with insufficient data."""
        x = pd.Series([1])
        y = pd.Series([2])
        corr = kpi_calculator.calculate_correlation_coefficient(x, y)
        assert corr == 0.0
    
    def test_update_filters(self, kpi_calculator):
        """Test updating filters."""
        filters = {"gender": "Male"}
        kpi_calculator.update_filters(filters)
        assert kpi_calculator.filters == filters
    
    def test_kpi_calculator_with_filters(self, db_manager):
        """Test KPI calculator with active filters."""
        filters = {"gender": "Male"}
        kpi_calc = KPICalculator(db_manager, filters)
        assert kpi_calc.filters == filters
