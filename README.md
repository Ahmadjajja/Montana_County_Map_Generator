# Montana Bee County Map Generator

A powerful visualization tool for analyzing and mapping bee distribution across Montana counties over different time periods.

## Overview

The Montana Bee County Map Generator is a desktop application designed to help researchers and enthusiasts visualize and analyze bee distribution patterns across Montana counties. The application supports both single-year and dual-year analysis, allowing users to track changes in bee populations over time.

## Features

### 1. Single Year Analysis
- Visualize bee distribution before and after a specific year
- Color-coded counties showing:
  - Pre-year records (First color)
  - Post-year records (Second color)
  - All records when no year specified (Single color)

### 2. Dual Year Analysis
- Analyze bee distribution across three time periods using two year boundaries
- Color-coded counties showing:
  - Records ≤ First year (First color)
  - Records between First and Second year (Second color)
  - Records > Second year (Third color)

### 3. Common Features
- Interactive taxonomic filtering:
  - Family level (with "All" option)
  - Genus level (with "All" option)
  - Species level (with "all" option)
- Customizable color schemes
- High-resolution map export (300 DPI TIFF format)
- User-friendly interface with tooltips and helper text
- Real-time map generation
- Comprehensive data validation
- County name standardization

## Installation

### Prerequisites
- Windows 10 or later
- Python 3.8 or later (if installing from source)

### Method 1: Using the Executable (Recommended)
1. Download the latest `Montana_Bee_Map_Generator.exe` from the releases page
2. Double-click the executable to run the application
3. No additional installation steps required

### Method 2: Installing from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Montana_Bee_Map_Generator.git
   cd Montana_Bee_Map_Generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install pandas geopandas matplotlib tkinter
   ```

4. Run the application:
   ```bash
   python GUI_MAP_Generator.py
   ```

## Data Requirements

### Excel File Format
Your Excel file must include the following columns:
- `county`: Montana county names
- `family`: Bee family names
- `genus`: Bee genus names
- `species`: Bee species names
- `year`: Collection year (YYYY format)

### County Names
- County names must match Montana county names exactly
- The application will standardize county names by:
  - Converting to lowercase
  - Removing extra whitespace
  - Converting '&' to 'and'

## Usage Guide

1. **Launch the Application**
   - Run the executable or start from source
   - Select analysis type (Single Year or Dual Year)

2. **Load Data**
   - Click "Load Excel File"
   - Select your Excel file (.xlsx format)
   - Review the data summary

3. **Configure Settings**
   - Select colors for different time periods
   - Enter year(s) for temporal analysis
   - Choose taxonomic filters:
     - Select Family (or "All")
     - Select Genus (or "All")
     - Select Species (or "all")

4. **Generate and Export Map**
   - Click "Generate Map" to create visualization
   - Review the map and legend
   - Click "Download Map" to save as TIFF
   - Maps are saved to your Downloads folder

## Troubleshooting

### Common Issues
1. **Missing Counties**
   - Ensure county names match exactly
   - Check console output for valid county names
   - Review standardization rules

2. **No Data Shown**
   - Verify Excel file format
   - Check required columns exist
   - Ensure data contains Montana records

3. **Invalid Years**
   - Years must be 4-digit numbers
   - First year must be less than second year (Dual Year Analysis)

### Error Messages
- "Missing required columns": Check Excel file format
- "No valid Montana county records": Verify county names
- "Invalid colors": Use valid color names or hex codes
- "Invalid years": Check year format and order

## Support

For bug reports and feature requests, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Montana State University
- Montana Geographic Information Clearinghouse for county boundary data
- All contributors to the Montana bee research community

## Version History

- v1.0.0 (2024-03-XX)
  - Initial release
  - Single and dual year analysis
  - High-resolution map export
  - Interactive filtering