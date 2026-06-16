```python
"""
Analytics Visualization Module
--------------------------------------------------

Cities are dynamic systems rather than static
snapshots.

A single measurement of collapse risk reveals
little about the underlying processes that
produced it.

Therefore, the objective of analytics is not
simply to display metrics, but to narrate the
evolution of the city through time.

The dashboard attempts to answer four questions:

1. Is the city becoming more fragile?

2. Are accessibility inequalities widening?

3. Is fleet utilization improving?

4. Are interventions restoring balance?

Visualization transforms isolated observations
into system-level understanding.
"""

import plotly.graph_objects as go


def plot_collapse_risk_history(
        risk_history):

    """
    Collapse Risk Through Time
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            y=risk_history,

            mode="lines+markers",

            line=dict(

                width=3,

                color="#EF4444"
            ),

            name="Collapse Risk"
        )
    )

    fig.update_layout(

        title="Evolution of Collapse Risk",

        xaxis_title="Simulation Step",

        yaxis_title="Risk Level",

        template="plotly_dark",

        height=450
    )

    return fig


def plot_fairness_history(
        fairness_history):

    """
    Mobility Equity Through Time
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            y=fairness_history,

            mode="lines+markers",

            line=dict(

                width=3,

                color="#10B981"
            ),

            name="Fairness Score"
        )
    )

    fig.update_layout(

        title="Evolution of Accessibility Equity",

        xaxis_title="Simulation Step",

        yaxis_title="Fairness Score",

        template="plotly_dark",

        height=450
    )

    return fig


def plot_fleet_utilization(
        utilization_history):

    """
    Fleet Efficiency Through Time
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            y=utilization_history,

            mode="lines+markers",

            line=dict(

                width=3,

                color="#3B82F6"
            ),

            name="Fleet Utilization"
        )
    )

    fig.update_layout(

        title="Fleet Utilization Dynamics",

        xaxis_title="Simulation Step",

        yaxis_title="Utilization (%)",

        template="plotly_dark",

        height=450
    )

    return fig


def plot_wait_time_history(
        wait_time_history):

    """
    Waiting Time Evolution
    """

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            y=wait_time_history,

            mode="lines+markers",

            line=dict(

                width=3,

                color="#F59E0B"
            ),

            name="Average Waiting Time"
        )
    )

    fig.update_layout(

        title="Evolution of Average Waiting Time",

        xaxis_title="Simulation Step",

        yaxis_title="Minutes",

        template="plotly_dark",

        height=450
    )

    return fig


def plot_system_dashboard(
        risk_history,
        fairness_history,
        utilization_history,
        wait_time_history):

    """
    Composite Storytelling Panel

    Rather than viewing metrics in isolation,
    this function enables observers to understand
    the interactions between fragility, equity,
    efficiency, and commuter experience.
    """

    figures = {

        "risk":

        plot_collapse_risk_history(

            risk_history
        ),

        "fairness":

        plot_fairness_history(

            fairness_history
        ),

        "utilization":

        plot_fleet_utilization(

            utilization_history
        ),

        "wait_time":

        plot_wait_time_history(

            wait_time_history
        )
    }

    return figures
```

