"""
Main Streamlit application for Student Performance Analyzer.

This module orchestrates the UI components and coordinates between modules
to provide an interactive interface for analyzing student performance data.
"""

import streamlit as st
import pandas as pd
from io import StringIO
from pathlib import Path

from file_manager import (
    validate_csv_structure, parse_csv_file, get_file_info,
    validate_csv_not_empty, handle_encoding_error, FileEncodingError
)
from database_manager import DatabaseManager, handle_duplicates
from filter_engine import FilterEngine
from kpi_calculator import KPICalculator
from visualization_engine import VisualizationEngine

# Configure Streamlit page
st.set_page_config(
    page_title="Analyse de Performance des Etudiants",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "db_manager" not in st.session_state:
    st.session_state.db_manager = DatabaseManager(":memory:")

if "filters" not in st.session_state:
    st.session_state.filters = {}

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False


def render_header():
    """Display application title and description."""
    st.title("📊 Student Performance Analyzer")
    st.subheader("MEMBRE DU GROUPE : SONTSA CHRISTIAN - NZATI STEPHANE - SAMA CAMELIA - MBOULA MONICA")
    st.markdown("""
    Bienvenue dans l’Analyseur de performance des étudiants ! Cette application aide les enseignants et les administrateurs à analyser les données de performance des étudiants grâce à des visualisations interactives et des filtres dynamiques.
    Fonctionnalités :
    <br/>- Importer et gérer les données de performance des étudiants
    <br/>- Appliquer des filtres dynamiques pour cibler des groupes d’étudiants spécifiques
    <br/>- Consulter quatre indicateurs clés de performance (KPI)
    <br/>- Explorer les relations entre les habitudes d’étude et les performances académiques
    """, unsafe_allow_html=True
)


def render_upload_section():
    """Display file upload interface."""
    st.header("📁 Charger fichiers")
    st.markdown("Charger les fichiers contenant les données des performances Etudiants.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📌 Charger student_habits_performance.csv")
        habits_file = st.file_uploader(
            "Choose habits file",
            type="csv",
            key="habits_upload"
        )
    
    with col2:
        st.info("📌 Charger StudentPerformanceFactors.csv")
        factors_file = st.file_uploader(
            "Choose factors file",
            type="csv",
            key="factors_upload"
        )
    
    if habits_file or factors_file:
        try:
            if habits_file:
                # Read and parse habits file
                file_content = habits_file.read().decode("utf-8")
                df_habits = parse_csv_file(file_content)
                
                # Validate structure
                is_valid, error_msg = validate_csv_not_empty(df_habits)
                if not is_valid:
                    st.error(f"❌ Habits file error: {error_msg}")
                else:
                    # Remove duplicates
                    df_habits = handle_duplicates(df_habits, keep="first")
                    
                    # Import to database
                    st.session_state.db_manager.import_data(df_habits, "student_habits_performance")
                    st.success(f"✅ Habits file imported: {len(df_habits)} rows")
            
            if factors_file:
                # Read and parse factors file
                file_content = factors_file.read().decode("utf-8")
                df_factors = parse_csv_file(file_content)
                
                # Validate structure
                is_valid, error_msg = validate_csv_not_empty(df_factors)
                if not is_valid:
                    st.error(f"❌ Factors file error: {error_msg}")
                else:
                    # Remove duplicates
                    df_factors = handle_duplicates(df_factors, keep="first")
                    
                    # Import to database
                    st.session_state.db_manager.import_data(df_factors, "student_performance_factors")
                    st.success(f"✅ Factors file imported: {len(df_factors)} rows")
            
            st.session_state.data_loaded = True
        
        except FileEncodingError as e:
            st.error(f"❌ File encoding error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")


def render_filter_section():
    """Display dynamic filter controls."""
    if not st.session_state.data_loaded:
        st.info("📌 Upload data files first to enable filtering")
        return
    
    st.header("🔍 Filtres")
    st.markdown("Appliquer les filtres pour profiler votre analyse.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender_options = ["All"]
        try:
            filter_engine = FilterEngine(st.session_state.db_manager)
            if st.session_state.db_manager.table_exists("student_habits_performance"):
                gender_options.extend(filter_engine.get_filter_options("student_habits_performance", "gender"))
        except:
            pass
        
        selected_gender = st.selectbox("Gender", gender_options)
        if selected_gender != "All":
            st.session_state.filters["gender"] = selected_gender
        elif "gender" in st.session_state.filters:
            del st.session_state.filters["gender"]
    
    with col2:
        age_range = st.slider("Age Range", 17, 24, (17, 24))
        st.session_state.filters["age"] = age_range
    
    with col3:
        education_options = ["All", "High School", "Bachelor", "Master", "Postgraduate", "None"]
        selected_education = st.selectbox("Parental Education", education_options)
        if selected_education != "All":
            st.session_state.filters["parental_education_level"] = selected_education
        elif "parental_education_level" in st.session_state.filters:
            del st.session_state.filters["parental_education_level"]
    
    if st.button("Clear Filters"):
        st.session_state.filters = {}
        st.rerun()


def render_kpi_section():
    """Display all four KPI visualizations."""
    if not st.session_state.data_loaded:
        st.info("📌 Upload data files first to view KPIs")
        return
    
    st.header("📈 Indicateurs de Performance Clés")
    
    try:
        kpi_calc = KPICalculator(st.session_state.db_manager, st.session_state.filters)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("KPI 1: Score Moyen par Groupe")
            try:
                data_kpi1 = kpi_calc.calculate_kpi_1_scores_by_group()
                if not data_kpi1.empty:
                    fig1 = VisualizationEngine.create_kpi_1_chart(data_kpi1)
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("No data available for this KPI")
            except Exception as e:
                st.error(f"Error calculating KPI 1: {str(e)}")
        
        with col2:
            st.subheader("KPI 2: Corrélation des heures d’étude")
            try:
                data_kpi2 = kpi_calc.calculate_kpi_2_study_correlation()
                if not data_kpi2.empty:
                    fig2 = VisualizationEngine.create_kpi_2_chart(data_kpi2)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No data available for this KPI")
            except Exception as e:
                st.error(f"Error calculating KPI 2: {str(e)}")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("KPI 3: Impact de l’assiduité")
            try:
                data_kpi3 = kpi_calc.calculate_kpi_3_attendance_impact()
                if not data_kpi3.empty:
                    fig3 = VisualizationEngine.create_kpi_3_chart(data_kpi3)
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("No data available for this KPI")
            except Exception as e:
                st.error(f"Error calculating KPI 3: {str(e)}")
        
        with col4:
            st.subheader("KPI 4: Performance liée au sommeil")
            try:
                data_kpi4 = kpi_calc.calculate_kpi_4_sleep_performance()
                if not data_kpi4.empty:
                    fig4 = VisualizationEngine.create_kpi_4_chart(data_kpi4)
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.info("No data available for this KPI")
            except Exception as e:
                st.error(f"Error calculating KPI 4: {str(e)}")
    
    except Exception as e:
        st.error(f"Error rendering KPIs: {str(e)}")


def main():
    """Main application entry point."""
    render_header()
    
    st.divider()
    
    render_upload_section()
    
    st.divider()
    
    render_filter_section()
    
    st.divider()
    
    render_kpi_section()
    
    st.divider()
    
    st.markdown("---")
    st.markdown("<center>**Student Performance Analyzer** | Built with Streamlit, DuckDB, and Plotly<center/>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
