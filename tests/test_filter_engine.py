"""
Unit tests for filter_engine module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_manager import DatabaseManager
from filter_engine import FilterEngine


class TestFilterEngine:
    """Tests for FilterEngine class."""
    
    @pytest.fixture
    def db_manager(self):
        """Create an in-memory database manager for testing."""
        db = DatabaseManager(":memory:")
        df = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "gender": ["Male", "Female", "Male", "Female", "Male"],
            "age": [25, 30, 35, 28, 32],
            "score": [85, 90, 78, 92, 88]
        })
        db.import_data(df, "students")
        return db
    
    @pytest.fixture
    def filter_engine(self, db_manager):
        """Create a FilterEngine instance."""
        return FilterEngine(db_manager)
    
    def test_build_filter_query_with_list_values(self, filter_engine):
        """Test building filter query with list of values."""
        filters = {"gender": ["Male", "Female"]}
        where_clause = filter_engine.build_filter_query(filters)
        assert "gender IN" in where_clause
        assert "Male" in where_clause
        assert "Female" in where_clause
    
    def test_build_filter_query_with_range(self, filter_engine):
        """Test building filter query with range."""
        filters = {"age": (25, 35)}
        where_clause = filter_engine.build_filter_query(filters)
        assert "age BETWEEN" in where_clause
        assert "25" in where_clause
        assert "35" in where_clause
    
    def test_build_filter_query_with_string_value(self, filter_engine):
        """Test building filter query with single string value."""
        filters = {"gender": "Male"}
        where_clause = filter_engine.build_filter_query(filters)
        assert "gender = 'Male'" in where_clause
    
    def test_build_filter_query_with_numeric_value(self, filter_engine):
        """Test building filter query with numeric value."""
        filters = {"age": 25}
        where_clause = filter_engine.build_filter_query(filters)
        assert "age = 25" in where_clause
    
    def test_build_filter_query_empty_filters(self, filter_engine):
        """Test building filter query with empty filters."""
        filters = {}
        where_clause = filter_engine.build_filter_query(filters)
        assert where_clause == ""
    
    def test_apply_filters_to_query(self, filter_engine):
        """Test applying filters to a query."""
        base_query = "SELECT * FROM students"
        filters = {"gender": "Male"}
        result_query = filter_engine.apply_filters(base_query, filters)
        assert "WHERE" in result_query
        assert "gender = 'Male'" in result_query
    
    def test_apply_filters_to_query_with_existing_where(self, filter_engine):
        """Test applying filters to query that already has WHERE clause."""
        base_query = "SELECT * FROM students WHERE age > 25"
        filters = {"gender": "Male"}
        result_query = filter_engine.apply_filters(base_query, filters)
        assert "AND" in result_query
        assert "gender = 'Male'" in result_query
    
    def test_get_filter_options(self, filter_engine):
        """Test retrieving available filter options."""
        options = filter_engine.get_filter_options("students", "gender")
        assert "Male" in options
        assert "Female" in options
    
    def test_get_column_range(self, filter_engine):
        """Test retrieving min and max values for a column."""
        min_val, max_val = filter_engine.get_column_range("students", "age")
        assert min_val == 25
        assert max_val == 35
    
    def test_validate_filters_valid(self, filter_engine):
        """Test validating valid filters."""
        filters = {"gender": ["Male"], "age": (25, 35)}
        is_valid, errors = filter_engine.validate_filters(filters)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_filters_empty_list(self, filter_engine):
        """Test validating filters with empty list."""
        filters = {"gender": []}
        is_valid, errors = filter_engine.validate_filters(filters)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_validate_filters_invalid_range(self, filter_engine):
        """Test validating filters with invalid range."""
        filters = {"age": (35, 25)}  # start > end
        is_valid, errors = filter_engine.validate_filters(filters)
        assert is_valid is False
        assert len(errors) > 0
    
    def test_clear_filters(self, filter_engine):
        """Test clearing all filters."""
        cleared = filter_engine.clear_filters()
        assert cleared == {}
