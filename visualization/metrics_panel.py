"""
Metrics Panel
--------------------------------------------------

Complex systems produce enormous amounts of
information. Human operators, however, cannot
continuously monitor every variable.

Metrics therefore act as compressed summaries
of the city's health.

The objective is not to maximize the number of
statistics shown, but to surface the few indicators
that best capture the balance between efficiency,
equity, and resilience.

Collapse Risk
    Fragility of the mobility network.

Fairness Score
    Accessibility balance across zones.

Fleet Utilization
    Efficiency of resource deployment.

Average Waiting Time
    Quality of commuter experience.

These metrics collectively represent different
dimensions of urban mobility health.
"""

import streamlit as st


def render_metrics_panel(
        collapse_risk,
        fairness_score,
        fleet_utilization,
        avg_wait_time):
    """
    Render top-level dashboard metrics with explicit CSS styling
    to ensure text visibility on white card backgrounds.

    Parameters
    ----------
    collapse_risk : float
    fairness_score : float
    fleet_utilization : float
    avg_wait_time : float
    """
    
    # Inject CSS to override default text color inside metric cards
    st.markdown(
        """
        <style>
        /* Force metric labels and values to be visible dark charcoal/black */
        [data-testid="stMetricLabel"] p {
            color: #1A1A1A !important;
            font-weight: 500 !important;
        }
        [data-testid="stMetricValue"] div {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        /* Style the delta containers slightly to preserve meaning */
        [data-testid="stMetricDelta"] div {
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    # -------------------------------------------------
    # Collapse Risk
    # -------------------------------------------------
    with col1:
        if collapse_risk < 0.3:
            risk_status = "Healthy"
            delta_color = "normal"
        elif collapse_risk < 0.7:
            risk_status = "Stressed"
            delta_color = "off"
        else:
            risk_status = "Critical"
            delta_color = "inverse"

        st.metric(
            label="Collapse Risk",
            value=f"{collapse_risk:.2f}",
            delta=risk_status,
            delta_color=delta_color
        )

    # -------------------------------------------------
    # Fairness Score
    # -------------------------------------------------
    with col2:
        st.metric(
            label="Equity Score (Gini)",
            value=f"{fairness_score:.3f}",
            delta="Accessibility Equity",
            delta_color="normal"
        )

    # -------------------------------------------------
    # Fleet Utilization
    # -------------------------------------------------
    with col3:
        st.metric(
            label="Fleet Utilization",
            value=f"{fleet_utilization:.1f}%",
            delta="Resource Efficiency",
            delta_color="normal"
        )

    # -------------------------------------------------
    # Waiting Time
    # -------------------------------------------------
    with col4:
        st.metric(
            label="Average Waiting Time",
            value=f"{avg_wait_time:.1f} min",
            delta="Commuter Experience",
            delta_color="inverse"
        )


def render_system_status(collapse_risk):
    """
    Provide a qualitative interpretation of
    overall system health.
    """
    if collapse_risk < 0.3:
        st.success("System Status : Stable")
    elif collapse_risk < 0.7:
        st.warning("System Status : Under Stress")
    else:
        st.error("System Status : Approaching Fragmentation")


def render_event_banner(event_name):
    """
    Highlight exogenous events affecting
    mobility dynamics.
    """
    if event_name != "None":
        st.info(f"Active Event : {event_name}")


def render_weather_banner(weather_condition):
    """
    Weather acts as an external disturbance
    influencing demand and accessibility.
    """
    st.caption(f"Weather Condition : {weather_condition}")


def render_time_banner(simulation_hour):
    """
    Time influences commuter behavior and
    demand concentration.
    """
    # Formats single digits like 6 to a clean 24-hour timestamp string "06:00"
    st.caption(f"Simulation Time : {int(simulation_hour):02d}:00")
