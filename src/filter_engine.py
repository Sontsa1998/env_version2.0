"""
Filter Engine module for dynamic data filtering.

This module provides functions to build and apply dynamic filters to SQL queries
and retrieve available filter options.
"""

from typing import Dict, List, Any, Optional, Tuple
from database_manager import DatabaseManager


class FilterEngine:
    """Manages dynamic filtering of data."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize Filter Engine with database manager.
        
        Args:
            db_manager: DatabaseManager instance for executing queries
        """
        self.db_manager = db_manager
    
    def build_filter_query(self, filters: Dict[str, Any]) -> str:
        """
        Build a WHERE clause from filter specifications.
        
        Args:
            filters: Dictionary of filter specifications
                    Example: {
                        "gender": ["Male", "Female"],
                        "age_range": (18, 25),
                        "attendance_range": (80.0, 100.0)
                    }
        
        Returns:
            WHERE clause string (without "WHERE" keyword)
        """
        if not filters:
            return ""
        
        conditions = []
        
        for key, value in filters.items():
            if value is None:
                continue
            
            if isinstance(value, list) and len(value) > 0:
                # Handle list of values (IN clause)
                values_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                conditions.append(f"{key} IN ({values_str})")
            
            elif isinstance(value, tuple) and len(value) == 2:
                # Handle range (BETWEEN clause)
                conditions.append(f"{key} BETWEEN {value[0]} AND {value[1]}")
            
            elif isinstance(value, str):
                # Handle single string value
                conditions.append(f"{key} = '{value}'")
            
            elif isinstance(value, (int, float)):
                # Handle single numeric value
                conditions.append(f"{key} = {value}")
            
            elif isinstance(value, bool):
                # Handle boolean value
                conditions.append(f"{key} = {value}")
        
        return " AND ".join(conditions) if conditions else ""
    
    def apply_filters(self, base_query: str, filters: Dict[str, Any]) -> str:
        """
        Apply filters to a SQL query.
        
        Args:
            base_query: Base SQL query (should not include WHERE clause)
            filters: Dictionary of filter specifications
        
        Returns:
            Complete SQL query with filters applied
        """
        where_clause = self.build_filter_query(filters)
        
        if not where_clause:
            return base_query
        
        # Check if query already has WHERE clause
        if "WHERE" in base_query.upper():
            return f"{base_query} AND {where_clause}"
        else:
            return f"{base_query} WHERE {where_clause}"
    
    def get_filter_options(self, table_name: str, column_name: str) -> List[Any]:
        """
        Get available values for a column to use in filters.
        
        Args:
            table_name: Name of the table
            column_name: Name of the column
        
        Returns:
            List of unique values in the column
        
        Raises:
            RuntimeError: If query fails
        """
        try:
            query = f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name}"
            result = self.db_manager.execute_query(query)
            return result[column_name].tolist()
        except Exception as e:
            raise RuntimeError(f"Failed to get filter options for {column_name}: {str(e)}")
    
    def get_column_range(self, table_name: str, column_name: str) -> Tuple[float, float]:
        """
        Get min and max values for a numeric column.
        
        Args:
            table_name: Name of the table
            column_name: Name of the numeric column
        
        Returns:
            Tuple of (min_value, max_value)
        
        Raises:
            RuntimeError: If query fails
        """
        try:
            query = f"SELECT MIN({column_name}) as min_val, MAX({column_name}) as max_val FROM {table_name}"
            result = self.db_manager.execute_query(query)
            min_val = result["min_val"].iloc[0]
            max_val = result["max_val"].iloc[0]
            return (float(min_val), float(max_val))
        except Exception as e:
            raise RuntimeError(f"Failed to get range for {column_name}: {str(e)}")
    
    def validate_filters(self, filters: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate filter specifications.
        
        Args:
            filters: Dictionary of filter specifications
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        for key, value in filters.items():
            if value is None:
                continue
            
            if isinstance(value, list):
                if len(value) == 0:
                    errors.append(f"Filter '{key}' has empty list")
            
            elif isinstance(value, tuple):
                if len(value) != 2:
                    errors.append(f"Filter '{key}' range must have exactly 2 values")
                elif value[0] > value[1]:
                    errors.append(f"Filter '{key}' range start is greater than end")
        
        return len(errors) == 0, errors
    
    def clear_filters(self) -> Dict[str, Any]:
        """
        Clear all filters.
        
        Returns:
            Empty filter dictionary
        """
        return {}
