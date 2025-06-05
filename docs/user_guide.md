# User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Single Year Analysis](#single-year-analysis)
4. [Dual Year Analysis](#dual-year-analysis)
5. [Map Generation](#map-generation)
6. [Exporting Maps](#exporting-maps)
7. [Tips and Tricks](#tips-and-tricks)

## Getting Started

### Installation
1. Download the latest release
2. Double-click the executable
3. No additional installation required

### First Launch
1. Choose analysis type:
   - Single Year: Compare before/after a specific year
   - Dual Year: Analyze three time periods

### Loading Data
1. Click "Load Excel File"
2. Select your data file
3. Review the data summary
4. Check for any validation messages

## Interface Overview

### Main Window Components
1. Left Panel
   - Data input controls
   - Color settings
   - Year filters
   - Taxonomic selection
2. Right Panel
   - Map display area
   - Legend
3. Top Bar
   - Title
   - Navigation

### Control Sections
1. Data Input
   - Load Excel button
   - File info display
2. Color Settings
   - Color pickers for periods
   - Custom color support
3. Year Filter(s)
   - Single or dual year input
4. Species Selection
   - Family dropdown
   - Genus dropdown
   - Species dropdown

## Single Year Analysis

### Purpose
Compare bee distribution before and after a specific year.

### Steps
1. Load your data file
2. Choose colors:
   - Pre-year color
   - Post-year color
   - All records color
3. Enter the dividing year (optional)
4. Select taxonomic filters:
   - Family
   - Genus
   - Species
5. Generate map

### Color Scheme
- Grey: Records before year
- Red: Records after year
- Yellow: All records (when no year specified)

## Dual Year Analysis

### Purpose
Analyze bee distribution across three time periods.

### Steps
1. Load your data file
2. Choose colors:
   - First period color
   - Second period color
   - Third period color
3. Enter both years:
   - First year
   - Second year
4. Select taxonomic filters
5. Generate map

### Time Periods
1. First Period: Records ≤ First year
2. Second Period: Records between years
3. Third Period: Records > Second year

## Map Generation

### Process
1. Configure all settings
2. Click "Generate Map"
3. Review the visualization
4. Adjust if needed

### Map Elements
1. County boundaries
2. Color-coded regions
3. Legend
4. Title with taxonomic info
5. Year information

### Validation
- County name matching
- Year format checking
- Color validation
- Data presence verification

## Exporting Maps

### Export Process
1. Generate desired map
2. Click "Download Map"
3. Map saves automatically to Downloads folder

### File Format
- Format: TIFF
- Resolution: 300 DPI
- Filename format:
  - Single Year: `Family-Genus-species_year_MMDD_HHMM.tiff`
  - Dual Year: `Family-Genus-species_year1-year2_MMDD_HHMM.tiff`

### Quality Control
- Check legend visibility
- Verify color contrast
- Ensure text readability
- Confirm data accuracy

## Tips and Tricks

### Performance
- Clean data before importing
- Use appropriate file sizes
- Close unused windows

### Color Selection
- Use contrasting colors
- Test visibility
- Consider colorblind accessibility
- Use standard colors when possible

### Data Management
- Keep regular backups
- Use consistent naming
- Validate data before import
- Check county names carefully

### Troubleshooting
1. Missing Counties
   - Verify county names
   - Check standardization
   - Review error messages
2. Color Issues
   - Use valid color names
   - Try hex codes
   - Check contrast
3. Year Problems
   - Use YYYY format
   - Verify chronological order
   - Check data range 