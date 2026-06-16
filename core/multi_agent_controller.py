```python
"""
Multi-Agent Controller
===============================================================================

Resilience in complex systems rarely emerges through
centralized control.

Instead, local agents continuously adapt to changing
conditions using partial observations and neighborhood
information.

The purpose of this module is therefore not to pursue
global optimization, but to study how decentralized
coordination can improve accessibility and stability.

Each zone acts as an autonomous decision-making unit.

Actions include:

    Hold

    Dispatch

    Rebalance

===============================================================================
"""


class MultiAgentController:
    """
    Decentralized coordination layer.
    """

    def __init__(
            self,
            num_zones=12):

        self.num_zones = num_zones

    # ==================================================================
    # Local Decision
    # ==================================================================

    def decide_action(
            self,
            zone_id,
            zone_demand,
            zone_state,
            zone_risk,
            zone_mei):
        """
        Generate zone-level intervention.
        """

        availability = zone_state["availability"]

        intensity = zone_demand.intensity

        # ---------------------------------------------------------
        # Severe stress
        # ---------------------------------------------------------

        if zone_risk > 0.7:

            return {

                "action":

                "Dispatch",

                "quantity":

                max(

                    5,

                    int(intensity)
                ),

                "target_zone":

                zone_id,

                "confidence":

                0.95

            }

        # ---------------------------------------------------------
        # Equity deficit
        # ---------------------------------------------------------

        elif zone_mei < 3:

            return {

                "action":

                "Rebalance",

                "quantity":

                3,

                "target_zone":

                zone_id,

                "confidence":

                0.80

            }

        # ---------------------------------------------------------
        # Healthy
        # ---------------------------------------------------------

        else:

            return {

                "action":

                "Hold",

                "quantity":

                0,

                "target_zone":

                "-",

                "confidence":

                0.60

            }

    # ==================================================================
    # Network-wide Coordination
    # ==================================================================

    def evaluate_network(
            self,
            demand_state,
            city_snapshot,
            collapse_metrics,
            equity_metrics):
        """
        Produce interventions for all zones.
        """

        zone_states = city_snapshot["zones"]

        actions = []

        for zone_demand in demand_state["zones"]:

            zone_id = zone_demand.zone_id

            action = self.decide_action(

                zone_id,

                zone_demand,

                zone_states[zone_id],

                collapse_metrics["by_zone"][zone_id],

                equity_metrics["zone_mei"][zone_id]

            )

            actions.append(

                action
            )

        return actions
```

