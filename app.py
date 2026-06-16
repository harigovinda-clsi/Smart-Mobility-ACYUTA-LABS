"""
OneJourney AI
===============================================================================

Cities are dynamic systems rather than isolated transportation assets.

OneJourney AI explores whether the decentralized predictive philosophy
previously investigated in crowd safety and resource allocation can be
adapted to urban mobility.

Instead of reacting to shortages after they occur, the framework attempts
to identify emerging accessibility imbalances before fragmentation becomes
visible to commuters.

The current implementation represents a simulation environment built around:

    Demand Flow Field
    +
    Collapse Risk Estimation
    +
    Mobility Equity Index
    +
    Decentralized Agent Coordination

The objective is not merely to maximize fleet utilization, but to study
how efficiency, accessibility, and resilience interact across the network.

Inspired by previously validated decentralized frameworks, the adaptation
to shared mobility remains exploratory and serves as a proof-of-concept
for future investigation.

===============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
import time
import sys
import os

# 1. Absolute path alignment
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. Safely catching the import/parsing failure
try:
    from core.synthetic_city import SyntheticCity
    from core.demand_generator import DemandGenerator
    from core.collapse_predictor import CollapsePredictor
    from core.mobility_equity_engine import MobilityEquityEngine
    from core.multi_agent_controller import MultiAgentController
    from visualization.network_plot import render_network_graph
    from visualization.heatmap_plot import render_equity_heatmap
    from visualization.metrics_panel import (
        render_metrics_panel,
        render_system_status,
        render_event_banner,
        render_weather_banner,
        render_time_banner
    )
except Exception as e:
    st.error("🚨 Failed to import custom modules!")
    st.exception(e)
    st.stop() # Stops execution so we can read the error cleanly

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="OneJourney AI - Mobility Equity",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional aesthetic and visible metrics
st.markdown("""
<style>
    :root {
        --primary-color: #0a2463;    /* Deep Navy */
        --secondary-color: #247ba0;  /* Teal */
        --success-color: #06d6a0;    /* Green */
        --warning-color: #f18f01;    /* Orange */
        --danger-color: #c1121f;     /* Red */
        --bg-light: #f5f5f5;         /* Light Gray */
    }
    
    .main {
        background-color: white;
    }
    
    /* Base card container styling */
    .stMetric {
        background-color: var(--bg-light) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--secondary-color) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* FIX: Force labels (e.g., "Collapse Risk") to be visible dark charcoal */
    [data-testid="stMetricLabel"] p {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* FIX: Force metric values (numbers) to be solid black */
    [data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "city" not in st.session_state:
    st.session_state.city = SyntheticCity(num_zones=12)

if "demand_gen" not in st.session_state:
    st.session_state.demand_gen = DemandGenerator()

if "collapse_predictor" not in st.session_state:
    st.session_state.collapse_predictor = CollapsePredictor()

if "equity_engine" not in st.session_state:
    st.session_state.equity_engine = MobilityEquityEngine()

if "agent_controller" not in st.session_state:
    st.session_state.agent_controller = MultiAgentController(
        num_zones=st.session_state.city.num_zones
    )

if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = {
        "timestamp": [],
        "collapse_risk": [],
        "avg_wait": [],
        "equity_score": [],
        "fleet_util": [],
        "zone_states": []
    }

# ============================================================================
# SIDEBAR: CONTROLS
# ============================================================================

st.sidebar.title("🎛️ Simulation Controls")

# Let users choose between an automatic live clock or a manual override slider
time_mode = st.sidebar.radio("Time Mode", ["Live Device Time", "Manual Override"])

if time_mode == "Live Device Time":
    now = datetime.datetime.now()
    time_slider = (now.hour * 60) + now.minute
    st.sidebar.info(f"⏰ Syncing live: {now.hour:02d}:{now.minute:02d}")
else:
    # Fallback manual slider if they want to experiment with different hours
    time_slider = st.sidebar.slider(
        "Simulation Time (Minutes from Start)",
        0, 1439, 765, step=10,
        help="Advance through a full day (1440 mins)."
    )

# Time control
time_slider = st.sidebar.slider(
    "Simulation Time (Minutes from Start)",
    0, 1439, int(current_device_minutes), step=10,
    help="Advance through a full day (1440 mins). Defaults to your device clock."
)

# Weather selection
weather = st.sidebar.selectbox(
    "🌤️ Weather Condition",
    ["Sunny", "Cloudy", "Light Rain", "Heavy Rain"],
    index=0
)

# Event selector
event = st.sidebar.selectbox(
    "📍 Special Event",
    ["None", "Festival", "Concert", "Accident", "Metro Delay"],
    index=0
)

# Metro frequency
metro_freq = st.sidebar.select_slider(
    "🚇 Metro Frequency",
    options=["Low", "Medium", "High"],
    value="Medium"
)

# Simulation speed
sim_speed = st.sidebar.slider(
    "⚡ Simulation Speed",
    1, 10, 3,
    help="Higher = faster time progression"
)

# ============================================================================
# MAIN HEADER
# ============================================================================

col_title, col_time = st.columns([3, 1])
with col_title:
    st.title("🛺 OneJourney AI")
    st.markdown(
        "**Predictive Last-Mile Mobility Equity Framework** \n"
        "*Decentralized MARL for fair scooter distribution*"
    )

with col_time:
    hours = time_slider // 60
    minutes = time_slider % 60
    time_of_day = f"{hours:02d}:{minutes:02d}"
    st.metric("Time of Day", time_of_day)

# ============================================================================
# SIMULATE ONE STEP
# ============================================================================

# Generate synthetic demand for current time
demand_state = st.session_state.demand_gen.generate_demand(
    time_minutes=time_slider,
    weather_condition=weather,
    event_type=event,
    metro_frequency=metro_freq
)

# Predict collapse risk
city_snapshot = st.session_state.city.get_city_snapshot()

collapse_risk = st.session_state.collapse_predictor.evaluate_network(
    demand_state,
    city_snapshot
)

# Compute mobility equity
equity_metrics = st.session_state.equity_engine.evaluate_network(
    demand_state,
    city_snapshot,
    collapse_risk
)

# Agent decisions
agent_actions = st.session_state.agent_controller.evaluate_network(
    demand_state,
    city_snapshot,
    collapse_risk,
    equity_metrics
)

# Update city state
st.session_state.city.update_city(demand_state)

# Store in history
st.session_state.simulation_history["timestamp"].append(time_slider)
st.session_state.simulation_history["collapse_risk"].append(collapse_risk["overall"])
st.session_state.simulation_history["avg_wait"].append(equity_metrics["average_wait_time"])
st.session_state.simulation_history["equity_score"].append(equity_metrics["fairness_score"])
st.session_state.simulation_history["fleet_util"].append(st.session_state.city.compute_fleet_utilization())

# ============================================================================
# TOP METRICS ROW
# ============================================================================

st.markdown("---")
metric_cols = st.columns(4)

with metric_cols[0]:
    st.metric(
        "Collapse Risk",
        f"{collapse_risk['overall']:.2f}",
        delta=f"{(collapse_risk['overall'] - 0.5) * 100:.1f}%",
        delta_color="inverse"
    )

with metric_cols[1]:
    st.metric(
        "Avg Wait Time",
        f"{equity_metrics['average_wait_time']:.1f} min",
        delta=f"-{max(0, equity_metrics['average_wait_time'] - 8):.1f} min" if equity_metrics['average_wait_time'] < 8 else None
    )

with metric_cols[2]:
    st.metric(
        "Equity Score (Gini)",
        f"{equity_metrics['fairness_score']:.3f}",
        delta="↑ Fair" if equity_metrics['fairness_score'] > 0.8 else "⚠ Unequal"
    )

with metric_cols[3]:
    st.metric(
        "Fleet Utilization",
        f"{st.session_state.city.compute_fleet_utilization():.1f}%",
        delta=f"+{st.session_state.city.compute_fleet_utilization()-50:.1f}%" if st.session_state.city.compute_fleet_utilization() > 50 else None
    )

st.markdown("---")

# ============================================================================
# TABBED INTERFACE
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 City Network",
    "🌊 Demand Flow Field",
    "📊 Equity Analysis",
    "🤖 Agent Decisions",
    "📈 Analytics"
])

# ─────────────────────────────────────────────────────────────────────────
# TAB 1: CITY NETWORK
# ─────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Network State Visualization")
    st.markdown(
        "Each zone node shows: demand intensity (size) + collapse risk (color) + "
        "available scooters (label). Edges represent transit corridors."
    )
    
    fig_network = render_network_graph(
        st.session_state.city.graph,
        demand_state,
        collapse_risk
    )
    st.plotly_chart(fig_network, use_container_width=True, key="network_plot")
    
    # Zone details table
    st.subheader("Zone Status Details")
    zone_df = pd.DataFrame({
        "Zone": [f"Zone {i+1}" for i in range(st.session_state.city.num_zones)],
        "Demand (rides/min)": [d.intensity for d in demand_state["zones"]],
        "Available Scooters": [st.session_state.city.zone_states[i]["availability"] for i in range(st.session_state.city.num_zones)],
        "Avg Wait (min)": [st.session_state.city.zone_states[i]["waiting_time"] for i in range(st.session_state.city.num_zones)],
        "Risk Level": ["🔴 High" if collapse_risk["by_zone"][i] > 0.7 else "🟡 Medium" if collapse_risk["by_zone"][i] > 0.4 else "🟢 Low" for i in range(st.session_state.city.num_zones)]
    })

    st.dataframe(
        zone_df,
        use_container_width=True,
        hide_index=True
    )

# ─────────────────────────────────────────────────────────────────────────
# TAB 2: DEMAND FLOW FIELD
# ─────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Demand Coherence & Flow Visualization")
    st.markdown(
        "High coherence (Φ_t ≈ 1): Demand flows smoothly through network.  \n"
        "Low coherence (Φ_t ≈ 0): Fragmented demand; fleet collapsing."
    )
    
    # Demand coherence per zone
    coherence_values = [demand_state["zones"][i].coherence for i in range(st.session_state.city.num_zones)]
    
    fig_flow = go.Figure()
    fig_flow.add_trace(go.Bar(
        x=[f"Z{i+1}" for i in range(st.session_state.city.num_zones)],
        y=coherence_values,
        marker=dict(
            color=coherence_values,
            colorscale="RdYlGn",
            cmin=0, cmax=1,
            colorbar=dict(title="Coherence")
        ),
        text=[f"{v:.2f}" for v in coherence_values],
        textposition="outside"
    ))
    fig_flow.update_layout(
        title="Demand Coherence by Zone (Φ_t)",
        xaxis_title="Zone",
        yaxis_title="Coherence [0=fragmented, 1=organized]",
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig_flow, use_container_width=True)
    
    st.markdown("**Key Insight:** Peripheral zones show low coherence → early warning for collapse.")

# ─────────────────────────────────────────────────────────────────────────
# TAB 3: EQUITY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Mobility Equity Index (MEI)")
    st.markdown(
        "MEI = Availability / Demand per zone. Low MEI = underserved zone.  \n"
        "**Gini coefficient target:** >0.85 (fair distribution)"
    )
    
    fig_equity = render_equity_heatmap(equity_metrics["zone_mei"])
    st.plotly_chart(fig_equity, use_container_width=True)
    
    # Zone fairness rankings
    st.subheader("Zone Fairness Rankings")
    mei_values = [
        (st.session_state.city.zone_states[i]["availability"] / max(demand_state["zones"][i].intensity, 1))
        for i in range(st.session_state.city.num_zones)
    ]
    
    zone_fairness = pd.DataFrame({
        "Rank": range(1, st.session_state.city.num_zones + 1),
        "Zone": [f"Zone {np.argsort(mei_values)[::-1][i]+1}" for i in range(st.session_state.city.num_zones)],
        "MEI Score": sorted(mei_values, reverse=True),
        "Status": ["✅ Fair" if v > 0.8 else "⚠️ Underserved" if v < 0.5 else "⚡ Adequate" for v in sorted(mei_values, reverse=True)]
    })
    st.dataframe(zone_fairness, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────
# TAB 4: AGENT DECISIONS
# ─────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Multi-Agent Rebalancing Actions (Next 15 Minutes)")
    st.markdown(
        "Each zone agent independently decides: dispatch, hold, or rebalance scooters.  \n"
        "Actions are coordinated via local observations + neighborhood info."
    )
    
    action_df = pd.DataFrame({
        "Zone": [f"Zone {i+1}" for i in range(st.session_state.city.num_zones)],
        "Action": [a.get("action", "Hold") for a in agent_actions],
        "Scooters to Move": [a.get("quantity", 0) for a in agent_actions],
        "Target": [a.get("target_zone", "-") for a in agent_actions],
        "Confidence": [f"{a.get('confidence', 0.5):.2f}" for a in agent_actions]
    })
    
    st.dataframe(action_df, use_container_width=True, hide_index=True)
    
    st.info(
        "🎬 **In full demo:** Animated scooter flow visualization showing real-time "
        "rebalancing actions across zones. Agents adapt dynamically to prevent collapse."
    )

# ─────────────────────────────────────────────────────────────────────────
# TAB 5: ANALYTICS & TRENDS
# ─────────────────────────────────────────────────────────────────────────
with tab5:
    st.subheader("Temporal Analytics")
    
    if len(st.session_state.simulation_history["timestamp"]) > 1:
        # Risk over time
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=st.session_state.simulation_history["timestamp"],
            y=st.session_state.simulation_history["collapse_risk"],
            mode="lines+markers",
            name="Collapse Risk",
            line=dict(color="#c1121f", width=2),
            fill="tozeroy"
        ))
        fig_risk.add_hline(y=0.5, line_dash="dash", line_color="orange", annotation_text="Warning")
        fig_risk.add_hline(y=0.7, line_dash="dash", line_color="red", annotation_text="Critical")
        fig_risk.update_layout(
            title="Collapse Risk Trajectory",
            xaxis_title="Simulation Time (min)",
            yaxis_title="Risk [0-1]",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Equity trend
        fig_equity_trend = go.Figure()
        fig_equity_trend.add_trace(go.Scatter(
            x=st.session_state.simulation_history["timestamp"],
            y=st.session_state.simulation_history["equity_score"],
            mode="lines+markers",
            name="Equity Score",
            line=dict(color="#06d6a0", width=2)
        ))
        fig_equity_trend.add_hline(y=0.85, line_dash="dash", line_color="green", annotation_text="Target")
        fig_equity_trend.update_layout(
            title="Equity (Gini) Evolution",
            xaxis_title="Simulation Time (min)",
            yaxis_title="Equity [0-1]",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig_equity_trend, use_container_width=True)
    else:
        st.info("Run simulation to populate analytics...")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    """
    <div style="
        text-align:center;
        color:#6B7280;
        font-size:0.88rem;
        line-height:1.7;
    ">
    <strong>OneJourney AI</strong><br>
    Predictive Last-Mile Intelligence Framework<br><br>
    Exploring interactions between efficiency, accessibility, and resilience in urban mobility systems.<br><br>
    Current implementation represents an exploratory simulation environment.<br>
    Validation for real-world deployment remains future work.<br><br>
    <strong>ACYUTA LABS</strong><br>
    SRMIST Urban Mobility Challenge 2026
    </div>
    """,
    unsafe_allow_html=True
)
