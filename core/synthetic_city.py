```python
"""
Synthetic City
===============================================================================

Cities are networks rather than isolated collections of stations.

The objective of this module is not to reproduce any specific city,
but to construct a simplified urban environment within which mobility
patterns, accessibility asymmetries, and interventions can be studied.

The synthetic city contains:

    Metro hubs

    Bus corridors

    Residential districts

    Commercial zones

    Peripheral communities

Each zone maintains a local state describing resource availability,
waiting time, and utilization.

The resulting structure serves as the spatial backbone for the
OneJourney AI simulation environment.

===============================================================================
"""

import networkx as nx
import numpy as np


class SyntheticCity:
    """
    Representation of a simplified metropolitan mobility network.
    """

    def __init__(self, num_zones=12):

        self.num_zones = num_zones

        self.graph = nx.Graph()

        self.zone_states = {}

        self.initialize_graph()

        self.initialize_zone_states()

    # ===================================================================
    # Graph Construction
    # ===================================================================

    def initialize_graph(self):
        """
        Construct the underlying connectivity structure.

        The topology intentionally combines central hubs with
        peripheral regions to reproduce accessibility asymmetries
        frequently observed in urban systems.
        """

        for zone in range(self.num_zones):

            self.graph.add_node(zone)

        transit_edges = [

            (0,1),
            (0,2),

            (1,3),

            (2,3),

            (3,5),

            (4,6),

            (5,7),

            (6,7),

            (7,10),

            (8,5),

            (9,6),

            (10,11),

            (8,9)

        ]

        self.graph.add_edges_from(

            transit_edges
        )

    # ===================================================================
    # Zone Initialization
    # ===================================================================

    def initialize_zone_states(self):
        """
        Initialize mobility resources and local characteristics.

        Peripheral zones intentionally begin with fewer resources
        to emulate structural imbalances often observed in practice.
        """

        for zone in range(self.num_zones):

            if zone in [8,9,11]:

                scooter_count = np.random.randint(

                    15,
                    30
                )

            else:

                scooter_count = np.random.randint(

                    40,
                    90
                )

            self.zone_states[zone] = {

                "scooters":

                scooter_count,

                "waiting_time":

                np.random.uniform(

                    3,
                    8
                ),

                "utilization":

                np.random.uniform(

                    0.40,
                    0.75
                ),

                "status":

                "Healthy"

            }

    # ===================================================================
    # State Update
    # ===================================================================

    def update_zone_state(
            self,
            zone_id,
            demand_intensity):
        """
        Update local state in response to changing demand.

        Higher demand increases waiting time and utilization
        while reducing available resources.
        """

        zone = self.zone_states[zone_id]

        scooters = zone["scooters"]

        scooters -= int(

            demand_intensity
        )

        scooters = max(

            scooters,
            0
        )

        utilization = min(

            1.0,

            demand_intensity / 10
        )

        waiting_time = (

            3
            +
            12 * utilization
        )

        if utilization < 0.4:

            status = "Healthy"

        elif utilization < 0.75:

            status = "Stressed"

        else:

            status = "Critical"

        self.zone_states[zone_id] = {

            "scooters":

            scooters,

            "waiting_time":

            waiting_time,

            "utilization":

            utilization,

            "status":

            status
        }

    # ===================================================================
    # Fleet Statistics
    # ===================================================================

    def compute_fleet_utilization(self):
        """
        Aggregate local behavior into a city-level indicator.

        Utilization represents the fraction of resources actively
        participating in mobility flows.
        """

        utilizations = [

            state["utilization"]

            for state

            in self.zone_states.values()

        ]

        return (

            np.mean(

                utilizations

            )

            * 100
        )

    # ===================================================================
    # Waiting Time
    # ===================================================================

    def compute_average_wait_time(self):
        """
        Estimate average commuter waiting time.
        """

        wait_times = [

            state["waiting_time"]

            for state

            in self.zone_states.values()

        ]

        return np.mean(

            wait_times
        )

    # ===================================================================
    # Snapshot
    # ===================================================================

    def get_city_snapshot(self):
        """
        Capture the current state of the mobility network.

        The snapshot acts as a bridge between
        demand generation, collapse estimation,
        equity analysis, and decentralized control.
        """

        return {

            "graph":

            self.graph,

            "zone_states":

            self.zone_states,

            "fleet_utilization":

            self.compute_fleet_utilization(),

            "average_wait_time":

            self.compute_average_wait_time()

        }
```

