"""
Database Manager module for DuckDB integration.

This module provides functions to manage DuckDB connections, create tables,
import data, and execute queries.
"""

from typing import List, Optional
import pandas as pd
import duckdb
from pathlib import Path


class DatabaseManager:
    """Manages DuckDB database connections and operations."""
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize DuckDB connection.
        
        Args:
            db_path: Path to DuckDB database file. Use ":memory:" for in-memory database.
        """
        self.db_path = db_path
        self.connection = None
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize or reconnect to DuckDB database."""
        try:
            self.connection = duckdb.connect(self.db_path)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DuckDB connection: {str(e)}")
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def import_data(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> None:
        """
        Import a pandas DataFrame into a DuckDB table.
        
        Args:
            df: pandas DataFrame to import
            table_name: Name of the table to create/update
            if_exists: How to behave if table exists ('replace', 'append', 'fail')
        
        Raises:
            ValueError: If DataFrame is empty or table_name is invalid
            RuntimeError: If import operation fails
        """
        if df.empty:
            raise ValueError("Cannot import empty DataFrame")
        
        if not table_name or not table_name.replace("_", "").isalnum():
            raise ValueError(f"Invalid table name: {table_name}")
        
        try:
            if if_exists == "replace":
                self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            self.connection.register(table_name, df)
            self.connection.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}")
            self.connection.unregister(table_name)
        except Exception as e:
            raise RuntimeError(f"Failed to import data into table '{table_name}': {str(e)}")
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.
        
        Args:
            query: SQL query to execute
        
        Returns:
            pandas DataFrame with query results
        
        Raises:
            RuntimeError: If query execution fails
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        try:
            result = self.connection.execute(query).fetchall()
            columns = [desc[0] for desc in self.connection.description]
            return pd.DataFrame(result, columns=columns)
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def get_available_tables(self) -> List[str]:
        """
        Get list of available tables in the database.
        
        Returns:
            List of table names
        """
        try:
            result = self.connection.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            ).fetchall()
            return [row[0] for row in result]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve table list: {str(e)}")
    
    def get_table_info(self, table_name: str) -> dict:
        """
        Get metadata about a table.
        
        Args:
            table_name: Name of the table
        
        Returns:
            Dictionary containing table metadata:
            - row_count: Number of rows
            - column_count: Number of columns
            - columns: List of column names and types
        
        Raises:
            RuntimeError: If table doesn't exist or query fails
        """
        try:
            # Get row count
            row_count = self.connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]
            
            # Get column info
            columns_info = self.connection.execute(
                f"PRAGMA table_info({table_name})"
            ).fetchall()
            
            columns = [
                {"name": col[1], "type": col[2]} for col in columns_info
            ]
            
            return {
                "row_count": row_count,
                "column_count": len(columns),
                "columns": columns
            }
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve table info for '{table_name}': {str(e)}")
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
        
        Returns:
            True if table exists, False otherwise
        """
        try:
            tables = self.get_available_tables()
            return table_name in tables
        except Exception:
            return False
    
    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.
        
        Args:
            table_name: Name of the table to delete
        
        Raises:
            RuntimeError: If deletion fails
        """
        try:
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        except Exception as e:
            raise RuntimeError(f"Failed to delete table '{table_name}': {str(e)}")
    
    def merge_tables(self, table1: str, table2: str, on_column: str, output_table: str) -> None:
        """
        Merge two tables based on a common column.
        
        Args:
            table1: Name of first table
            table2: Name of second table
            on_column: Column name to merge on
            output_table: Name of output table
        
        Raises:
            RuntimeError: If merge operation fails
        """
        try:
            query = f"""
            CREATE TABLE {output_table} AS
            SELECT * FROM {table1}
            FULL OUTER JOIN {table2}
            ON {table1}.{on_column} = {table2}.{on_column}
            """
            self.connection.execute(query)
        except Exception as e:
            raise RuntimeError(f"Failed to merge tables: {str(e)}")



def handle_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, 
                     keep: str = "first") -> pd.DataFrame:
    """
    Handle duplicate records in a DataFrame.
    
    Args:
        df: pandas DataFrame to process
        subset: Column names to consider for identifying duplicates. If None, all columns are used.
        keep: Which duplicates to keep ('first', 'last', or False to remove all)
    
    Returns:
        DataFrame with duplicates handled according to strategy
    """
    if keep not in ["first", "last"]:
        raise ValueError("keep must be 'first' or 'last'")
    
    return df.drop_duplicates(subset=subset, keep=keep)


def remove_all_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove all duplicate records from a DataFrame.
    
    Args:
        df: pandas DataFrame to process
        subset: Column names to consider for identifying duplicates
    
    Returns:
        DataFrame with all duplicates removed
    """
    return df.drop_duplicates(subset=subset, keep=False)
