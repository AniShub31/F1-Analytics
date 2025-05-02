# Interactive Formula One Dashboard with Streamlit

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Formula 1 Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #E10600;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem !important;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #FFFFFF;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E10600;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">Formula 1 Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Interactive analytics for F1 racing data</p>', unsafe_allow_html=True)

# Functions to fetch data from Ergast API
@st.cache_data(ttl=3600)
def get_seasons():
    response = requests.get('http://ergast.com/api/f1/seasons.json?limit=100')
    data = response.json()
    seasons = [season['season'] for season in data['MRData']['SeasonTable']['Seasons']]
    seasons.sort(reverse=True)
    return seasons

@st.cache_data(ttl=3600)
def get_races(season):
    response = requests.get(f'http://ergast.com/api/f1/{season}.json')
    data = response.json()
    races = data['MRData']['RaceTable']['Races']
    return races

@st.cache_data(ttl=3600)
def get_drivers_standings(season):
    response = requests.get(f'http://ergast.com/api/f1/{season}/driverStandings.json')
    data = response.json()
    if 'StandingsLists' in data['MRData']['StandingsTable'] and len(data['MRData']['StandingsTable']['StandingsLists']) > 0:
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        drivers_data = []
        for driver in standings:
            drivers_data.append({
                'position': int(driver['position']),
                'points': float(driver['points']),
                'wins': int(driver['wins']),
                'driver': f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
                'constructor': driver['Constructors'][0]['name']
            })
        return pd.DataFrame(drivers_data)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_constructor_standings(season):
    response = requests.get(f'http://ergast.com/api/f1/{season}/constructorStandings.json')
    data = response.json()
    if 'StandingsLists' in data['MRData']['StandingsTable'] and len(data['MRData']['StandingsTable']['StandingsLists']) > 0:
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        constructors_data = []
        for constructor in standings:
            constructors_data.append({
                'position': int(constructor['position']),
                'points': float(constructor['points']),
                'wins': int(constructor['wins']),
                'constructor': constructor['Constructor']['name'],
                'nationality': constructor['Constructor']['nationality']
            })
        return pd.DataFrame(constructors_data)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_race_results(season, round_num):
    response = requests.get(f'http://ergast.com/api/f1/{season}/{round_num}/results.json')
    data = response.json()
    if 'Races' in data['MRData']['RaceTable'] and len(data['MRData']['RaceTable']['Races']) > 0:
        results = data['MRData']['RaceTable']['Races'][0]['Results']
        race_data = []
        for result in results:
            position = result.get('position', 'N/A')
            if position == 'N/A' or not position.isdigit():
                position = len(results)  # Default to last if position is not available
            else:
                position = int(position)
                
            points = float(result.get('points', 0))
            driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            team = result['Constructor']['name']
            
            status = result.get('status', 'Unknown')
            
            fastest_lap_rank = 'N/A'
            fastest_lap_time = 'N/A'
            if 'FastestLap' in result:
                fastest_lap_rank = result['FastestLap'].get('rank', 'N/A')
                if 'Time' in result['FastestLap']:
                    fastest_lap_time = result['FastestLap']['Time'].get('time', 'N/A')
            
            grid = result.get('grid', 'N/A')
            if grid != 'N/A':
                grid = int(grid)
                
            race_data.append({
                'position': position,
                'points': points,
                'driver': driver_name,
                'team': team,
                'status': status,
                'grid': grid,
                'fastest_lap_rank': fastest_lap_rank,
                'fastest_lap_time': fastest_lap_time
            })
        return pd.DataFrame(race_data)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_qualifying_results(season, round_num):
    response = requests.get(f'http://ergast.com/api/f1/{season}/{round_num}/qualifying.json')
    data = response.json()
    if 'Races' in data['MRData']['RaceTable'] and len(data['MRData']['RaceTable']['Races']) > 0:
        results = data['MRData']['RaceTable']['Races'][0]['QualifyingResults']
        qualifying_data = []
        for result in results:
            q1_time = result.get('Q1', 'N/A')
            q2_time = result.get('Q2', 'N/A')
            q3_time = result.get('Q3', 'N/A')
            
            qualifying_data.append({
                'position': int(result['position']),
                'driver': f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
                'team': result['Constructor']['name'],
                'Q1': q1_time,
                'Q2': q2_time,
                'Q3': q3_time
            })
        return pd.DataFrame(qualifying_data)
    return pd.DataFrame()

# Create sidebar
with st.sidebar:
    st.image("https://www.formula1.com/etc/designs/fom-website/images/f1_logo.png", width=200)
    st.header("Options")
    
    # Season selection
    seasons = get_seasons()
    selected_season = st.selectbox("Select Season", seasons)
    
    # Get races for selected season
    races = get_races(selected_season)
    race_options = {f"Round {race['round']}: {race['raceName']}": race['round'] for race in races}
    
    # Race selection
    selected_race = st.selectbox("Select Race", list(race_options.keys()))
    selected_round = race_options[selected_race]
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This dashboard uses the Ergast F1 API to display Formula 1 statistics and race results.")
    st.markdown("Data is refreshed hourly.")

# Main content
tabs = st.tabs(["Season Overview", "Driver Standings", "Constructor Standings", "Race Results", "Qualifying Results"])

# Season Overview Tab
with tabs[0]:
    st.header(f"Formula 1 Season {selected_season} Overview")
    
    # Get data
    driver_standings = get_drivers_standings(selected_season)
    constructor_standings = get_constructor_standings(selected_season)
    
    if not driver_standings.empty and not constructor_standings.empty:
        # Season Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Season", selected_season)
        with col2:
            st.metric("Races", len(races))
        with col3:
            st.metric("Top Driver", driver_standings.iloc[0]['driver'] if not driver_standings.empty else "N/A")
        
        # Display Calendar
        st.subheader("Race Calendar")
        calendar_data = []
        for race in races:
            race_date = datetime.strptime(race['date'], '%Y-%m-%d')
            calendar_data.append({
                'Round': int(race['round']),
                'Grand Prix': race['raceName'],
                'Circuit': race['Circuit']['circuitName'],
                'Location': f"{race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}",
                'Date': race_date.strftime('%d %b %Y')
            })
        
        calendar_df = pd.DataFrame(calendar_data)
        st.dataframe(calendar_df, use_container_width=True)
        
        # Upcoming races
        today = datetime.now()
        upcoming_races = [race for race in calendar_data if datetime.strptime(race['Date'], '%d %b %Y') >= today]
        
        if upcoming_races:
            st.subheader("Upcoming Races")
            st.dataframe(pd.DataFrame(upcoming_races[:3]), use_container_width=True)
        
        # Top Drivers and Constructors visualization
        st.subheader("Top Performers")
        col1, col2 = st.columns(2)
        
        with col1:
            top_drivers = driver_standings.head(5)
            fig = px.bar(
                top_drivers, 
                x='driver', 
                y='points',
                color='constructor',
                title="Top 5 Drivers",
                labels={'driver': 'Driver', 'points': 'Points', 'constructor': 'Team'},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            top_constructors = constructor_standings.head(5)
            fig = px.bar(
                top_constructors, 
                x='constructor', 
                y='points',
                color='constructor',
                title="Top 5 Constructors",
                labels={'constructor': 'Team', 'points': 'Points'},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this season yet.")

# Driver Standings Tab
with tabs[1]:
    st.header(f"Driver Standings - {selected_season}")
    
    driver_standings = get_drivers_standings(selected_season)
    
    if not driver_standings.empty:
        # Points visualization
        fig = px.bar(
            driver_standings,
            x='driver',
            y='points',
            color='constructor',
            title=f"{selected_season} Driver Championship Points",
            labels={'driver': 'Driver', 'points': 'Points', 'constructor': 'Team'},
            height=500
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Driver standings table with styling
        st.subheader("Full Driver Standings")
        
        # Use colormap for positions
        def highlight_position(val):
            color = 'white'
            if val == 1:
                color = '#FFDF00'  # Gold
            elif val == 2:
                color = '#C0C0C0'  # Silver
            elif val == 3:
                color = '#CD7F32'  # Bronze
            return f'background-color: {color}'
        
        styled_df = driver_standings.style.applymap(
            highlight_position, 
            subset=['position']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Wins distribution
        st.subheader("Race Wins Distribution")
        wins_df = driver_standings[driver_standings['wins'] > 0].sort_values('wins', ascending=False)
        
        if not wins_df.empty:
            fig = px.pie(
                wins_df,
                values='wins',
                names='driver',
                title=f"{selected_season} Race Wins Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No wins data available yet.")
    else:
        st.info("No driver standings data available for this season yet.")

# Constructor Standings Tab
with tabs[2]:
    st.header(f"Constructor Standings - {selected_season}")
    
    constructor_standings = get_constructor_standings(selected_season)
    
    if not constructor_standings.empty:
        # Points visualization
        fig = px.bar(
            constructor_standings,
            x='constructor',
            y='points',
            color='constructor',
            title=f"{selected_season} Constructor Championship Points",
            labels={'constructor': 'Team', 'points': 'Points'},
            height=500
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Constructor standings table with styling
        st.subheader("Full Constructor Standings")
        
        # Use colormap for positions
        def highlight_position(val):
            color = 'white'
            if val == 1:
                color = '#FFDF00'  # Gold
            elif val == 2:
                color = '#C0C0C0'  # Silver
            elif val == 3:
                color = '#CD7F32'  # Bronze
            return f'background-color: {color}'
        
        styled_df = constructor_standings.style.applymap(
            highlight_position, 
            subset=['position']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Nationality distribution
        st.subheader("Team Nationality Distribution")
        
        nationality_counts = constructor_standings['nationality'].value_counts().reset_index()
        nationality_counts.columns = ['nationality', 'count']
        
        fig = px.pie(
            nationality_counts,
            values='count',
            names='nationality',
            title="Team Nationality Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No constructor standings data available for this season yet.")

# Race Results Tab
with tabs[3]:
    st.header(f"Race Results - {selected_race}")
    
    race_results = get_race_results(selected_season, selected_round)
    
    if not race_results.empty:
        # Points visualization
        fig = px.bar(
            race_results,
            x='driver',
            y='points',
            color='team',
            title=f"Points Scored - {selected_race}",
            labels={'driver': 'Driver', 'points': 'Points', 'team': 'Team'},
            height=500
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Grid vs Finish position
        st.subheader("Grid vs. Finish Position")
        
        # Filter out rows where grid or position is N/A
        grid_finish_df = race_results[race_results['grid'] != 'N/A'].copy()
        
        if not grid_finish_df.empty:
            grid_finish_df['position_change'] = grid_finish_df['grid'] - grid_finish_df['position']
            
            # Color mapping for position changes
            def position_color(val):
                if val > 0:  # Gained positions
                    return 'green'
                elif val < 0:  # Lost positions
                    return 'red'
                else:  # No change
                    return 'gray'
            
            grid_finish_df['color'] = grid_finish_df['position_change'].apply(position_color)
            
            fig = px.scatter(
                grid_finish_df,
                x='grid',
                y='position',
                color='color',
                size=abs(grid_finish_df['position_change']) + 5,  # Make the size reflect magnitude of change
                text='driver',
                labels={'grid': 'Grid Position', 'position': 'Finish Position', 'team': 'Team'},
                title=f"Grid vs. Finish Position - {selected_race}",
                color_discrete_map={'green': 'green', 'red': 'red', 'gray': 'gray'}
            )
            
            # Add diagonal line representing no position change
            fig.add_trace(
                go.Scatter(
                    x=[1, grid_finish_df['grid'].max()],
                    y=[1, grid_finish_df['grid'].max()],
                    mode='lines',
                    line=dict(color='black', dash='dash'),
                    name='No Position Change'
                )
            )
            
            # Reverse y-axis so that position 1 is at the top
            fig.update_layout(
                yaxis={'autorange': 'reversed'},
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add annotations to explain the chart
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("🟢 **Above line**: Gained positions")
            with col2:
                st.markdown("⚫ **On line**: No change")
            with col3:
                st.markdown("🔴 **Below line**: Lost positions")
        
        # Full race results table
        st.subheader("Full Race Results")
        
        # Format the results table
        display_columns = ['position', 'driver', 'team', 'grid', 'status', 'points']
        
        if 'fastest_lap_time' in race_results.columns:
            # Add fastest lap info if available
            fastest_lap_data = race_results[race_results['fastest_lap_rank'] == '1']
            if not fastest_lap_data.empty:
                fastest_driver = fastest_lap_data.iloc[0]['driver']
                fastest_time = fastest_lap_data.iloc[0]['fastest_lap_time']
                
                st.markdown(f"**Fastest Lap**: {fastest_driver} - {fastest_time}")
            
        # Display the data with styling
        def highlight_position(val):
            color = 'white'
            if val == 1:
                color = '#FFDF00'  # Gold
            elif val == 2:
                color = '#C0C0C0'  # Silver
            elif val == 3:
                color = '#CD7F32'  # Bronze
            return f'background-color: {color}'
        
        styled_df = race_results[display_columns].style.applymap(
            highlight_position, 
            subset=['position']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Status analysis
        st.subheader("Race Finishing Status")
        
        status_counts = race_results['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.pie(
            status_counts,
            values='count',
            names='status',
            title="Race Finishing Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No race results data available for this selection yet.")

# Qualifying Results Tab
with tabs[4]:
    st.header(f"Qualifying Results - {selected_race}")
    
    qualifying_results = get_qualifying_results(selected_season, selected_round)
    
    if not qualifying_results.empty:
        # Visualization of qualifying positions
        fig = px.bar(
            qualifying_results,
            x='position',
            y='driver',
            color='team',
            title=f"Qualifying Results - {selected_race}",
            labels={'position': 'Position', 'driver': 'Driver', 'team': 'Team'},
            orientation='h',
            height=600
        )
        
        # Reverse y-axis to have P1 at the top
        fig.update_layout(yaxis={'autorange': 'reversed'})
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Full qualifying results table
        st.subheader("Full Qualifying Results")
        
        # Display the data with styling
        def highlight_position(val):
            color = 'white'
            if val == 1:
                color = '#FFDF00'  # Gold
            elif val == 2:
                color = '#C0C0C0'  # Silver
            elif val == 3:
                color = '#CD7F32'  # Bronze
            return f'background-color: {color}'
        
        styled_df = qualifying_results.style.applymap(
            highlight_position, 
            subset=['position']
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Q1, Q2, Q3 progression analysis
        st.subheader("Qualifying Session Progression")
        
        # Count how many drivers participated in each session
        q1_count = qualifying_results['Q1'].count()
        q2_count = qualifying_results['Q2'].count()
        q3_count = qualifying_results['Q3'].count()
        
        progression_data = pd.DataFrame({
            'Session': ['Q1', 'Q2', 'Q3'],
            'Drivers': [q1_count, q2_count, q3_count]
        })
        
        fig = px.bar(
            progression_data,
            x='Session',
            y='Drivers',
            title="Drivers per Qualifying Session",
            color='Session',
            color_discrete_sequence=['#E10600', '#1E1E1E', '#FFFFFF']
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No qualifying results data available for this selection yet.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Formula 1 Dashboard | Data from Ergast API | Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)
