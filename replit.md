# Employee Management System

## Overview

This is a Streamlit-based employee management system that provides a comprehensive dashboard for managing company personnel. The application offers functionality for employee registration, data visualization, and reporting through an intuitive web interface. The system uses CSV files for data storage and leverages Plotly for creating interactive charts and visualizations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Layout**: Multi-page application with sidebar navigation
- **UI Components**: Wide layout with expandable sidebar, organized in columns for metrics display
- **Navigation**: Page-based routing system with four main sections: Dashboard, Employees, Reports, and Settings

### Data Storage
- **Primary Storage**: CSV file-based storage system located in `data/funcionarios.csv`
- **Data Structure**: Employee records with fields including name, email, phone, department, position, salary, hire date, status, and notes
- **Data Handling**: Centralized through `DataHandler` class with automatic file and directory creation
- **Caching**: Streamlit resource caching for data handler optimization

### Visualization Layer
- **Charting Library**: Plotly Express and Plotly Graph Objects for interactive visualizations
- **Chart Types**: Pie charts for department distribution, bar charts for salary analysis, histograms for salary distribution, box plots for salary variance, and line charts for hiring trends
- **Dashboard Metrics**: Real-time calculation of key performance indicators displayed in column layout

### Application Structure
- **Main Application**: `app.py` serves as the entry point with page routing and dashboard functionality
- **Utilities Layer**: Modular architecture with separate utilities for data handling and visualization generation
- **Error Handling**: Graceful handling of missing files and empty datasets with user-friendly warnings

### Data Management
- **CRUD Operations**: Full create, read, update, and delete functionality for employee records
- **Data Validation**: Built-in validation through pandas DataFrame structure
- **File Management**: Automatic creation of data directory and CSV file initialization
- **Data Persistence**: Direct CSV file operations for reliable data storage

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework and UI components
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library (both express and graph_objects modules)
- **datetime**: Date and time handling for employee records
- **os**: File system operations and path management
- **io**: Input/output operations support

### Data Dependencies
- **CSV Files**: Employee data stored in CSV format in local `data/` directory
- **File System**: Local file system for data persistence and configuration storage

### System Requirements
- **Python Environment**: Python 3.x runtime environment
- **File Permissions**: Read/write access to local directory for data storage
- **Browser Compatibility**: Modern web browser for Streamlit interface interaction