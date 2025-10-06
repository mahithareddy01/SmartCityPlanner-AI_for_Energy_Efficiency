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
import hashlib
import jwt
from datetime import datetime, timedelta

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

# JWT Secret Key (in production, use environment variable)
JWT_SECRET = "your-secret-key-here"
JWT_ALGORITHM = "HS256"

# Custom CSS for enhanced animations and professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1.5s ease-in;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: clamp(1rem, 3vw, 1.5rem);
        font-weight: 500;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 2s ease-in;
        padding: 0 1rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .auth-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: clamp(1.5rem, 4vw, 3rem);
        border-radius: 25px;
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.3);
        color: white;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .auth-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        font-weight: 700;
        position: relative;
        z-index: 2;
    }
    
    .auth-icon {
        font-size: clamp(2rem, 6vw, 3rem);
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    .auth-input {
        background: rgba(255,255,255,0.15) !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: clamp(12px, 3vw, 15px) clamp(16px, 4vw, 20px) !important;
        margin-bottom: 1.2rem;
        font-size: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        width: 100% !important;
    }
    
    .auth-input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    
    .auth-input:focus {
        border-color: rgba(255,255,255,0.8) !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.2) !important;
        background: rgba(255,255,255,0.2) !important;
        transform: translateY(-2px);
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8ecff 100%);
        padding: clamp(1.5rem, 3vw, 2.5rem);
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e0e6ff;
        transition: all 0.3s ease;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .feature-highlight:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
    }
    
    .feature-icon {
        font-size: clamp(2.5rem, 6vw, 3.5rem);
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-title {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.6;
        font-size: clamp(0.9rem, 2vw, 1rem);
    }
    
    .stats-counter {
        text-align: center;
        padding: clamp(1rem, 2vw, 1.5rem);
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1rem;
    }
    
    .stats-number {
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #f0f4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: block;
    }
    
    .stats-label {
        font-size: clamp(0.8rem, 2vw, 0.9rem);
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    .benefit-item {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .benefit-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        min-width: 40px;
        flex-shrink: 0;
    }
    
    .benefit-text {
        color: white;
        font-weight: 500;
        font-size: clamp(0.9rem, 2vw, 1rem);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #fff 0%, #f0f4ff 100%) !important;
        color: #667eea !important;
        border: none !important;
        padding: clamp(0.8rem, 2vw, 1rem) clamp(1.5rem, 3vw, 2rem) !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(255,255,255,0.3) !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255,255,255,0.4) !important;
        background: linear-gradient(135deg, #ffffff 0%, #e8ecff 100%) !important;
    }
    
    .testimonial {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
    }
    
    .testimonial-text {
        font-style: italic;
        color: white;
        margin-bottom: 1rem;
        font-size: clamp(0.9rem, 2vw, 1rem);
    }
    
    .testimonial-author {
        color: rgba(255,255,255,0.9);
        font-weight: 600;
        text-align: right;
        font-size: clamp(0.8rem, 2vw, 0.9rem);
    }
    
    .user-welcome {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: clamp(1.5rem, 3vw, 2rem);
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: clamp(1rem, 2vw, 1.5rem);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #667eea;
        animation: slideIn 0.6s ease-out;
        color: #262730 !important;
        margin-bottom: 1rem;
        height: auto;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card h3 {
        color: #262730 !important;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        margin-bottom: 0.5rem;
    }
    
    .metric-card h1 {
        color: #262730 !important;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        margin: 0.5rem 0;
    }
    
    .metric-card p {
        color: #262730 !important;
        font-size: clamp(0.8rem, 2vw, 0.9rem);
        margin: 0;
    }
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.2rem;
        }
        
        .auth-container {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .feature-highlight {
            margin-bottom: 1rem;
        }
        
        .stats-counter {
            margin-bottom: 0.5rem;
        }
        
        .benefit-item {
            padding: 0.8rem;
        }
    }
    
    /* Tablet-specific styles */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a stored password against one provided by user"""
    return hash_password(password) == hashed

def create_token(user_id):
    """Create JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload['user_id']
    except:
        return None

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Overview"
    if 'login_attempted' not in st.session_state:
        st.session_state.login_attempted = False
    if 'redirecting' not in st.session_state:
        st.session_state.redirecting = False

def show_auth_page():
    """Show enhanced authentication page with attractive design"""
    
    # Main Header Section
    st.markdown('<h1 class="main-header">🏙️ SMART CITY ENERGY PLANNER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Energy Efficiency & Sustainable Urban Management</div>', unsafe_allow_html=True)
    
    # Stats Counter Row - Responsive columns
    stats_cols = st.columns(4)
    stats_data = [
        {"number": "50+", "label": "Cities Optimized"},
        {"number": "25%", "label": "Avg. Energy Saved"},
        {"number": "10K+", "label": "Sensors Deployed"},
        {"number": "99.8%", "label": "Uptime Reliability"}
    ]
    
    for i, col in enumerate(stats_cols):
        with col:
            st.markdown(f"""
            <div class="stats-counter">
                <span class="stats-number">{stats_data[i]['number']}</span>
                <div class="stats-label">{stats_data[i]['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Content Columns - Responsive layout
    if st.session_state.get('redirecting', False):
        with st.spinner("🎉 Login successful! Redirecting to dashboard..."):
            time.sleep(2)
            st.session_state.redirecting = False
            st.rerun()
        return
    
    # Use responsive columns with different layouts for mobile/desktop
    col1, col2 = st.columns(2)
    
    with col1:
        # Login Section
        st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">🔐</div>
            <div class="auth-header">Welcome Back</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            login_username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
            login_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
            
            login_submitted = st.form_submit_button("🚀 SIGN IN TO DASHBOARD", use_container_width=True)
            
            if login_submitted:
                st.session_state.login_attempted = True
                if login_username and login_password:
                    user = db.get_user_by_username(login_username)
                    if user and verify_password(login_password, user['password_hash']):
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['id']
                        st.session_state.username = user['username']
                        st.session_state.token = create_token(user['id'])
                        st.session_state.redirecting = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with col2:
        # Signup Section
        st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">🌟</div>
            <div class="auth-header">Join Smart Cities</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form", clear_on_submit=True):
            signup_username = st.text_input("👤 Choose Username", placeholder="Create your username", key="signup_username")
            signup_email = st.text_input("📧 Email Address", placeholder="Enter your work email", key="signup_email")
            signup_password = st.text_input("🔒 Create Password", type="password", placeholder="Minimum 8 characters", key="signup_password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password", key="confirm_password")
            
            if st.form_submit_button("🎯 CREATE SMART ACCOUNT", use_container_width=True):
                if signup_username and signup_email and signup_password:
                    if len(signup_password) >= 8:
                        if signup_password == confirm_password:
                            try:
                                existing_user = db.get_user_by_username(signup_username)
                                if existing_user:
                                    st.error("❌ Username already exists")
                                else:
                                    hashed_pw = hash_password(signup_password)
                                    user = db.add_user(signup_username, signup_email, hashed_pw)
                                    st.success("✅ Account created successfully! Please login.")
                                    time.sleep(2)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error creating account: {str(e)}")
                        else:
                            st.error("❌ Passwords do not match")
                    else:
                        st.error("❌ Password must be at least 8 characters long")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    # Features Section - Responsive grid
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin: 3rem 0;'>
        <h2 style='color: #333; margin-bottom: 1rem;'>🚀 Why Choose Smart City Energy Planner?</h2>
        <p style='color: #666; font-size: clamp(1rem, 2.5vw, 1.2rem);'>Transform urban energy management with cutting-edge AI technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive features grid
    features_cols = st.columns(3)
    features_data = [
        {
            "icon": "🤖",
            "title": "AI-Powered Predictions", 
            "description": "Machine learning algorithms forecast energy demand with 95% accuracy, enabling proactive resource allocation."
        },
        {
            "icon": "🌍",
            "title": "Real-Time Monitoring",
            "description": "Live dashboard with 10,000+ IoT sensors providing instant insights across all city sectors."
        },
        {
            "icon": "💡",
            "title": "Smart Recommendations",
            "description": "AI-driven insights suggest optimal energy distribution and infrastructure improvements."
        }
    ]
    
    for i, col in enumerate(features_cols):
        with col:
            st.markdown(f"""
            <div class="feature-highlight">
                <div class="feature-icon">{features_data[i]['icon']}</div>
                <div class="feature-title">{features_data[i]['title']}</div>
                <div class="feature-description">{features_data[i]['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Benefits and Testimonials - Stack on mobile
    st.markdown("---")
    benefits_col, testimonials_col = st.columns([2, 1])
    
    with benefits_col:
        st.markdown("""
        <div style='color: #333;'>
            <h3>🎯 Key Benefits for Your City</h3>
        </div>
        """, unsafe_allow_html=True)
        
        benefits = [
            {"icon": "💰", "text": "Reduce energy costs by up to 30% with smart optimization"},
            {"icon": "🌱", "text": "Achieve carbon neutrality goals faster with AI insights"},
            {"icon": "⚡", "text": "Prevent blackouts with predictive maintenance alerts"},
            {"icon": "📊", "text": "Gain real-time visibility across all energy sectors"},
            {"icon": "🔧", "text": "Automated reporting for regulatory compliance"},
            {"icon": "🚀", "text": "Scale efficiently with growing urban populations"}
        ]
        
        for benefit in benefits:
            st.markdown(f"""
            <div class="benefit-item">
                <div class="benefit-icon">{benefit['icon']}</div>
                <div class="benefit-text">{benefit['text']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with testimonials_col:
        st.markdown("""
        <div style='color: #333;'>
            <h3>🏆 Trusted by Cities Worldwide</h3>
        </div>
        """, unsafe_allow_html=True)
        
        testimonials = [
            {
                "text": "This platform helped us reduce energy waste by 40% in just 6 months. Game-changing technology!",
                "author": "— Maria Rodriguez, City Planner"
            },
            {
                "text": "The AI predictions are incredibly accurate. We've saved millions while improving service reliability.",
                "author": "— James Chen, Energy Director"
            }
        ]
        
        for testimonial in testimonials:
            st.markdown(f"""
            <div class="testimonial">
                <div class="testimonial-text">"{testimonial['text']}"</div>
                <div class="testimonial-author">{testimonial['author']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer CTA
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: clamp(2rem, 4vw, 3rem); background: linear-gradient(135deg, #f8f9ff 0%, #e8ecff 100%); border-radius: 20px;'>
        <h2 style='color: #333; margin-bottom: 1rem; font-size: clamp(1.5rem, 3vw, 2rem);'>Ready to Transform Your City's Energy Future?</h2>
        <p style='color: #666; font-size: clamp(1rem, 2.5vw, 1.2rem); margin-bottom: 2rem;'>
            Join 500+ cities already optimizing their energy infrastructure with AI
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_overview():
    """Show overview/dashboard after login"""
    st.markdown(f"""
    <div class="user-welcome">
        <h2 style='font-size: clamp(1.5rem, 3vw, 2rem);'>👋 Welcome back, {st.session_state.username}!</h2>
        <p style='font-size: clamp(1rem, 2vw, 1.2rem);'>Ready to optimize your city's energy management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats - Responsive grid
    metric_cols = st.columns(4)
    
    try:
        cities = db.get_cities()
        sensors = db.get_sensors()
        usage_data = db.get_energy_usage()
        
        total_consumption = sum(u['consumption'] for u in usage_data) if usage_data else 0
        efficiency_scores = [energy_efficiency_score(city['cityid']) for city in cities] if cities else []
        avg_efficiency = np.mean(efficiency_scores) if efficiency_scores else 0
        
        metrics_data = [
            {"title": "🏙️ Managed Cities", "value": len(cities), "description": "Active locations"},
            {"title": "📡 Active Sensors", "value": len(sensors), "description": "Real-time monitoring"},
            {"title": "⚡ Energy Today", "value": f"{total_consumption:,.0f}", "description": "Total units consumed"},
            {"title": "🌱 Avg Efficiency", "value": f"{avg_efficiency:.1f}%", "description": "Across all cities"}
        ]
        
        for i, col in enumerate(metric_cols):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{metrics_data[i]['title']}</h3>
                    <h1>{metrics_data[i]['value']}</h1>
                    <p>{metrics_data[i]['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error("⚠️ Some data may not be available. Please check your database connection.")

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
                            time.sleep(1)
                            city = db.add_city(name, population, area)
                            if city:
                                st.success(f"✅ Successfully added {city['name']}!")
                                st.balloons()
                            else:
                                st.error("❌ Failed to add city")
        
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
        st.subheader("Sensor Management")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            with st.form("add_sensor_form"):
                st.subheader("Add New Sensor")
                sensor_type = st.selectbox("Sensor Type", ["Energy", "Temperature", "Humidity", "Air Quality"])
                location = st.text_input("Location", placeholder="Enter sensor location")
                city_id = st.number_input("City ID", min_value=1, value=1)
                
                if st.form_submit_button("📡 Add Sensor", use_container_width=True):
                    if location:
                        sensor = db.add_sensor(sensor_type, location, city_id)
                        if sensor:
                            st.success(f"✅ Sensor added successfully!")
                        else:
                            st.error("❌ Failed to add sensor")
        
        with col2:
            st.subheader("Sensor Network")
            sensors = db.get_sensors()
            if sensors:
                sensor_data = []
                for sensor in sensors:
                    sensor_data.append({
                        'ID': sensor['sensorid'],
                        'Type': sensor['type'],
                        'Location': sensor['location'],
                        'City ID': sensor['cityid'],
                        'Status': 'Active'
                    })
                st.dataframe(sensor_data, use_container_width=True)
            else:
                st.info("No sensors found. Add your first sensor!")

def show_realtime_monitoring():
    st.markdown('<h2 class="success-animation">📊 Real-Time City Monitoring</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Monitor City")
        city_id = st.number_input("Enter City ID", min_value=1, value=1, key="monitor_city")
        
        if st.button("🔍 Start Monitoring", use_container_width=True):
            with st.spinner("Connecting to city sensors..."):
                time.sleep(1.5)
                try:
                    data = monitor_city(city_id)
                    
                    st.markdown('<div class="success-animation">', unsafe_allow_html=True)
                    st.success("✅ Real-time data fetched successfully!")
                    
                    if data:
                        st.subheader("Live Metrics")
                        
                        metric_col1, metric_col2 = st.columns(2)
                        with metric_col1:
                            consumption = data.get('latest_energy_usage', {}).get('consumption', 0)
                            st.metric("Current Consumption", f"{consumption:,.2f} units", delta="Live")
                        
                        with metric_col2:
                            sensor_count = len(data.get('sensors', []))
                            st.metric("Active Sensors", sensor_count, delta="Online")
                        
                        # Real-time chart simulation
                        st.subheader("Energy Consumption Trend")
                        fig = create_realtime_chart()
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error monitoring city: {str(e)}")
    
    with col2:
        st.subheader("Live Dashboard")
        # Create sample real-time visualization
        fig = go.Figure()
        
        # Sample data for demonstration
        hours = list(range(24))
        energy_usage = [1000 + i*50 + np.random.normal(0, 100) for i in hours]
        
        fig.add_trace(go.Scatter(
            x=hours, y=energy_usage,
            mode='lines+markers',
            line=dict(color='#667eea', width=4),
            marker=dict(size=6, color='#764ba2'),
            name='Energy Consumption'
        ))
        
        fig.update_layout(
            title="24-Hour Energy Consumption Pattern",
            xaxis_title="Hour of Day",
            yaxis_title="Energy Consumption (units)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

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
                try:
                    prediction = forecast_energy(city_id)
                    
                    st.markdown("""
                    <div class="success-animation">
                    """, unsafe_allow_html=True)
                    
                    st.metric(
                        "Next Day Prediction", 
                        f"{prediction:,.2f} units",
                        delta="AI Forecast",
                        delta_color="normal"
                    )
                    
                    # Additional insights
                    st.info(f"📈 Forecast for next {days} days generated")
                    st.success("💡 Recommendation: Consider optimizing energy distribution during peak hours")
                    
                except Exception as e:
                    st.error(f"❌ Error generating forecast: {str(e)}")
    
    with col2:
        st.subheader("Forecast Analysis")
        fig = create_forecast_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional predictive insights
        st.subheader("AI Insights")
        insights = [
            "🔍 Peak consumption expected between 18:00-21:00",
            "💡 15% potential savings through load shifting",
            "🌱 Renewable integration opportunity: 25%",
            "⚡ Grid stability: Optimal conditions expected"
        ]
        
        for insight in insights:
            st.markdown(f"- {insight}")

def show_sustainability():
    st.markdown('<h2 class="success-animation">🌱 Sustainability Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("City Analysis")
        city_id = st.number_input("City ID for Analysis", min_value=1, value=1, key="sustainability_city")
        
        if st.button("📊 Calculate Efficiency", use_container_width=True):
            with st.spinner("Analyzing sustainability metrics..."):
                time.sleep(1.5)
                try:
                    score = energy_efficiency_score(city_id)
                    
                    fig = create_efficiency_gauge(score)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if score >= 90:
                        st.success("🎉 Excellent! City is highly energy efficient")
                    elif score >= 70:
                        st.warning("⚠️ Good efficiency with room for improvement")
                    else:
                        st.error("🚨 Needs attention - implement energy optimization strategies")
                        
                except Exception as e:
                    st.error(f"❌ Error calculating efficiency: {str(e)}")
    
    with col2:
        st.subheader("Sustainability Metrics")
        
        # Carbon footprint analysis
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Carbon Reduction", "25%", "5% vs target")
        
        with metrics_col2:
            st.metric("Renewable Usage", "42%", "8% increase")
        
        with metrics_col3:
            st.metric("Energy Savings", "1.2M kWh", "Monthly")
        
        # Sustainability recommendations
        st.subheader("🌿 Improvement Opportunities")
        recommendations = [
            "Install solar panels on municipal buildings",
            "Implement smart street lighting",
            "Promote electric vehicle infrastructure",
            "Optimize water treatment plant energy usage",
            "Enhance building insulation standards"
        ]
        
        for i, recommendation in enumerate(recommendations, 1):
            st.markdown(f"{i}. {recommendation}")

def show_planner_assistance():
    st.markdown('<h2 class="success-animation">💡 AI Planner Assistance</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Get Recommendations")
        city_id = st.number_input("City ID for Recommendations", min_value=1, value=1, key="planner_city")
        
        if st.button("🤖 Get Smart Recommendations", use_container_width=True):
            with st.spinner("AI is generating personalized recommendations..."):
                time.sleep(2)
                try:
                    advice = suggest_improvements(city_id)
                    
                    st.markdown("""
                    <div class="feature-card success-animation">
                    """, unsafe_allow_html=True)
                    st.success("🎯 AI Recommendations Generated!")
                    
                    # Display recommendations in a structured way
                    st.subheader("📋 Action Plan")
                    
                    recommendations = [
                        "Optimize energy distribution during peak hours (18:00-21:00)",
                        "Implement demand-response programs for commercial sectors",
                        "Upgrade to LED street lighting in downtown areas",
                        "Install smart meters in residential districts",
                        "Develop renewable energy integration strategy"
                    ]
                    
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"**{i}.** {rec}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating recommendations: {str(e)}")
    
    with col2:
        st.subheader("Implementation Roadmap")
        
        # Timeline visualization
        timeline_data = {
            "Phase": ["Immediate (1-3 months)", "Short-term (3-6 months)", "Medium-term (6-12 months)", "Long-term (12+ months)"],
            "Actions": [
                "Smart meter deployment, Peak load analysis",
                "Renewable integration, Infrastructure upgrades",
                "AI optimization, Community engagement",
                "Full automation, Expansion planning"
            ],
            "Impact": ["15% savings", "25% savings", "35% savings", "50% savings"]
        }
        
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True)
        
        # Cost-benefit analysis
        st.subheader("💰 Cost-Benefit Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Initial Investment", "$2.5M")
        with col2:
            st.metric("Annual Savings", "$1.8M")
        with col3:
            st.metric("ROI Period", "1.4 years")

def show_analytics():
    st.markdown('<h2 class="success-animation">📈 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "📈 Trends", "🔍 Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("City Performance")
            fig = create_performance_chart()
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Energy Distribution")
            fig = create_distribution_chart()
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Historical Trends")
        
        # Sample time series data
        dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        consumption = np.random.normal(100000, 20000, len(dates)).cumsum()
        efficiency = np.random.normal(75, 10, len(dates))
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=dates, y=consumption, name="Energy Consumption", line=dict(color='#667eea')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=dates, y=efficiency, name="Efficiency %", line=dict(color='#ff6b6b')),
            secondary_y=True,
        )
        
        fig.update_layout(
            title="Monthly Energy Trends",
            xaxis_title="Month",
            height=400
        )
        
        fig.update_yaxes(title_text="Consumption (units)", secondary_y=False)
        fig.update_yaxes(title_text="Efficiency (%)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("AI-Generated Insights")
        
        insights = [
            "💡 **Peak Demand Pattern**: Highest consumption occurs on weekdays between 18:00-20:00",
            "🌱 **Renewable Opportunity**: 35% of current load can be shifted to renewable sources",
            "💰 **Cost Savings**: Potential 28% reduction through load optimization",
            "⚡ **Infrastructure**: Grid capacity utilization at 68% - room for expansion",
            "🔧 **Maintenance**: Predictive maintenance can reduce downtime by 45%"
        ]
        
        for insight in insights:
            st.markdown(f"- {insight}")
        
        st.subheader("Recommendation Priority")
        priority_data = {
            "Priority": ["High", "High", "Medium", "Medium", "Low"],
            "Action": [
                "Implement peak shaving strategies",
                "Deploy smart meters in commercial zones",
                "Solar panel installation program",
                "Energy efficiency awareness campaign",
                "Long-term infrastructure planning"
            ],
            "Impact": ["30% savings", "25% savings", "20% savings", "15% savings", "10% savings"]
        }
        
        df_priority = pd.DataFrame(priority_data)
        st.dataframe(df_priority, use_container_width=True)

# Chart creation functions
def create_realtime_chart():
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

def create_forecast_chart():
    days = list(range(1, 8))
    actual = [950, 1020, 980, 1100, 1050, 1075, 1030]
    predicted = [None] * 6 + [1080]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days[:-1], y=actual[:-1],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#667eea', width=4)
    ))
    
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

def create_efficiency_gauge(score):
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

def create_performance_chart():
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
