"""
Unit tests for visualization_engine module.
"""

import pytest
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from visualization_engine import VisualizationEngine


class TestVisualizationEngine:
    """Tests for VisualizationEngine class."""
    
    @pytest.fixture
    def sample_kpi1_data(self):
        """Sample data for KPI 1."""
        return pd.DataFrame({
            "group": ["Male", "Female"],
            "average_score": [85.0, 88.0],
            "count": [50, 50]
        })
    
    @pytest.fixture
    def sample_kpi2_data(self):
        """Sample data for KPI 2."""
        return pd.DataFrame({
            "study_hours": [4.0, 5.0, 6.0, 7.0],
            "exam_score": [75.0, 80.0, 85.0, 90.0]
        })
    
    @pytest.fixture
    def sample_kpi3_data(self):
        """Sample data for KPI 3."""
        return pd.DataFrame({
            "attendance_range": [70.0, 80.0, 90.0],
            "average_score": [75.0, 82.0, 88.0],
            "count": [30, 40, 30]
        })
    
    @pytest.fixture
    def sample_kpi4_data(self):
        """Sample data for KPI 4."""
        return pd.DataFrame({
            "sleep_hours": [6.0, 7.0, 8.0, 9.0],
            "exam_score": [70.0, 80.0, 85.0, 88.0]
        })
    
    def test_create_kpi_1_chart(self, sample_kpi1_data):
        """Test creating KPI 1 chart."""
        fig = VisualizationEngine.create_kpi_1_chart(sample_kpi1_data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == "bar"
    
    def test_create_kpi_1_chart_empty_data(self):
        """Test creating KPI 1 chart with empty data."""
        empty_df = pd.DataFrame()
        fig = VisualizationEngine.create_kpi_1_chart(empty_df)
        assert isinstance(fig, go.Figure)
        # Should have annotation for empty data
        assert len(fig.layout.annotations) > 0
    
    def test_create_kpi_2_chart(self, sample_kpi2_data):
        """Test creating KPI 2 chart."""
        fig = VisualizationEngine.create_kpi_2_chart(sample_kpi2_data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == "scatter"
    
    def test_create_kpi_2_chart_empty_data(self):
        """Test creating KPI 2 chart with empty data."""
        empty_df = pd.DataFrame()
        fig = VisualizationEngine.create_kpi_2_chart(empty_df)
        assert isinstance(fig, go.Figure)
        assert len(fig.layout.annotations) > 0
    
    def test_create_kpi_3_chart(self, sample_kpi3_data):
        """Test creating KPI 3 chart."""
        fig = VisualizationEngine.create_kpi_3_chart(sample_kpi3_data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == "scatter"
    
    def test_create_kpi_3_chart_empty_data(self):
        """Test creating KPI 3 chart with empty data."""
        empty_df = pd.DataFrame()
        fig = VisualizationEngine.create_kpi_3_chart(empty_df)
        assert isinstance(fig, go.Figure)
        assert len(fig.layout.annotations) > 0
    
    def test_create_kpi_4_chart(self, sample_kpi4_data):
        """Test creating KPI 4 chart."""
        fig = VisualizationEngine.create_kpi_4_chart(sample_kpi4_data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert fig.data[0].type == "scatter"
    
    def test_create_kpi_4_chart_empty_data(self):
        """Test creating KPI 4 chart with empty data."""
        empty_df = pd.DataFrame()
        fig = VisualizationEngine.create_kpi_4_chart(empty_df)
        assert isinstance(fig, go.Figure)
        assert len(fig.layout.annotations) > 0
    
    def test_create_empty_chart(self):
        """Test creating empty placeholder chart."""
        fig = VisualizationEngine._create_empty_chart("Test Title", "No data")
        assert isinstance(fig, go.Figure)
        assert len(fig.layout.annotations) > 0
        assert fig.layout.title.text == "Test Title"
