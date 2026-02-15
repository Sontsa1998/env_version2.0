"""
Unit tests for database_manager module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_manager import DatabaseManager, handle_duplicates, remove_all_duplicates


class TestDatabaseManager:
    """Tests for DatabaseManager class."""
    
    @pytest.fixture
    def db_manager(self):
        """Create an in-memory database manager for testing."""
        return DatabaseManager(":memory:")
    
    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame for testing."""
        return pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 28, 32],
            "score": [85, 90, 78, 92, 88]
        })
    
    def test_initialize_connection(self, db_manager):
        """Test that database connection is initialized."""
        assert db_manager.connection is not None
    
    def test_import_data_creates_table(self, db_manager, sample_df):
        """Test that importing data creates a table."""
        db_manager.import_data(sample_df, "test_table")
        tables = db_manager.get_available_tables()
        assert "test_table" in tables
    
    def test_import_empty_dataframe_raises_error(self, db_manager):
        """Test that importing empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError):
            db_manager.import_data(empty_df, "test_table")
    
    def test_import_invalid_table_name_raises_error(self, db_manager, sample_df):
        """Test that invalid table name raises ValueError."""
        with pytest.raises(ValueError):
            db_manager.import_data(sample_df, "invalid-table-name!")
    
    def test_execute_query_returns_dataframe(self, db_manager, sample_df):
        """Test that query execution returns DataFrame."""
        db_manager.import_data(sample_df, "test_table")
        result = db_manager.execute_query("SELECT * FROM test_table")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5
    
    def test_execute_empty_query_raises_error(self, db_manager):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError):
            db_manager.execute_query("")
    
    def test_get_available_tables(self, db_manager, sample_df):
        """Test retrieving list of available tables."""
        db_manager.import_data(sample_df, "table1")
        db_manager.import_data(sample_df, "table2")
        tables = db_manager.get_available_tables()
        assert "table1" in tables
        assert "table2" in tables
    
    def test_get_table_info(self, db_manager, sample_df):
        """Test retrieving table metadata."""
        db_manager.import_data(sample_df, "test_table")
        info = db_manager.get_table_info("test_table")
        assert info["row_count"] == 5
        assert info["column_count"] == 4
        assert len(info["columns"]) == 4
    
    def test_table_exists(self, db_manager, sample_df):
        """Test checking if table exists."""
        db_manager.import_data(sample_df, "test_table")
        assert db_manager.table_exists("test_table") is True
        assert db_manager.table_exists("nonexistent") is False
    
    def test_delete_table(self, db_manager, sample_df):
        """Test deleting a table."""
        db_manager.import_data(sample_df, "test_table")
        db_manager.delete_table("test_table")
        assert db_manager.table_exists("test_table") is False
    
    def test_close_connection(self, db_manager):
        """Test closing database connection."""
        db_manager.close()
        assert db_manager.connection is None


class TestHandleDuplicates:
    """Tests for handle_duplicates function."""
    
    def test_keep_first_duplicate(self):
        """Test keeping first occurrence of duplicates."""
        df = pd.DataFrame({
            "id": [1, 1, 2, 2, 3],
            "name": ["Alice", "Alice", "Bob", "Bob", "Charlie"]
        })
        result = handle_duplicates(df, subset=["id"], keep="first")
        assert len(result) == 3
        assert list(result["id"]) == [1, 2, 3]
    
    def test_keep_last_duplicate(self):
        """Test keeping last occurrence of duplicates."""
        df = pd.DataFrame({
            "id": [1, 1, 2, 2, 3],
            "name": ["Alice", "Alice", "Bob", "Bob", "Charlie"]
        })
        result = handle_duplicates(df, subset=["id"], keep="last")
        assert len(result) == 3
        assert list(result["id"]) == [1, 2, 3]
    
    def test_invalid_keep_parameter_raises_error(self):
        """Test that invalid keep parameter raises ValueError."""
        df = pd.DataFrame({"id": [1, 1, 2]})
        with pytest.raises(ValueError):
            handle_duplicates(df, keep="invalid")


class TestRemoveAllDuplicates:
    """Tests for remove_all_duplicates function."""
    
    def test_remove_all_duplicates(self):
        """Test removing all duplicate records."""
        df = pd.DataFrame({
            "id": [1, 1, 2, 2, 3],
            "name": ["Alice", "Alice", "Bob", "Bob", "Charlie"]
        })
        result = remove_all_duplicates(df, subset=["id"])
        assert len(result) == 1
        assert result.iloc[0]["id"] == 3
    
    def test_remove_all_duplicates_no_duplicates(self):
        """Test removing duplicates when none exist."""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"]
        })
        result = remove_all_duplicates(df, subset=["id"])
        assert len(result) == 3
