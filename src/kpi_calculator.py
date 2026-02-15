"""
KPI Calculator module for computing key performance indicators.

This module provides functions to calculate various KPIs from student performance data.
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from database_manager import DatabaseManager
from filter_engine import FilterEngine


class KPICalculator:
    """Calculates key performance indicators from student data."""
    
    def __init__(self, db_manager: DatabaseManager, filters: Optional[Dict[str, Any]] = None):
        """
        Initialize KPI Calculator.
        
        Args:
            db_manager: DatabaseManager instance
            filters: Optional dictionary of active filters
        """
        self.db_manager = db_manager
        self.filter_engine = FilterEngine(db_manager)
        self.filters = filters or {}
    
    def _apply_filters_to_query(self, base_query: str, available_columns: list = None) -> str:
        """Apply active filters to a query, only for columns that exist."""
        if not self.filters:
            return base_query
        
        # Build WHERE clause manually to handle range filters correctly
        conditions = []
        
        for key, value in self.filters.items():
            if value is None:
                continue
            
            # Skip filters for columns that don't exist in this table
            # Check both lowercase and mixed-case versions
            if available_columns:
                key_found = False
                actual_key = key
                for col in available_columns:
                    if col.lower() == key.lower():
                        key_found = True
                        actual_key = col
                        break
                if not key_found:
                    continue
            else:
                actual_key = key
            
            if key == "age" and isinstance(value, tuple) and len(value) == 2:
                # Handle age range
                conditions.append(f'"{actual_key}" BETWEEN {value[0]} AND {value[1]}')
            elif isinstance(value, str):
                # Handle string values
                conditions.append(f'"{actual_key}" = \'{value}\'')
            elif isinstance(value, (int, float)):
                # Handle numeric values
                conditions.append(f'"{actual_key}" = {value}')
        
        if not conditions:
            return base_query
        
        where_clause = " AND ".join(conditions)
        
        # Check if query already has WHERE clause
        if "WHERE" in base_query.upper():
            return f"{base_query} AND {where_clause}"
        else:
            return f"{base_query} WHERE {where_clause}"
    
    def calculate_kpi_1_scores_by_group(self) -> pd.DataFrame:
        """
        Calculate average exam scores by demographic group.
        
        Returns:
            DataFrame with columns: group, average_score, count
        
        Raises:
            RuntimeError: If calculation fails
        """
        try:
            # Try to use student_habits_performance table
            available_cols_habits = ["age", "gender", "parental_education_level", "exam_score"]
            query = """
            SELECT 
                gender as group,
                AVG(exam_score) as average_score,
                COUNT(*) as count
            FROM student_habits_performance
            """
            
            query = self._apply_filters_to_query(query, available_cols_habits)
            query += " GROUP BY gender ORDER BY average_score DESC"
            
            result = self.db_manager.execute_query(query)
            
            if result.empty:
                # Fallback to student_performance_factors (note: capital letters in column names)
                available_cols_factors = ["Gender", "Parental_Education_Level", "Exam_Score"]
                query = """
                SELECT 
                    "Gender" as group,
                    AVG("Exam_Score") as average_score,
                    COUNT(*) as count
                FROM student_performance_factors
                """
                query = self._apply_filters_to_query(query, available_cols_factors)
                query += ' GROUP BY "Gender" ORDER BY average_score DESC'
                result = self.db_manager.execute_query(query)
            
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to calculate KPI 1: {str(e)}")
    
    def calculate_kpi_2_study_correlation(self) -> pd.DataFrame:
        """
        Calculate correlation between study hours and exam performance.
        
        Returns:
            DataFrame with study_hours and exam_score columns
        
        Raises:
            RuntimeError: If calculation fails
        """
        try:
            # Try student_habits_performance first
            available_cols_habits = ["age", "gender", "parental_education_level", "study_hours_per_day", "exam_score"]
            query = """
            SELECT 
                study_hours_per_day as study_hours,
                exam_score
            FROM student_habits_performance
            WHERE study_hours_per_day IS NOT NULL 
                AND exam_score IS NOT NULL
            """
            
            query = self._apply_filters_to_query(query, available_cols_habits)
            query += " ORDER BY study_hours_per_day"
            result = self.db_manager.execute_query(query)
            
            if result.empty:
                # Fallback to student_performance_factors (note: capital letters in column names)
                available_cols_factors = ["Gender", "Parental_Education_Level", "Hours_Studied", "Exam_Score"]
                query = """
                SELECT 
                    "Hours_Studied" as study_hours,
                    "Exam_Score" as exam_score
                FROM student_performance_factors
                WHERE "Hours_Studied" IS NOT NULL 
                    AND "Exam_Score" IS NOT NULL
                """
                query = self._apply_filters_to_query(query, available_cols_factors)
                query += " ORDER BY \"Hours_Studied\""
                result = self.db_manager.execute_query(query)
            
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to calculate KPI 2: {str(e)}")
    
    def calculate_kpi_3_attendance_impact(self) -> pd.DataFrame:
        """
        Calculate impact of attendance on exam scores.
        
        Returns:
            DataFrame with attendance and average_score columns
        
        Raises:
            RuntimeError: If calculation fails
        """
        try:
            # Try student_habits_performance first
            available_cols_habits = ["age", "gender", "parental_education_level", "attendance_percentage", "exam_score"]
            query = """
            SELECT 
                ROUND(attendance_percentage / 10) * 10 as attendance_range,
                AVG(exam_score) as average_score,
                COUNT(*) as count
            FROM student_habits_performance
            WHERE attendance_percentage IS NOT NULL 
                AND exam_score IS NOT NULL
            """
            
            query = self._apply_filters_to_query(query, available_cols_habits)
            query += " GROUP BY ROUND(attendance_percentage / 10) * 10 ORDER BY attendance_range"
            result = self.db_manager.execute_query(query)
            
            if result.empty:
                # Fallback to student_performance_factors (note: capital letters in column names)
                available_cols_factors = ["Gender", "Parental_Education_Level", "Attendance", "Exam_Score"]
                query = """
                SELECT 
                    ROUND("Attendance" / 10) * 10 as attendance_range,
                    AVG("Exam_Score") as average_score,
                    COUNT(*) as count
                FROM student_performance_factors
                WHERE "Attendance" IS NOT NULL 
                    AND "Exam_Score" IS NOT NULL
                """
                query = self._apply_filters_to_query(query, available_cols_factors)
                query += ' GROUP BY ROUND("Attendance" / 10) * 10 ORDER BY attendance_range'
                result = self.db_manager.execute_query(query)
            
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to calculate KPI 3: {str(e)}")
    
    def calculate_kpi_4_sleep_performance(self) -> pd.DataFrame:
        """
        Calculate relationship between sleep hours and academic performance.
        
        Returns:
            DataFrame with sleep_hours and exam_score columns
        
        Raises:
            RuntimeError: If calculation fails
        """
        try:
            # Try student_habits_performance first
            available_cols_habits = ["age", "gender", "parental_education_level", "sleep_hours", "exam_score"]
            query = """
            SELECT 
                sleep_hours,
                exam_score
            FROM student_habits_performance
            WHERE sleep_hours IS NOT NULL 
                AND exam_score IS NOT NULL
            """
            
            query = self._apply_filters_to_query(query, available_cols_habits)
            query += " ORDER BY sleep_hours"
            result = self.db_manager.execute_query(query)
            
            if result.empty:
                # Fallback to student_performance_factors (note: capital letters in column names)
                available_cols_factors = ["Gender", "Parental_Education_Level", "Sleep_Hours", "Exam_Score"]
                query = """
                SELECT 
                    "Sleep_Hours" as sleep_hours,
                    "Exam_Score" as exam_score
                FROM student_performance_factors
                WHERE "Sleep_Hours" IS NOT NULL 
                    AND "Exam_Score" IS NOT NULL
                """
                query = self._apply_filters_to_query(query, available_cols_factors)
                query += " ORDER BY \"Sleep_Hours\""
                result = self.db_manager.execute_query(query)
            
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to calculate KPI 4: {str(e)}")
    
    def calculate_correlation_coefficient(self, x: pd.Series, y: pd.Series) -> float:
        """
        Calculate Pearson correlation coefficient between two series.
        
        Args:
            x: First data series
            y: Second data series
        
        Returns:
            Correlation coefficient (-1 to 1)
        """
        if len(x) < 2 or len(y) < 2:
            return 0.0
        
        return float(np.corrcoef(x, y)[0, 1])
    
    def update_filters(self, filters: Dict[str, Any]) -> None:
        """
        Update active filters.
        
        Args:
            filters: New filter dictionary
        """
        self.filters = filters
