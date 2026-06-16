```python
"""
Demand Flow Field
===============================================================================

Mobility demand is not merely a collection of isolated requests.

Instead, demand propagates through the network as structured
origin-destination interactions.

The objective of this module is to represent mobility demand
as a dynamic flow field whose organization may contain early
signatures of fragmentation.

Highly coherent flow patterns indicate stable mobility regimes.

Fragmented flow patterns suggest increasing competition for
resources and the possibility of emerging instability.

===============================================================================
"""

import numpy as np


class DemandFlowField:
    """
    Characterize mobility flows across the network.
    """

    def __init__(
            self,
            num_zones=12):

        self.num_zones = num_zones

    # ================================================================
    # Flow Matrix
    # ================================================================

    def compute_flow_matrix(
            self,
            demand_state):
        """
        Estimate origin-destination interactions.
        """

        flow_matrix = np.zeros(

            (
                self.num_zones,
                self.num_zones
            )
        )

        for zone_demand in demand_state["zones"]:

            origin = zone_demand.zone_id

            intensity = zone_demand.intensity

            destinations = (

                zone_demand.destination_distribution
            )

            flow_matrix[origin] = (

                intensity

                *

                destinations
            )

        return flow_matrix

    # ================================================================
    # Zone Flow Strength
    # ================================================================

    def compute_zone_strength(
            self,
            flow_matrix):
        """
        Aggregate total outgoing mobility.
        """

        return np.sum(

            flow_matrix,

            axis=1
        )

    # ================================================================
    # Network Coherence
    # ================================================================

    def compute_network_coherence(
            self,
            demand_state):
        """
        Aggregate local coherence values.
        """

        phi_values = [

            zone.coherence

            for zone

            in demand_state["zones"]

        ]

        return np.mean(

            phi_values
        )

    # ================================================================
    # Fragmentation Index
    # ================================================================

    def compute_fragmentation_index(
            self,
            demand_state):
        """
        Quantify disorder in mobility patterns.

        Lower coherence implies higher fragmentation.
        """

        network_phi = (

            self.compute_network_coherence(

                demand_state
            )
        )

        fragmentation = (

            1

            -

            network_phi
        )

        return fragmentation

    # ================================================================
    # Complete Flow Representation
    # ================================================================

    def evaluate_network(
            self,
            demand_state):
        """
        Generate a complete representation
        of mobility flows.
        """

        flow_matrix = (

            self.compute_flow_matrix(

                demand_state
            )
        )

        return {

            "flow_matrix":

            flow_matrix,

            "zone_flow_strength":

            self.compute_zone_strength(

                flow_matrix
            ),

            "network_coherence":

            self.compute_network_coherence(

                demand_state
            ),

            "fragmentation_index":

            self.compute_fragmentation_index(

                demand_state
            )

        }
```

