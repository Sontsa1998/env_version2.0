# Student Performance Analyzer

An interactive web application for analyzing student performance data using Streamlit, DuckDB, and Plotly.

## Overview

The Student Performance Analyzer enables educators and administrators to:
- Upload and manage student performance data from CSV files
- Store data efficiently using DuckDB
- Apply dynamic filters to focus on specific student groups
- Visualize four key performance indicators (KPIs)
- Explore relationships between study habits and academic performance

## Features

### 1. Data Upload
- Upload CSV files containing student performance data
- Automatic validation of file structure and required columns
- Support for multiple data sources with automatic merging

### 2. Dynamic Filtering
- Filter by gender, age range, parental education level, and more
- Apply multiple filters simultaneously with AND logic
- Real-time visualization updates

### 3. Key Performance Indicators
- **KPI 1**: Average exam scores by demographic group
- **KPI 2**: Correlation between study hours and exam performance
- **KPI 3**: Impact of attendance on exam scores
- **KPI 4**: Relationship between sleep hours and academic performance

### 4. Interactive Visualizations
- Interactive charts using Plotly
- Hover information for detailed data exploration
- Responsive design for different screen sizes

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd student-performance-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
streamlit run src/app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Uploading Data

1. Navigate to the "Data Upload" section
2. Upload `student_habits_performance.csv`
3. Upload `StudentPerformanceFactors.csv`
4. The application will validate and import the data

### Analyzing Data

1. Use the "Filters" section to refine your analysis
2. Select specific demographics, age ranges, or other criteria
3. View the four KPI visualizations that update in real-time
4. Hover over data points for detailed information

## Project Structure

```
student-performance-analyzer/
├── src/
│   ├── __init__.py
│   ├── app.py                      # Main Streamlit application
│   ├── file_manager.py             # CSV file handling
│   ├── database_manager.py         # DuckDB integration
│   ├── filter_engine.py            # Dynamic filtering
│   ├── kpi_calculator.py           # KPI calculations
│   └── visualization_engine.py     # Plotly visualizations
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── test_file_manager.py        # File manager tests
│   ├── test_database_manager.py    # Database manager tests
│   ├── test_filter_engine.py       # Filter engine tests
│   ├── test_kpi_calculator.py      # KPI calculator tests
│   └── test_visualization_engine.py # Visualization tests
├── data/                           # Data directory
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Format

### student_habits_performance.csv

Required columns:
- `student_id`: Unique student identifier
- `age`: Student age
- `gender`: Student gender
- `study_hours_per_day`: Daily study hours
- `social_media_hours`: Daily social media hours
- `netflix_hours`: Daily Netflix hours
- `part_time_job`: Whether student has part-time job
- `attendance_percentage`: Class attendance percentage
- `sleep_hours`: Daily sleep hours
- `diet_quality`: Quality of diet
- `exercise_frequency`: Exercise frequency
- `parental_education_level`: Parent's education level
- `internet_quality`: Internet connection quality
- `mental_health_rating`: Mental health rating
- `extracurricular_participation`: Participation in extracurricular activities
- `exam_score`: Final exam score

### StudentPerformanceFactors.csv

Required columns:
- `Hours_Studied`: Total hours studied
- `Attendance`: Attendance percentage
- `Parental_Involvement`: Level of parental involvement
- `Access_to_Resources`: Access to learning resources
- `Extracurricular_Activities`: Participation in activities
- `Sleep_Hours`: Daily sleep hours
- `Previous_Scores`: Previous exam scores
- `Motivation_Level`: Student motivation level
- `Internet_Access`: Whether student has internet access
- `Tutoring_Sessions`: Number of tutoring sessions
- `Family_Income`: Family income level
- `Teacher_Quality`: Quality of teaching
- `School_Type`: Type of school
- `Peer_Influence`: Influence of peers
- `Physical_Activity`: Physical activity level
- `Learning_Disabilities`: Whether student has learning disabilities
- `Parental_Education_Level`: Parent's education level
- `Distance_from_Home`: Distance from home to school
- `Gender`: Student gender
- `Exam_Score`: Final exam score

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_file_manager.py

# Run with coverage report
pytest --cov=src tests/
```

### Test Structure

- **Unit Tests**: Test specific functions and edge cases
- **Property-Based Tests**: Test universal properties across random inputs using Hypothesis

## Performance

- Handles datasets up to 100,000 rows
- Query execution within 2 seconds
- Filter updates within 1 second
- Import operations within 5 seconds for files up to 50MB

## Error Handling

The application includes comprehensive error handling for:
- Invalid CSV file formats
- Missing required columns
- Invalid data types
- Database connection errors
- Insufficient data for visualizations

## Contributing

When contributing to this project:
1. Follow PEP 8 style guidelines
2. Include type hints for all functions
3. Add docstrings to all modules and functions
4. Write tests for new functionality
5. Ensure all tests pass before submitting

## License

This project is part of a group assignment for educational purposes.

## Support

For issues or questions, please contact the development team.

---

**Built with:**
- [Streamlit](https://streamlit.io/) - Web application framework
- [DuckDB](https://duckdb.org/) - SQL database engine
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pytest](https://pytest.org/) - Testing framework
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing
