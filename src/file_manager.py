"""
File Manager module for handling CSV file uploads and validation.

This module provides functions to validate CSV file structure, parse CSV files,
and retrieve file metadata.
"""

from typing import Tuple, List, Optional
import pandas as pd
from io import StringIO


def validate_csv_structure(file_content: str, required_columns: List[str]) -> Tuple[bool, str]:
    """
    Validate that a CSV file contains all required columns.
    
    Args:
        file_content: The content of the CSV file as a string
        required_columns: List of required column names
    
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if file is valid, False otherwise
        - error_message: Empty string if valid, error message if invalid
    
    Raises:
        ValueError: If file cannot be parsed as CSV
    """
    try:
        df = pd.read_csv(StringIO(file_content))
    except Exception as e:
        return False, f"Failed to parse CSV file: {str(e)}"
    
    # Check for required columns (case-insensitive)
    df_columns_lower = [col.lower() for col in df.columns]
    required_lower = [col.lower() for col in required_columns]
    
    missing_columns = [col for col in required_lower if col not in df_columns_lower]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, ""


def parse_csv_file(file_content: str) -> pd.DataFrame:
    """
    Parse a CSV file into a pandas DataFrame.
    
    Args:
        file_content: The content of the CSV file as a string
    
    Returns:
        pandas DataFrame containing the CSV data
    
    Raises:
        ValueError: If file cannot be parsed as CSV
    """
    try:
        df = pd.read_csv(StringIO(file_content))
        return df
    except Exception as e:
        raise ValueError(f"Failed to parse CSV file: {str(e)}")


def get_file_info(df: pd.DataFrame) -> dict:
    """
    Get metadata about a DataFrame (parsed from CSV).
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary containing file metadata:
        - row_count: Number of rows
        - column_count: Number of columns
        - columns: List of column names
        - memory_usage: Approximate memory usage in bytes
    """
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "memory_usage": df.memory_usage(deep=True).sum()
    }


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to lowercase with underscores.
    
    Args:
        df: pandas DataFrame with columns to normalize
    
    Returns:
        DataFrame with normalized column names
    """
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df


def validate_data_types(df: pd.DataFrame, expected_types: dict) -> Tuple[bool, List[str]]:
    """
    Validate that DataFrame columns have expected data types.
    
    Args:
        df: pandas DataFrame to validate
        expected_types: Dictionary mapping column names to expected types
    
    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: True if all types match, False otherwise
        - error_messages: List of type mismatch messages
    """
    errors = []
    
    for column, expected_type in expected_types.items():
        if column not in df.columns:
            continue
        
        # Try to convert to expected type
        try:
            if expected_type == "numeric":
                pd.to_numeric(df[column], errors="coerce")
            elif expected_type == "boolean":
                df[column].astype(bool)
        except Exception as e:
            errors.append(f"Column '{column}' cannot be converted to {expected_type}: {str(e)}")
    
    return len(errors) == 0, errors



class FileValidationError(Exception):
    """Exception raised when file validation fails."""
    pass


class FileEncodingError(Exception):
    """Exception raised when file encoding is invalid."""
    pass


def handle_encoding_error(file_bytes: bytes) -> str:
    """
    Handle file encoding errors by trying multiple encodings.
    
    Args:
        file_bytes: Raw bytes from the file
    
    Returns:
        Decoded file content as string
    
    Raises:
        FileEncodingError: If file cannot be decoded with any supported encoding
    """
    encodings = ["utf-8", "latin-1", "iso-8859-1", "cp1252"]
    
    for encoding in encodings:
        try:
            return file_bytes.decode(encoding)
        except (UnicodeDecodeError, AttributeError):
            continue
    
    raise FileEncodingError(
        f"Could not decode file with any supported encoding: {', '.join(encodings)}"
    )


def validate_file_size(file_size: int, max_size_mb: int = 50) -> Tuple[bool, str]:
    """
    Validate that file size is within acceptable limits.
    
    Args:
        file_size: Size of file in bytes
        max_size_mb: Maximum allowed file size in MB
    
    Returns:
        Tuple of (is_valid, message)
    """
    max_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_bytes:
        return False, f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum ({max_size_mb}MB)"
    
    return True, ""


def validate_csv_not_empty(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that CSV file is not empty.
    
    Args:
        df: pandas DataFrame to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(df) == 0:
        return False, "CSV file is empty"
    
    if len(df.columns) == 0:
        return False, "CSV file has no columns"
    
    return True, ""
