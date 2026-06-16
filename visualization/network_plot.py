"""
Network Visualization Module
--------------------------------------------------

Cities are not isolated collections of stations.
They are living networks whose behavior emerges
through interactions between zones.

The objective of this visualization is not merely
to display nodes and edges, but to provide an
intuitive understanding of how demand, risk,
and accessibility evolve across the city.

Node Size:
    Demand Intensity

Node Color:
    Collapse Risk

Edge:
    Transit Connectivity

This representation attempts to mimic the feeling
of observing a digital twin rather than a static graph.
"""

import networkx as nx
import plotly.graph_objects as go
import numpy as np


def render_network_graph(city_graph,
                         demand_state,
                         collapse_risk):

    pos = nx.spring_layout(city_graph, seed=42)

    edge_x = []
    edge_y = []

    for edge in city_graph.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=1,
            color="#94A3B8"
        ),
        hoverinfo="none"
    )

    node_x = []
    node_y = []

    node_sizes = []
    node_colors = []

    hover_text = []

    for node in city_graph.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

        demand = demand_state["zones"][node].intensity
        risk = collapse_risk["by_zone"][node]

        node_sizes.append(15 + demand * 3)
        node_colors.append(risk)

        hover_text.append(
            f"""
            Zone {node}

            Demand : {demand:.2f}

            Collapse Risk : {risk:.2f}
            """
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,

        mode="markers+text",

        text=[
            f"Z{i}"
            for i in city_graph.nodes()
        ],

        textposition="top center",

        hovertext=hover_text,

        hoverinfo="text",

        marker=dict(

            size=node_sizes,

            color=node_colors,

            colorscale="RdYlGn_r",

            colorbar=dict(
                title="Risk"
            ),

            line=dict(
                width=2,
                color="white"
            )
        )
    )

    fig = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    fig.update_layout(

        title="Urban Mobility Network",

        template="plotly_dark",

        height=650,

        showlegend=False,

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        )
    )

    return fig
```

