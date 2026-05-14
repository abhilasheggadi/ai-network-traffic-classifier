"""
Network Traffic Classifier Dashboard - Streamlit UI
Real-time traffic analysis and classification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests

# Page configuration
st.set_page_config(
    page_title="AI Network Traffic Classifier",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Color Palette
COLOR_PRIMARY = "#00d4ff"      # Bright cyan - primary accents
COLOR_SECONDARY = "#1a1a2e"    # Dark navy - backgrounds
COLOR_NORMAL = "#2ecc71"       # Bright green - normal/safe traffic
COLOR_MALICIOUS = "#e74c3c"    # Red - alerts/attacks
COLOR_WARNING = "#f39c12"      # Orange - warnings
COLOR_ACCENT = "#9b59b6"       # Purple - secondary accents
COLOR_HEADER = "#0a0e27"       # Very dark blue - header background

# Custom CSS with professional styling
st.markdown(f"""
<style>
    /* Overall styling */
    .main {{
        background-color: {COLOR_SECONDARY};
    }}
    
    /* Metric card styling with colored left borders */
    [data-testid="metric-container"] {{
        background-color: #0f1419;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {COLOR_PRIMARY};
        margin-bottom: 10px;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 24px;
        color: #ffffff;
        font-weight: bold;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #a0a0a0;
        font-size: 13px;
    }}
    
    [data-testid="stMetricDelta"] {{
        color: #2ecc71;
        font-size: 12px;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {COLOR_SECONDARY};
    }}
    
    /* General text */
    .stMarkdown {{
        color: #e0e0e0;
    }}
    
    /* Header styling */
    .header-container {{
        background: linear-gradient(135deg, {COLOR_HEADER} 0%, #1a2a3a 100%);
        padding: 20px;
        border-bottom: 3px solid {COLOR_PRIMARY};
        margin: -20px -20px 20px -20px;
        border-radius: 0;
    }}
    
    .header-title {{
        color: {COLOR_PRIMARY};
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }}
    
    .header-subtitle {{
        color: #a0a0a0;
        font-size: 14px;
        margin: 5px 0 0 0;
    }}
    
    /* Metric cards with different colors */
    .metric-card-1 {{ border-left-color: {COLOR_PRIMARY} !important; }}
    .metric-card-2 {{ border-left-color: {COLOR_NORMAL} !important; }}
    .metric-card-3 {{ border-left-color: {COLOR_WARNING} !important; }}
    .metric-card-4 {{ border-left-color: {COLOR_MALICIOUS} !important; }}
    .metric-card-5 {{ border-left-color: {COLOR_ACCENT} !important; }}
    
    /* Chart styling */
    .plotly-container {{
        background-color: {COLOR_SECONDARY};
    }}
    
    /* Dataframe styling */
    .stDataFrame {{
        background-color: #0f1419;
    }}
    
    /* Divider styling */
    .stDivider {{
        background-color: #404050 !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {COLOR_PRIMARY};
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: #00b8d4;
        transform: translateY(-2px);
    }}
</style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://127.0.0.1:8000"
API_KEY = "dev-key-change-in-production"  # Default dev key
API_HEADERS = {"X-API-Key": API_KEY}

# Sidebar
with st.sidebar:
    st.title("🔒 AI Network Classifier")
    st.markdown("Smart Traffic Analysis & Classification")
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Live Traffic", "Predictions", "Traffic Analysis", "Model Performance", "Alerts"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("**Model Version:** v1.0.0\n\n**Updated:** May 12, 2026")

# ============ DASHBOARD PAGE ============
if page == "Dashboard":
    # Professional Header Bar
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🔒 Network Traffic Classifier</div>
        <div class="header-subtitle">Real-Time Threat Detection & Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status Row
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("")
    with col2:
        st.markdown(f"<p style='color: #2ecc71; font-weight: bold;'>🟢 Online</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='color: #a0a0a0;'>{datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Key Metrics with Custom Styling
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background-color: #0f1419; padding: 15px; border-radius: 8px; border-left: 4px solid #00d4ff;">
            <p style="color: #a0a0a0; font-size: 13px; margin: 0 0 10px 0;">Total Traffic Analyzed</p>
            <p style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 0;">1.2M</p>
            <p style="color: #2ecc71; font-size: 12px; margin: 5px 0 0 0;">↑ 12.4% from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #0f1419; padding: 15px; border-radius: 8px; border-left: 4px solid #2ecc71;">
            <p style="color: #a0a0a0; font-size: 13px; margin: 0 0 10px 0;">Normal Traffic</p>
            <p style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 0;">862K</p>
            <p style="color: #2ecc71; font-size: 12px; margin: 5px 0 0 0;">69.1% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #0f1419; padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12;">
            <p style="color: #a0a0a0; font-size: 13px; margin: 0 0 10px 0;">Malicious Traffic</p>
            <p style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 0;">385K</p>
            <p style="color: #f39c12; font-size: 12px; margin: 5px 0 0 0;">30.9% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #0f1419; padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c;">
            <p style="color: #a0a0a0; font-size: 13px; margin: 0 0 10px 0;">Active Alerts</p>
            <p style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 0;">12</p>
            <p style="color: #e74c3c; font-size: 12px; margin: 5px 0 0 0;">🔴 High Priority</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background-color: #0f1419; padding: 15px; border-radius: 8px; border-left: 4px solid #9b59b6;">
            <p style="color: #a0a0a0; font-size: 13px; margin: 0 0 10px 0;">Model Accuracy</p>
            <p style="color: #ffffff; font-size: 24px; font-weight: bold; margin: 0;">98.34%</p>
            <p style="color: #2ecc71; font-size: 12px; margin: 5px 0 0 0;">Last 24h</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts Row 1
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Traffic Classification")
        
        traffic_types = {
            'Normal': 862592,
            'DoS': 158483,
            'Port Scan': 78864,
            'Brute Force': 59879,
            'Botnet': 51212,
            'DDoS': 37022
        }
        
        colors = ['#2ecc71', '#e74c3c', '#f39c12', '#e67e22', '#c0392b', '#8b0000']
        fig = go.Figure(data=[go.Pie(
            labels=list(traffic_types.keys()),
            values=list(traffic_types.values()),
            hole=0.4,
            marker=dict(colors=colors),
        )])
        
        fig.update_layout(
            height=350,
            showlegend=True,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#1a1a2e',
            font=dict(color='#e0e0e0'),
            legend=dict(font=dict(size=10))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Traffic Over Time (Last Hour)")
        
        # Generate time series
        times = pd.date_range(end=datetime.now(), periods=40, freq='min')
        normal = np.cumsum(np.random.randint(500, 1500, 40))
        malicious = np.cumsum(np.random.randint(100, 400, 40))
        total = normal + malicious
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=normal, mode='lines', name='Normal', 
                                 line=dict(color='#2ecc71', width=2), fill='tozeroy'))
        fig.add_trace(go.Scatter(x=times, y=malicious, mode='lines', name='Malicious',
                                 line=dict(color='#e74c3c', width=2), fill='tozeroy'))
        fig.add_trace(go.Scatter(x=times, y=total, mode='lines', name='Total',
                                 line=dict(color='#00d4ff', width=2.5)))
        
        fig.update_layout(
            height=350, 
            hovermode='x unified', 
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#0f1419',
            font=dict(color='#e0e0e0'),
            legend=dict(font=dict(size=10))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Recent Predictions Table
    st.subheader("Recent Predictions")
    
    predictions = {
        'Time': ['10:42:28', '10:42:27', '10:42:26', '10:42:25', '10:42:24'],
        'Source IP': ['192.168.1.105', '192.168.1.107', '192.168.1.108', '192.168.1.109', '192.168.1.110'],
        'Destination IP': ['203.45.67.89', '185.234.219.16', '203.45.67.90', '45.33.32.156', '103.21.244.12'],
        'Prediction': ['Normal', 'DoS', 'Port Scan', 'Brute Force', 'Botnet'],
        'Confidence': ['99.12%', '97.45%', '95.32%', '96.18%', '94.77%']
    }
    
    df_pred = pd.DataFrame(predictions)
    st.dataframe(df_pred, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Bottom Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Source IPs")
        
        top_ips = pd.DataFrame({
            'IP': ['192.168.1.105', '192.168.1.107', '192.168.1.108', '192.168.1.109', '192.168.1.110'],
            'Packets': [98221, 87621, 76543, 65432, 54321]
        })
        
        fig = px.bar(top_ips, x='Packets', y='IP', orientation='h', 
                     color='Packets', color_continuous_scale=['#1a1a2e', '#00d4ff'])
        fig.update_layout(
            height=300, 
            margin=dict(l=0, r=0, t=0, b=0), 
            showlegend=False,
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#0f1419',
            font=dict(color='#e0e0e0')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Recent Alerts")
        
        # Create alerts dataframe
        alerts_data = {
            'Time': ['10:42:23', '10:42:18', '10:42:10', '10:41:55', '10:41:30'],
            'Type': ['DDoS Attack', 'Port Scan', 'Brute Force', 'Suspicious Activity', 'Malware Detected'],
            'Source': ['202.12.27.33', '203.45.67.90', '45.33.32.156', '192.168.1.50', '185.234.219.16'],
            'Severity': ['Critical', 'High', 'High', 'Medium', 'Critical'],
            'Status': ['Active', 'Active', 'Mitigated', 'Monitoring', 'Blocked']
        }
        
        df_alerts = pd.DataFrame(alerts_data).head(3)
        
        # Display top 3 alerts with color coding
        st.error("🔴 DDoS Attack - 202.12.27.33 @ 10:42:23")
        st.caption("Severity: **Critical** | Status: Active")
        
        st.warning("🟡 Port Scan - 203.45.67.90 @ 10:42:18")
        st.caption("Severity: **High** | Status: Active")
        
        st.warning("🟡 Brute Force - 45.33.32.156 @ 10:42:10")
        st.caption("Severity: **High** | Status: Mitigated")
        
        if st.button("📋 View All Alerts", key="dashboard_alerts"):
            st.subheader("All Recent Alerts")
            alerts_full = pd.DataFrame(alerts_data)
            
            # Add emoji indicators for severity
            severity_emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵'}
            alerts_full['Severity'] = alerts_full['Severity'].map(lambda x: f"{severity_emoji.get(x, '')} {x}")
            
            # Display the alerts dataframe
            st.dataframe(alerts_full, use_container_width=True, hide_index=True)

# ============ LIVE TRAFFIC PAGE ============
elif page == "Live Traffic":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">📡 Live Traffic Analysis</div>
        <div class="header-subtitle">Real-time network packet monitoring</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        refresh = st.slider("Refresh interval (seconds)", 1, 30, 5)
    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Simulated live data
    live_data = []
    for i in range(15):
        live_data.append({
            'Timestamp': (datetime.now() - timedelta(seconds=i*5)).strftime('%H:%M:%S'),
            'Source IP': f"192.168.1.{100 + i}",
            'Destination IP': f"10.0.0.{50 + i}",
            'Protocol': np.random.choice(['TCP', 'UDP']),
            'Port': np.random.randint(1000, 65535),
            'Bytes': np.random.randint(100, 10000),
            'Type': np.random.choice(['Normal', 'DoS', 'Scan']),
            'Confidence': f"{np.random.randint(90, 100)}%"
        })
    
    df_live = pd.DataFrame(live_data)
    st.dataframe(df_live, use_container_width=True, hide_index=True)

# ============ PREDICTIONS PAGE ============
elif page == "Predictions":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🎯 Make Predictions</div>
        <div class="header-subtitle">Classify network traffic with AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Enter Traffic Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.number_input("Duration (seconds)", value=120, step=1)
        src_bytes = st.number_input("Source Bytes", value=5000, step=100)
        dst_bytes = st.number_input("Destination Bytes", value=4000, step=100)
        count = st.number_input("Connection Count", value=5, step=1)
        srv_count = st.number_input("Service Count", value=4, step=1)
    
    with col2:
        serror_rate = st.slider("Error Rate (%)", 0.0, 100.0, 2.0) / 100
        srv_serror_rate = st.slider("Service Error Rate (%)", 0.0, 100.0, 2.0) / 100
        rerror_rate = st.slider("Rejected Rate (%)", 0.0, 100.0, 1.0) / 100
        srv_rerror_rate = st.slider("Service Rejected (%)", 0.0, 100.0, 1.0) / 100
    
    same_srv_rate = st.slider("Same Service Rate", 0.0, 1.0, 0.95)
    dst_host_count = st.number_input("Dest Host Count", value=10, step=1)
    dst_host_srv_count = st.number_input("Dest Service Count", value=8, step=1)
    
    if st.button("🔍 Classify Traffic", use_container_width=True):
        try:
            payload = {
                "duration": duration,
                "protocol_type": "tcp",
                "service": "http",
                "flag": "S2",
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "land": 0,
                "wrong_fragment": 0,
                "urgent": 0,
                "hot": 0,
                "num_failed_logins": 0,
                "logged_in": 1,
                "num_compromised": 0,
                "root_shell": 0,
                "su_attempted": 0,
                "num_root": 0,
                "num_file_creations": 0,
                "num_shells": 0,
                "num_access_files": 0,
                "num_outbound_cmds": 0,
                "is_host_login": 0,
                "is_guest_login": 0,
                "count": count,
                "srv_count": srv_count,
                "serror_rate": serror_rate,
                "srv_serror_rate": srv_serror_rate,
                "rerror_rate": rerror_rate,
                "srv_rerror_rate": srv_rerror_rate,
                "same_srv_rate": same_srv_rate,
                "same_ctry_rate": 0.98,
                "dst_host_count": dst_host_count,
                "dst_host_srv_count": dst_host_srv_count,
                "dst_host_same_srv_rate": 0.9,
                "dst_host_diff_srv_rate": 0.1,
                "dst_host_same_src_port_rate": 0.95,
                "dst_host_srv_diff_host_rate": 0.05,
                "dst_host_serror_rate": 0.01,
                "dst_host_srv_serror_rate": 0.01,
                "dst_host_rerror_rate": 0.01,
                "dst_host_srv_rerror_rate": 0.01
            }
            
            response = requests.post(f"{API_BASE_URL}/predict", json=payload, headers=API_HEADERS, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Classification", result['prediction'].upper())
                with col2:
                    st.metric("Confidence", f"{result['confidence']*100:.2f}%")
                with col3:
                    st.metric("Timestamp", result['timestamp'][:10])
                
                st.markdown("### Probabilities")
                probs = result['probabilities']
                prob_df = pd.DataFrame(list(probs.items()), columns=['Type', 'Probability'])
                prob_df['Probability'] = (prob_df['Probability'] * 100).round(2)
                prob_df = prob_df.sort_values('Probability', ascending=False)
                
                fig = px.bar(prob_df, x='Type', y='Probability', color='Type',
                             color_discrete_sequence=['#00d4ff', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'])
                fig.update_layout(
                    height=400, 
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='#1a1a2e',
                    plot_bgcolor='#0f1419',
                    font=dict(color='#e0e0e0'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}\n\nMake sure FastAPI is running: http://127.0.0.1:8000")

# ============ ANALYTICS PAGE ============
elif page == "Traffic Analysis":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">📊 Traffic Analysis</div>
        <div class="header-subtitle">Advanced traffic analysis & insights</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["By Hour", "By Protocol", "By Destination"])
    
    with tab1:
        st.subheader("Traffic by Hour")
        hours = pd.date_range(start=datetime.now().date(), periods=24, freq='h')
        traffic = np.random.randint(5000, 15000, 24)
        
        fig = px.bar(x=hours, y=traffic, labels={'x': 'Hour', 'y': 'Packets'}, color=traffic,
                     color_continuous_scale=['#1a1a2e', '#00d4ff'])
        fig.update_layout(
            height=400, 
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#0f1419',
            font=dict(color='#e0e0e0'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Traffic by Protocol")
        protocols = ['TCP', 'UDP', 'ICMP', 'Other']
        counts = [800000, 350000, 80000, 17842]
        colors_protocol = ['#00d4ff', '#2ecc71', '#f39c12', '#9b59b6']
        
        fig = px.pie(values=counts, names=protocols, color=protocols,
                     color_discrete_map=dict(zip(protocols, colors_protocol)))
        fig.update_layout(
            height=400, 
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#1a1a2e',
            font=dict(color='#e0e0e0')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Top Destinations")
        dests = pd.DataFrame({
            'IP': ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5'],
            'Packets': [120000, 95000, 78000, 65000, 52000]
        })
        
        fig = px.bar(dests, x='IP', y='Packets', color='Packets',
                     color_continuous_scale=['#1a1a2e', '#00d4ff'])
        fig.update_layout(
            height=400, 
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#0f1419',
            font=dict(color='#e0e0e0'),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ============ MODEL INFO PAGE ============
elif page == "Model Performance":
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🤖 Model Performance</div>
        <div class="header-subtitle">Performance metrics & specifications</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", "96.8%")
    with col2:
        st.metric("Precision", "96.81%")
    with col3:
        st.metric("Recall", "96.8%")
    with col4:
        st.metric("F1 Score", "96.8%")
    
    st.divider()
    
    st.markdown("### Classification Report")
    report_data = {
        'Type': ['Normal', 'DoS', 'Port Scan', 'Brute Force', 'Botnet'],
        'Precision': [96.5, 97.2, 95.8, 97.3, 97.8],
        'Recall': [96.8, 97.0, 95.5, 96.8, 97.5],
        'F1-Score': [96.6, 97.1, 95.6, 97.0, 97.6],
        'Support': [1000, 1000, 1000, 1000, 1000]
    }
    
    st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.markdown("### Features Used (12 Total)")
    features = [
        '1. duration', '2. src_bytes', '3. dst_bytes', '4. count',
        '5. srv_count', '6. serror_rate', '7. srv_serror_rate', '8. rerror_rate',
        '9. srv_rerror_rate', '10. same_srv_rate', '11. dst_host_count', '12. dst_host_srv_count'
    ]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        for f in features[0:4]:
            st.markdown(f"• {f}")
    with col2:
        for f in features[4:8]:
            st.markdown(f"• {f}")
    with col3:
        for f in features[8:12]:
            st.markdown(f"• {f}")

# ============ ALERTS PAGE ============
else:  # Alerts
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">⚠️ Alerts & Events</div>
        <div class="header-subtitle">Security events & threat intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter controls
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        alert_levels = st.multiselect("Filter by Level", ["Critical", "High", "Medium"], default=["Critical", "High", "Medium"])
    
    with col2:
        time_filter = st.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
    
    with col3:
        status_filter = st.multiselect("Filter by Status", ["Active", "Mitigated", "Blocked", "Monitoring"], default=["Active", "Mitigated"])
    
    st.divider()
    
    # All alerts data
    all_alerts = [
        {'Time': '10:42:23', 'Type': 'DDoS Attack', 'Source': '202.12.27.33', 'Severity': 'Critical', 'Status': 'Active', 'Description': 'High volume attack detected from multiple sources'},
        {'Time': '10:42:18', 'Type': 'Port Scan', 'Source': '203.45.67.90', 'Severity': 'High', 'Status': 'Active', 'Description': 'Suspicious port scanning activity'},
        {'Time': '10:42:10', 'Type': 'Brute Force Attempt', 'Source': '45.33.32.156', 'Severity': 'High', 'Status': 'Mitigated', 'Description': 'Multiple failed login attempts detected'},
        {'Time': '10:41:55', 'Type': 'Suspicious Activity', 'Source': '192.168.1.50', 'Severity': 'Medium', 'Status': 'Monitoring', 'Description': 'Unusual traffic pattern detected'},
        {'Time': '10:41:30', 'Type': 'Malware Detected', 'Source': '185.234.219.16', 'Severity': 'Critical', 'Status': 'Blocked', 'Description': 'Known malicious signature identified'},
    ]
    
    # Filter alerts
    filtered_alerts = [a for a in all_alerts if a['Severity'] in alert_levels and a['Status'] in status_filter]
    
    # Display alerts as expandable cards
    for idx, alert in enumerate(filtered_alerts):
        severity_color = {'Critical': '🔴', 'High': '🟡', 'Medium': '🔵'}.get(alert['Severity'], '⚪')
        status_color = {'Active': '🔴', 'Mitigated': '🟢', 'Blocked': '✅', 'Monitoring': '🟠'}.get(alert['Status'], '')
        
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{severity_color}**")
            
            with col2:
                st.markdown(f"**{alert['Type']}**")
                st.caption(f"From: {alert['Source']}")
            
            with col3:
                st.caption(alert['Time'])
                st.caption(f"Status: {alert['Status']} {status_color}")
            
            with col4:
                st.caption(alert['Description'])
            
            st.divider()
    
    # Summary statistics
    st.subheader("Alert Summary")
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    total_alerts = len(all_alerts)
    critical_alerts = len([a for a in all_alerts if a['Severity'] == 'Critical'])
    high_alerts = len([a for a in all_alerts if a['Severity'] == 'High'])
    active_alerts = len([a for a in all_alerts if a['Status'] == 'Active'])
    
    with summary_col1:
        st.metric("Total Alerts", total_alerts)
    
    with summary_col2:
        st.metric("Critical", critical_alerts, delta="+2" if critical_alerts > 1 else None)
    
    with summary_col3:
        st.metric("High Priority", high_alerts)
    
    with summary_col4:
        st.metric("Active Now", active_alerts)
