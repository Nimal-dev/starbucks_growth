# Starbucks Growth Opportunity Dashboard - Walkthrough

## Overview
This project identifies high-potential "Blue Ocean" markets for Starbucks expansion by cross-referencing global city populations with existing store locations.

**Key Insight:** South Asia (Dhaka, Lahore) and Sub-Saharan Africa (Lagos, Kinshasa) represent the largest untapped urban markets globally.

## Deliverables
- **Interactive Dashboard:** `dashboard/index.html` (Open in any modern browser)
- **Analytical Report:** `data/findings.md`
- **Processed Dataset:** `data/processed/city_analysis.csv`
- **Source Scripts:** `scripts/download_data.py`, `scripts/process_data.py`

## How to Run
1. **View the Dashboard:**
   - Navigate to the `dashboard` folder.
   - Double-click `index.html`. 
   - *Note: No server is required; data is embedded via `data.js`.*

2. **Reproduce Analysis:**
   - Run data download:
     ```bash
     python scripts/download_data.py
     ```
   - Run processing algorithm:
     ```bash
     python scripts/process_data.py
     ```
   - Regenerate dashboard data:
     ```bash
     python scripts/prepare_dashboard.py
     ```

## Visualization Highlights
The dashboard features **7 interactive visualizations**:
1. **Top 10 "Blue Ocean" Cities:** Bar chart of megacities with 0 stores.
2. **Global Opportunity Map:** Scatter plot visualizing geographic distribution.
3. **Population vs. Saturation:** Scatter plot identifying market outliers.
4. **Regional Opportunity Breakdown:** Composition of opportunities by region.
5. **Unserved Population by Country:** Aggregated market gap analysis.
6. **City Size Distribution:** Frequency of opportunities by population tier.
7. **Key Stats Cards:** High-level metrics on market value and city count.

## Technical Details
- **Stack:** HTML5, CSS3 (Glassmorphism), Vanilla JS, Chart.js.
- **Data Pipeline:** Python (Standard Libs) -> JSON -> JS Object.
- **Optimization:** Spatial grid hashing for O(N) geospatial matching.
