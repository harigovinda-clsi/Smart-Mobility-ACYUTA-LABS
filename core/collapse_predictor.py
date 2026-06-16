```python
"""
Collapse Predictor
===============================================================================

Urban systems rarely fail instantaneously.

Periods of instability are often preceded by
early signatures that manifest as fragmented
demand patterns, increasing pressure, and
resource scarcity.

The purpose of this module is therefore not
to detect collapse after it occurs, but to
identify emerging stress before fragmentation
becomes visible to commuters.

Collapse risk is treated as a function of:

    Demand coherence

    Demand pressure

    Resource utilization

rather than a consequence of any single variable.

===============================================================================
"""

import numpy as np


class CollapsePredictor:
    """
    Estimate network fragility and zone-level stress.
    """

    def __init__(self):

        pass

    # ==================================================================
    # Demand Pressure
    # ==================================================================

    def compute_demand_pressure(
            self,
            intensity):
        """
        Normalize ride demand.

        Higher values imply increasing stress.
        """

        pressure = intensity / 10

        return min(

            pressure,
            1.0
        )

    # ==================================================================
    # Collapse Risk
    # ==================================================================

    def compute_zone_risk(
            self,
            zone_demand,
            zone_state):
        """
        Estimate local collapse risk.

        Fragmented mobility patterns combined
        with high utilization and low availability
        increase fragility.
        """

        phi = zone_demand.coherence

        intensity = zone_demand.intensity

        utilization = zone_state["utilization"]

        availability = zone_state["availability"]

        demand_pressure = self.compute_demand_pressure(

            intensity
        )

        scarcity_factor = 1 - min(

            availability / 100,

            1.0
        )

        risk = (

            0.4 * (1 - phi)

            +

            0.3 * demand_pressure

            +

            0.2 * utilization

            +

            0.1 * scarcity_factor

        )

        risk = min(

            risk,
            1.0
        )

        return risk

    # ==================================================================
    # Status Classification
    # ==================================================================

    def classify_risk(
            self,
            risk):
        """
        Convert numerical values into
        interpretable categories.
        """

        if risk < 0.3:

            return "Healthy"

        elif risk < 0.7:

            return "Stressed"

        else:

            return "Critical"

    # ==================================================================
    # City-wide Assessment
    # ==================================================================

    def evaluate_network(
            self,
            demand_state,
            city_snapshot):
        """
        Estimate stress across the network.

        Parameters
        ----------

        demand_state :

            Output from DemandGenerator

        city_snapshot :

            Output from SyntheticCity
        """

        zone_risks = []

        statuses = []

        zone_states = city_snapshot["zones"]

        for zone_demand in demand_state["zones"]:

            zone_id = zone_demand.zone_id

            risk = self.compute_zone_risk(

                zone_demand,

                zone_states[zone_id]

            )

            zone_risks.append(

                risk
            )

            statuses.append(

                self.classify_risk(

                    risk
                )
            )

        overall_risk = np.mean(

            zone_risks
        )

        return {

            "overall":

            overall_risk,

            "by_zone":

            zone_risks,

            "status":

            statuses

        }
```

