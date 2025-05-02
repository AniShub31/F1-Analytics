# F1-Analytics
Formula 1 year-wise dashboard analytics, single pane of glass view to quench your trivia!

![F1 Racing Dashboard](https://github.com/AniShub31/F1-Analytics/blob/main/formula_1-logo-brandlogos.net_.png)

## Overview

This interactive Formula 1 Racing Dashboard provides real-time statistics, race results, and analytics for F1 fans. Built using Streamlit, it visualizes data from the Ergast F1 API to create an engaging experience for both casual and dedicated F1 followers.

## Features

- **Season Overview**: Race calendar, standings, and championship points
- **Driver Standings**: Detailed driver statistics with points visualization
- **Constructor Standings**: Team performance metrics and comparisons
- **Race Results**: Detailed race outcomes with position change analysis
- **Qualifying Results**: Session-by-session qualifying performance data

## How It Works

The dashboard connects to the Ergast F1 API to fetch the latest Formula 1 data. It processes this information and displays it through interactive charts, tables, and visualizations. Users can select specific seasons and races to explore detailed statistics.

Key components:
- Data retrieval from Ergast F1 API
- Data processing and formatting
- Interactive visualizations with Plotly
- User-friendly interface with Streamlit

## Installation Guide

### Prerequisites

No technical knowledge required! Just make sure you have:
- A computer with internet connection
- Python installed (if not, see simple install steps below)

### Step 1: Install Python (if needed)

If you don't have Python installed:

**For Windows:**
1. Go to [python.org](https://www.python.org/downloads/)
2. Click "Download Python" (choose the latest version)
3. Run the installer
4. Make sure to check "Add Python to PATH" during installation
5. Click "Install Now"

**For Mac:**
1. Open Terminal
2. Install Homebrew if not installed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Run: `brew install python`

### Step 2: Download the Dashboard

**Option 1: Simple Download**
1. Click the green "Code" button at the top of this page
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer

**Option 2: Using Git (slightly more technical)**
1. Open Command Prompt (Windows) or Terminal (Mac)
2. Navigate to where you want to save the project: `cd Documents`
3. Run: `git clone https://github.com/yourusername/f1-dashboard.git`

### Step 3: Install Requirements

1. Open Command Prompt (Windows) or Terminal (Mac)
2. Navigate to the folder where you downloaded the dashboard: `cd path/to/f1-dashboard`
3. Run: `pip install -r requirements.txt`

The requirements.txt file contains:
```
streamlit
pandas
numpy
matplotlib
seaborn
requests
plotly
```

### Step 4: Run the Dashboard

1. In your Command Prompt or Terminal, make sure you're in the dashboard folder
2. Run: `streamlit run app.py`
3. Your web browser will automatically open with the dashboard

## Using the Dashboard

1. **Select a Season**: Use the dropdown in the sidebar to choose an F1 season
2. **Select a Race**: Choose a specific Grand Prix from that season
3. **Explore Tabs**: Navigate between different data views using the tabs at the top
4. **Interact with Charts**: Hover over charts for additional information, zoom in/out, or download images

## Troubleshooting

**Dashboard won't start:**
- Make sure all requirements are installed: `pip install -r requirements.txt`
- Check your internet connection (the dashboard needs internet to fetch F1 data)

**Charts not loading:**
- Refresh your browser
- Check your internet connection
- Try selecting a different season/race

**For other issues:**
- Restart the application: Press Ctrl+C in the terminal, then run `streamlit run app.py` again

## Data Source

This dashboard uses the [Ergast F1 API](http://ergast.com/mrd/), which provides historical Formula 1 race data from 1950 to the present day.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ergast Motor Racing Database API
- Streamlit for the interactive framework
- Formula 1 for the exciting sport we all love

---

Enjoy exploring Formula 1 statistics with your new interactive dashboard! No technical expertise required - just your passion for F1 racing.
