"""
Synthetic City
===============================================================================

Cities are networks rather than isolated collections of stations.

The objective of this module is not to reproduce any specific city,
but to construct a simplified urban environment within which mobility
patterns, accessibility asymmetries, and interventions can be studied.

The synthetic city maintains only resource and accessibility states.

Demand itself is generated externally through the DemandGenerator module.

This separation reflects the idea that infrastructure and mobility demand
are distinct but interacting components of urban systems.

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

    # ==================================================================
    # Graph Construction
    # ==================================================================

    def initialize_graph(self):
        """
        Construct connectivity relationships between zones.

        The topology intentionally combines central hubs and
        peripheral regions to reproduce accessibility asymmetries.
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

    # ==================================================================
    # Zone Initialization
    # ==================================================================

    def initialize_zone_states(self):
        """
        Initialize resource availability and accessibility
        characteristics associated with each zone.

        Peripheral regions intentionally begin with fewer
        mobility resources.
        """

        for zone in range(self.num_zones):

            if zone in [8,9,11]:

                availability = np.random.randint(

                    15,
                    30
                )

            else:

                availability = np.random.randint(

                    40,
                    90
                )

            self.zone_states[zone] = {

                "availability":

                availability,

                "waiting_time":

                np.random.uniform(

                    3,
                    8
                ),

                "utilization":

                np.random.uniform(

                    0.4,
                    0.75
                ),

                "status":

                "Healthy"

            }

    # ==================================================================
    # State Update
    # ==================================================================

    def update_zone_state(
            self,
            zone_demand):
        """
        Update local conditions in response to
        evolving demand.

        Demand is supplied externally through
        the DemandGenerator.
        """

        zone_id = zone_demand.zone_id

        intensity = zone_demand.intensity

        zone = self.zone_states[zone_id]

        availability = zone["availability"]

        availability -= int(

            intensity
        )

        availability = max(

            availability,
            0
        )

        utilization = min(

            1.0,

            intensity / 10
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

            "availability":

            availability,

            "waiting_time":

            waiting_time,

            "utilization":

            utilization,

            "status":

            status

        }

    # ==================================================================
    # Batch Update
    # ==================================================================

    def update_city(
            self,
            demand_state):
        """
        Update all zones using the current demand snapshot.
        """

        for zone_demand in demand_state["zones"]:

            self.update_zone_state(

                zone_demand
            )

    # ==================================================================
    # Fleet Utilization
    # ==================================================================

    def compute_fleet_utilization(self):
        """
        Aggregate local utilization into
        a city-level indicator.
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

    # ==================================================================
    # Average Waiting Time
    # ==================================================================

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

    # ==================================================================
    # Snapshot
    # ==================================================================

    def get_city_snapshot(self):
        """
        Capture the current state of the city.

        The snapshot acts as a bridge between
        demand generation, collapse estimation,
        equity analysis, and decentralized control.
        """

        return {

            "graph":

            self.graph,

            "zones":

            self.zone_states,

            "zone_states":

            self.zone_states,

            "fleet_utilization":

            self.compute_fleet_utilization(),

            "average_wait_time":

            self.compute_average_wait_time()

        }
