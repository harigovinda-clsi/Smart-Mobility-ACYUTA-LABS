"""
Mobility Equity Heatmap
--------------------------------------------------

Efficiency and accessibility are not synonymous.

A city may exhibit high fleet utilization while
simultaneously leaving peripheral communities
underserved.

The purpose of this visualization is therefore
not simply to display numbers, but to expose
emerging accessibility asymmetries.

Green:
    Well-served regions

Yellow:
    Moderately stressed regions

Red:
    Persistent accessibility deficits

The heatmap provides a spatial lens through which
mobility inequality becomes observable.
"""

import numpy as np
import plotly.graph_objects as go


def render_equity_heatmap(mei_values):

    """
    Parameters
    ----------
    mei_values : list

        Mobility Equity Index values
        for all 12 zones.

    Returns
    -------
    Plotly Heatmap
    """

    zone_labels = [
        "Z0","Z1","Z2","Z3",
        "Z4","Z5","Z6","Z7",
        "Z8","Z9","Z10","Z11"
    ]

    heatmap_matrix = np.array(
        mei_values
    ).reshape(3,4)

    fig = go.Figure(

        data=go.Heatmap(

            z=heatmap_matrix,

            colorscale="RdYlGn",

            zmin=0,

            zmax=2,

            colorbar=dict(

                title="MEI"
            ),

            hovertemplate=

            "Mobility Equity Index : %{z:.2f}<extra></extra>"
        )
    )

    fig.update_layout(

        title="Mobility Equity Landscape",

        template="plotly_dark",

        height=500,

        xaxis=dict(

            tickmode="array",

            tickvals=[0,1,2,3],

            ticktext=[

                zone_labels[0],
                zone_labels[1],
                zone_labels[2],
                zone_labels[3]
            ]
        ),

        yaxis=dict(

            tickmode="array",

            tickvals=[0,1,2],

            ticktext=[

                "Cluster A",

                "Cluster B",

                "Cluster C"
            ]
        )
    )

    return fig


def render_zone_ranking_table(mei_values):

    """
    Generates zone-wise ranking.

    Lower MEI indicates underserved regions.
    """

    ranking = []

    for zone_id, mei in enumerate(mei_values):

        ranking.append(

            {

                "Zone":

                f"Zone {zone_id}",

                "MEI":

                round(mei,3)
            }
        )

    ranking = sorted(

        ranking,

        key=lambda x: x["MEI"]
    )

    return ranking


def compute_city_fairness_score(mei_values):

    """
    Measure overall equity.

    Higher values imply a more balanced network.
    """

    variance = np.var(mei_values)

    fairness_score = 1/(1 + variance)

    return round(

        fairness_score,

        3
    )
