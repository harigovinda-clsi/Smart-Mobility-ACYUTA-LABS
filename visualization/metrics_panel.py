```python
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
    Render top-level dashboard metrics.

    Parameters
    ----------

    collapse_risk : float

    fairness_score : float

    fleet_utilization : float

    avg_wait_time : float
    """

    col1, col2, col3, col4 = st.columns(4)

    # -------------------------------------------------
    # Collapse Risk
    # -------------------------------------------------

    with col1:

        if collapse_risk < 0.3:

            risk_status = "Healthy"

        elif collapse_risk < 0.7:

            risk_status = "Stressed"

        else:

            risk_status = "Critical"

        st.metric(

            label="Collapse Risk",

            value=f"{collapse_risk:.2f}",

            delta=risk_status
        )

    # -------------------------------------------------
    # Fairness Score
    # -------------------------------------------------

    with col2:

        st.metric(

            label="Fairness Score",

            value=f"{fairness_score:.2f}",

            delta="Accessibility Equity"
        )

    # -------------------------------------------------
    # Fleet Utilization
    # -------------------------------------------------

    with col3:

        st.metric(

            label="Fleet Utilization",

            value=f"{fleet_utilization:.1f}%",

            delta="Resource Efficiency"
        )

    # -------------------------------------------------
    # Waiting Time
    # -------------------------------------------------

    with col4:

        st.metric(

            label="Average Waiting Time",

            value=f"{avg_wait_time:.1f} min",

            delta="Commuter Experience"
        )


def render_system_status(

        collapse_risk):

    """
    Provide a qualitative interpretation of
    overall system health.
    """

    if collapse_risk < 0.3:

        st.success(

            "System Status : Stable"

        )

    elif collapse_risk < 0.7:

        st.warning(

            "System Status : Under Stress"

        )

    else:

        st.error(

            "System Status : Approaching Fragmentation"

        )


def render_event_banner(

        event_name):

    """
    Highlight exogenous events affecting
    mobility dynamics.
    """

    if event_name != "None":

        st.info(

            f"Active Event : {event_name}"

        )


def render_weather_banner(

        weather_condition):

    """
    Weather acts as an external disturbance
    influencing demand and accessibility.
    """

    st.caption(

        f"Weather Condition : {weather_condition}"
    )


def render_time_banner(

        simulation_hour):

    """
    Time influences commuter behavior and
    demand concentration.
    """

    st.caption(

        f"Simulation Time : {simulation_hour}:00"
    )
```
