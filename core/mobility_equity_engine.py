"""
Mobility Equity Engine
===============================================================================

Efficiency and accessibility are not synonymous.

A city may exhibit high fleet utilization while
simultaneously leaving peripheral communities
underserved.

The objective of this module is therefore not
to maximize equality, but to identify emerging
accessibility imbalances before they become
persistent.

Accessibility is represented through the
Mobility Equity Index:

        availability
MEI = --------------
            demand

Lower values indicate zones where mobility
resources may be insufficient relative to
local demand.

===============================================================================
"""

import numpy as np


class MobilityEquityEngine:
    """
    Quantify accessibility and equity across zones.
    """

    def __init__(self):

        pass

    # ==============================================================
    # Mobility Equity Index
    # ==============================================================

    def compute_mei(
            self,
            availability,
            demand):
        """
        Compute local accessibility.

        Higher values imply better alignment
        between resources and demand.
        """

        demand = max(

            demand,
            0.1
        )

        return availability / demand

    # ==============================================================
    # Zone-wise MEI
    # ==============================================================

    def evaluate_network(
            self,
            demand_state,
            city_snapshot,
            collapse_risk):
        """
        Estimate accessibility across the city.
        """

        zone_states = city_snapshot["zones"]

        mei_values = []

        underserved_zones = []

        for zone_demand in demand_state["zones"]:

            zone_id = zone_demand.zone_id

            availability = zone_states[zone_id][

                "availability"

            ]

            demand = zone_demand.intensity

            mei = self.compute_mei(

                availability,

                demand

            )

            mei_values.append(

                mei
            )

            if mei < 3:

                underserved_zones.append(

                    zone_id
                )

        variance_mei = np.var(

            mei_values
        )

        fairness_score = 1 / (

            1 + variance_mei
        )

        average_wait_time = city_snapshot[

            "average_wait_time"

        ]

        return {

            "zone_mei":

            mei_values,

            "variance":

            variance_mei,

            "fairness_score":

            fairness_score,

            "average_wait_time":

            average_wait_time,

            "underserved_zones":

            underserved_zones,

            "collapse_risk":

            collapse_risk["overall"]

        }
```

