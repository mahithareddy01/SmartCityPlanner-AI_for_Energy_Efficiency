import streamlit as st
import sys
import os
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from db import database as db
from modules.realtime_monitor import monitor_city
from modules.predictive import forecast_energy
from modules.sustainability import energy_efficiency_score
from modules.planner_assist import suggest_improvements

# Page configuration
st.set_page_config(
    page_title="Smart City Energy Planner",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #667eea;
        animation: slideIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid #e0e6ff;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .success-animation {
        animation: success 0.6s ease-out;
    }
    
    @keyframes success {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content .sidebar-collapse-control {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header with animation
    st.markdown('<h1 class="main-header">🏙️ Smart City Energy Planner</h1>', unsafe_allow_html=True)
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; color: white;'>
            <h2 style='color: white; margin-bottom: 2rem;'>Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        app_mode = st.selectbox(
            "Choose Module",
            ["🏠 Dashboard", "🏙️ City Management", "📊 Real-Time Monitoring", 
             "🔮 Predictive Analytics", "🌱 Sustainability", "💡 Planner Assistance", "📈 Analytics"],
            key="nav_select"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style='color: white; padding: 1rem;'>
            <h4>Quick Stats</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats in sidebar
        try:
            cities = db.get_cities()
            sensors = db.get_sensors()
            st.metric("Cities", len(cities))
            st.metric("Sensors", len(sensors))
        except:
            st.info("Connect to database to see stats")

    # Route to selected page
    if "🏠 Dashboard" in app_mode:
        show_dashboard()
    elif "🏙️ City Management" in app_mode:
        show_city_management()
    elif "📊 Real-Time Monitoring" in app_mode:
        show_realtime_monitoring()
    elif "🔮 Predictive Analytics" in app_mode:
        show_predictive_analytics()
    elif "🌱 Sustainability" in app_mode:
        show_sustainability()
    elif "💡 Planner Assistance" in app_mode:
        show_planner_assistance()
    elif "📈 Analytics" in app_mode:
        show_analytics()

def show_dashboard():
    st.markdown('<div class="pulse" style="text-align: center; margin-bottom: 2rem;">'
                '<h2>🌍 Smart City Energy Management Dashboard</h2>'
                '</div>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            cities = db.get_cities()
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏙️ Cities</h3>
                <h1 style="color: #667eea; font-size: 2.5rem;">{len(cities)}</h1>
                <p>Managed Cities</p>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Database connection required")
    
    with col2:
        try:
            sensors = db.get_sensors()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📡 Sensors</h3>
                <h1 style="color: #667eea; font-size: 2.5rem;">{len(sensors)}</h1>
                <p>Active Sensors</p>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Database connection required")
    
    with col3:
        try:
            usage_data = db.get_energy_usage()
            total_consumption = sum(u['consumption'] for u in usage_data) if usage_data else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Energy</h3>
                <h1 style="color: #667eea; font-size: 2.5rem;">{total_consumption:,.0f}</h1>
                <p>Total Consumption</p>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Database connection required")
    
    with col4:
        try:
            efficiency_scores = []
            for city in cities:
                score = energy_efficiency_score(city['cityid'])
                efficiency_scores.append(score)
            avg_efficiency = np.mean(efficiency_scores) if efficiency_scores else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌱 Efficiency</h3>
                <h1 style="color: #667eea; font-size: 2.5rem;">{avg_efficiency:.1f}%</h1>
                <p>Average Score</p>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Calculate efficiency scores")
    
    # Features Grid
    st.markdown("## 🚀 Key Features")
    features_col1, features_col2, features_col3 = st.columns(3)
    
    with features_col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Real-Time Monitoring</h3>
            <p>Live energy consumption tracking across all city sectors with instant alerts and visualization.</p>
            <div style="color: #667eea; font-size: 2rem;">🔍</div>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔮 AI Predictions</h3>
            <p>Machine learning powered energy forecasting for proactive resource planning and allocation.</p>
            <div style="color: #667eea; font-size: 2rem;">🤖</div>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Smart Insights</h3>
            <p>Actionable recommendations for energy optimization and sustainable urban development.</p>
            <div style="color: #667eea; font-size: 2rem;">💎</div>
        </div>
        """, unsafe_allow_html=True)

def show_city_management():
    st.markdown('<h2 class="success-animation">🏙️ City Management Portal</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏙️ Cities", "📡 Sensors", "⚡ Energy Data", "👥 Planners"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Add New City")
            with st.form("add_city_form"):
                name = st.text_input("City Name", placeholder="Enter city name")
                population = st.number_input("Population", min_value=0, value=100000)
                area = st.number_input("Area (km²)", min_value=0.0, value=150.5)
                
                if st.form_submit_button("🚀 Add City", use_container_width=True):
                    if name:
                        with st.spinner("Adding city..."):
                            time.sleep(1)  # Animation delay
                            city = db.add_city(name, population, area)
                            st.success(f"✅ Successfully added {city['name']}!")
                            st.balloons()
        
        with col2:
            st.subheader("City Directory")
            cities = db.get_cities()
            if cities:
                city_data = []
                for city in cities:
                    city_data.append({
                        'ID': city['cityid'],
                        'Name': city['name'],
                        'Population': f"{city['population']:,}",
                        'Area': f"{city['area']} km²"
                    })
                st.dataframe(city_data, use_container_width=True)
            else:
                st.info("No cities found. Add your first city!")
    
    with tab2:
        # Similar enhanced layout for sensors
        st.subheader("Sensor Management")
        # Add sensor management UI here

def show_realtime_monitoring():
    st.markdown('<h2 class="success-animation">📊 Real-Time City Monitoring</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Monitor City")
        city_id = st.number_input("Enter City ID", min_value=1, value=1, key="monitor_city")
        
        if st.button("🔍 Start Monitoring", use_container_width=True):
            with st.spinner("Connecting to city sensors..."):
                time.sleep(1.5)  # Simulate loading
                data = monitor_city(city_id)
                
                # Animated success
                st.markdown('<div class="success-animation">', unsafe_allow_html=True)
                st.success("✅ Real-time data fetched successfully!")
                
                # Display metrics with animations
                if data:
                    st.subheader("Live Metrics")
                    
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        consumption = data['latest_energy_usage']['consumption']
                        st.metric("Current Consumption", f"{consumption:,.2f} units", delta="Live")
                    
                    with metric_col2:
                        sensor_count = len(data['sensors'])
                        st.metric("Active Sensors", sensor_count, delta="Online")
                    
                    # Real-time chart simulation
                    st.subheader("Energy Consumption Trend")
                    fig = create_realtime_chart()
                    st.plotly_chart(fig, use_container_width=True)

def create_realtime_chart():
    """Create an animated real-time chart"""
    # Simulate real-time data
    time_points = pd.date_range(start='2024-01-01', periods=24, freq='H')
    consumption = np.random.normal(1000, 200, 24).cumsum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_points, 
        y=consumption,
        mode='lines+markers',
        line=dict(color='#667eea', width=4),
        marker=dict(size=8, color='#764ba2'),
        name='Energy Consumption'
    ))
    
    fig.update_layout(
        title="Real-Time Energy Consumption",
        xaxis_title="Time",
        yaxis_title="Consumption (units)",
        template="plotly_white",
        hovermode='x unified',
        height=400
    )
    
    return fig

def show_predictive_analytics():
    st.markdown('<h2 class="success-animation">🔮 Predictive Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Energy Forecasting")
        city_id = st.number_input("City ID", min_value=1, value=1, key="predict_city")
        days = st.slider("Forecast Period (days)", 1, 30, 7)
        
        if st.button("🎯 Generate Forecast", use_container_width=True):
            with st.spinner("AI is analyzing patterns..."):
                time.sleep(2)
                prediction = forecast_energy(city_id)
                
                # Animated metric display
                st.markdown("""
                <div class="success-animation">
                """, unsafe_allow_html=True)
                
                st.metric(
                    "Next Day Prediction", 
                    f"{prediction:,.2f} units",
                    delta="AI Forecast",
                    delta_color="normal"
                )
    
    with col2:
        # Forecast visualization
        st.subheader("Forecast Analysis")
        fig = create_forecast_chart()
        st.plotly_chart(fig, use_container_width=True)

def create_forecast_chart():
    """Create an animated forecast chart"""
    # Sample forecast data
    days = list(range(1, 8))
    actual = [950, 1020, 980, 1100, 1050, 1075, 1030]
    predicted = [None] * 6 + [1080]  # Only show prediction for last day
    
    fig = go.Figure()
    
    # Actual data
    fig.add_trace(go.Scatter(
        x=days[:-1], y=actual[:-1],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#667eea', width=4)
    ))
    
    # Prediction
    fig.add_trace(go.Scatter(
        x=[days[-2], days[-1]], y=[actual[-2], predicted[-1]],
        mode='lines+markers',
        name='Predicted',
        line=dict(color='#ff6b6b', width=4, dash='dash')
    ))
    
    fig.update_layout(
        title="7-Day Energy Forecast",
        xaxis_title="Days",
        yaxis_title="Energy Consumption",
        template="plotly_white",
        height=400
    )
    
    return fig

def show_sustainability():
    st.markdown('<h2 class="success-animation">🌱 Sustainability Analytics</h2>', unsafe_allow_html=True)
    
    city_id = st.number_input("City ID for Analysis", min_value=1, value=1, key="sustainability_city")
    
    if st.button("📊 Calculate Efficiency", use_container_width=True):
        with st.spinner("Analyzing sustainability metrics..."):
            time.sleep(1.5)
            score = energy_efficiency_score(city_id)
            
            # Animated gauge chart
            fig = create_efficiency_gauge(score)
            st.plotly_chart(fig, use_container_width=True)
            
            # Efficiency interpretation
            if score >= 90:
                st.success("🎉 Excellent! City is highly energy efficient")
            elif score >= 70:
                st.warning("⚠️ Good efficiency with room for improvement")
            else:
                st.error("🚨 Needs attention - implement energy optimization strategies")

def create_efficiency_gauge(score):
    """Create an animated gauge chart for efficiency score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Energy Efficiency Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    return fig

def show_planner_assistance():
    st.markdown('<h2 class="success-animation">💡 AI Planner Assistance</h2>', unsafe_allow_html=True)
    
    city_id = st.number_input("City ID for Recommendations", min_value=1, value=1, key="planner_city")
    
    if st.button("🤖 Get Smart Recommendations", use_container_width=True):
        with st.spinner("AI is generating personalized recommendations..."):
            time.sleep(2)
            advice = suggest_improvements(city_id)
            
            # Enhanced advice display with animations
            st.markdown("""
            <div class="feature-card success-animation">
            """, unsafe_allow_html=True)
            st.success("🎯 AI Recommendations Generated!")
            
            # Parse and display advice beautifully
            lines = advice.split('\n')
            for line in lines:
                if 'City ID' in line:
                    st.info(f"**{line}**")
                elif 'Predicted' in line:
                    st.metric("Energy Forecast", line.split(": ")[1])
                elif 'Efficiency Score' in line:
                    score = float(line.split(": ")[1].replace('%', ''))
                    st.metric("Efficiency Score", f"{score}%")
                elif 'Recommendation' in line:
                    st.success(f"💡 **{line}**")

def show_analytics():
    st.markdown('<h2 class="success-animation">📈 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    # Sample analytics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("City Performance")
        fig = create_performance_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Energy Distribution")
        fig = create_distribution_chart()
        st.plotly_chart(fig, use_container_width=True)

def create_performance_chart():
    """Create performance comparison chart"""
    cities = ['City A', 'City B', 'City C', 'City D']
    efficiency = [85, 92, 78, 88]
    
    fig = px.bar(
        x=cities, y=efficiency,
        title="City Efficiency Comparison",
        color=efficiency,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=400)
    return fig

def create_distribution_chart():
    """Create energy distribution pie chart"""
    sectors = ['Residential', 'Commercial', 'Industrial', 'Public']
    consumption = [40, 25, 20, 15]
    
    fig = px.pie(
        values=consumption, names=sectors,
        title="Energy Consumption by Sector",
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

if __name__ == "__main__":
    main()
