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
    def __init__(self):
        pass

    def _calculate_gini(self, allocations):
        """Computes the Gini Coefficient for a list of resource allocations."""
        n = len(allocations)
        if n == 0:
            return 0.0
        
        allocations = np.array(allocations, dtype=np.float64)
        mean_val = np.mean(allocations)
        
        if mean_val == 0:
            return 0.0  # Safe fallback if there are no resources anywhere
        
        # Efficient vectorized calculation of absolute differences
        abs_diffs = np.abs(allocations[:, None] - allocations)
        gini = np.sum(abs_diffs) / (2 * (n ** 2) * mean_val)
        return float(gini)

    def evaluate_network(self, demand_state, city_snapshot):
        """
        Evaluates real-time fairness based on current zone demand vs available scooters.
        """
        zone_equity_metrics = []
        
        # Iterate over matching zones to determine service fulfillment ratios
        for zone_id, zone_data in city_snapshot.items():
            # Extract real-world demand dynamically, avoiding zero division
            demand = max(demand_state.get(zone_id, {}).get('demand', 1.0), 0.1)
            available = zone_data.get('available_scooters', 0)
            
            # Metric: How well is the supply meeting the localized demand?
            fulfillment_ratio = available / demand
            zone_equity_metrics.append(fulfillment_ratio)
            
        # Calculate Gini Index (0 = perfect equality, 1 = maximum inequality)
        gini_index = self._calculate_gini(zone_equity_metrics)
        
        # Convert to an Equity/Fairness Score sitting realistically between 0.0 and 1.0
        # A higher score implies high systemic fairness across the network
        fairness_score = max(0.0, min(1.0, 1.0 - gini_index))
        
        return {
            "equity_score": round(fairness_score, 3),
            "gini_index": round(gini_index, 3),
            "zone_metrics": zone_equity_metrics
        }
