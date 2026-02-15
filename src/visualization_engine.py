"""
Visualization Engine module for creating interactive charts.

This module provides functions to create Plotly visualizations for KPIs.
"""

from typing import Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class VisualizationEngine:
    """Creates interactive visualizations using Plotly."""
    
    @staticmethod
    def create_kpi_1_chart(data: pd.DataFrame) -> go.Figure:
        """
        Create bar chart for average scores by demographic group.
        
        Args:
            data: DataFrame with columns: group, average_score, count
        
        Returns:
            Plotly Figure object
        """
        if data.empty:
            return VisualizationEngine._create_empty_chart(
                "KPI 1: Average Scores by Group",
                "No data available"
            )
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data["group"],
            y=data["average_score"],
            text=data["average_score"].round(2),
            textposition="auto",
            marker=dict(
                color=data["average_score"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Avg Score")
            ),
            hovertemplate="<b>%{x}</b><br>Average Score: %{y:.2f}<br>Count: %{customdata}<extra></extra>",
            customdata=data["count"]
        ))
        
        fig.update_layout(
            title="KPI 1: Average Exam Scores by Demographic Group",
            xaxis_title="Group",
            yaxis_title="Average Exam Score",
            hovermode="x unified",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def create_kpi_2_chart(data: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot for study hours correlation.
        
        Args:
            data: DataFrame with columns: study_hours, exam_score
        
        Returns:
            Plotly Figure object
        """
        if data.empty:
            return VisualizationEngine._create_empty_chart(
                "KPI 2: Study Hours Correlation",
                "No data available"
            )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data["study_hours"],
            y=data["exam_score"],
            mode="markers",
            marker=dict(
                size=8,
                color=data["exam_score"],
                colorscale="Plasma",
                showscale=True,
                colorbar=dict(title="Exam Score"),
                line=dict(width=1, color="white")
            ),
            text=data.index,
            hovertemplate="<b>Student %{text}</b><br>Study Hours: %{x:.2f}<br>Exam Score: %{y:.2f}<extra></extra>"
        ))
        
        # Add trend line if enough data points
        if len(data) > 2:
            z = np.polyfit(data["study_hours"], data["exam_score"], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(data["study_hours"].min(), data["study_hours"].max(), 100)
            y_trend = p(x_trend)
            
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=y_trend,
                mode="lines",
                name="Trend",
                line=dict(color="red", dash="dash"),
                hoverinfo="skip"
            ))
        
        fig.update_layout(
            title="KPI 2: Correlation Between Study Hours and Exam Performance",
            xaxis_title="Study Hours per Day",
            yaxis_title="Exam Score",
            hovermode="closest",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def create_kpi_3_chart(data: pd.DataFrame) -> go.Figure:
        """
        Create line chart for attendance impact.
        
        Args:
            data: DataFrame with columns: attendance_range, average_score, count
        
        Returns:
            Plotly Figure object
        """
        if data.empty:
            return VisualizationEngine._create_empty_chart(
                "KPI 3: Attendance Impact",
                "No data available"
            )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data["attendance_range"],
            y=data["average_score"],
            mode="lines+markers",
            name="Average Score",
            line=dict(color="rgb(31, 119, 180)", width=3),
            marker=dict(size=10),
            fill="tozeroy",
            hovertemplate="<b>Attendance: %{x:.0f}%</b><br>Average Score: %{y:.2f}<br>Count: %{customdata}<extra></extra>",
            customdata=data["count"]
        ))
        
        fig.update_layout(
            title="KPI 3: Impact of Attendance on Exam Scores",
            xaxis_title="Attendance Range (%)",
            yaxis_title="Average Exam Score",
            hovermode="x unified",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def create_kpi_4_chart(data: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot for sleep performance relationship.
        
        Args:
            data: DataFrame with columns: sleep_hours, exam_score
        
        Returns:
            Plotly Figure object
        """
        if data.empty:
            return VisualizationEngine._create_empty_chart(
                "KPI 4: Sleep Performance",
                "No data available"
            )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data["sleep_hours"],
            y=data["exam_score"],
            mode="markers",
            marker=dict(
                size=8,
                color=data["exam_score"],
                colorscale="Turbo",
                showscale=True,
                colorbar=dict(title="Exam Score"),
                line=dict(width=1, color="white")
            ),
            text=data.index,
            hovertemplate="<b>Student %{text}</b><br>Sleep Hours: %{x:.2f}<br>Exam Score: %{y:.2f}<extra></extra>"
        ))
        
        # Add trend line if enough data points
        if len(data) > 2:
            z = np.polyfit(data["sleep_hours"], data["exam_score"], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(data["sleep_hours"].min(), data["sleep_hours"].max(), 100)
            y_trend = p(x_trend)
            
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=y_trend,
                mode="lines",
                name="Trend",
                line=dict(color="red", dash="dash"),
                hoverinfo="skip"
            ))
        
        fig.update_layout(
            title="KPI 4: Relationship Between Sleep Hours and Academic Performance",
            xaxis_title="Sleep Hours per Night",
            yaxis_title="Exam Score",
            hovermode="closest",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def _create_empty_chart(title: str, message: str) -> go.Figure:
        """
        Create a placeholder chart for empty data.
        
        Args:
            title: Chart title
            message: Message to display
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        fig.update_layout(
            title=title,
            height=400,
            template="plotly_white",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig


# Import numpy for trend line calculations
import numpy as np
