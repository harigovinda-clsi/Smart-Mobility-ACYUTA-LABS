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

    def _calculate_gini(self, values):
        """Standard Gini coefficient calculation (0 = perfect equality, 1 = inequality)."""
        n = len(values)
        if n == 0:
            return 0.0
        array = np.array(values, dtype=np.float64)
        if np.mean(array) == 0:
            return 0.0
        
        # Vectorized absolute difference
        abs_diff = np.abs(array[:, None] - array)
        gini = np.sum(abs_diff) / (2 * n**2 * np.mean(array))
        return float(gini)

    def evaluate_network(self, demand_state, city_snapshot, collapse_risk):
        """
        Calculates realistic, dynamic equity values mapping directly to app.py requirements.
        """
        # 1. Dynamically compute Mobility Equity Index (MEI) for all 12 zones
        mei_values = []
        waiting_times = []
        
        for i, zone_demand in enumerate(demand_state["zones"]):
            intensity = max(zone_demand.intensity, 0.1)
            # Pull real fluctuating values from the running state simulation snapshot
            availability = city_snapshot[i].get("availability", 50) if isinstance(city_snapshot, list) else city_snapshot.get(i, {}).get("availability", 50)
            
            # MEI formula: availability relative to current demand intensity
            mei = availability / intensity
            mei_values.append(mei)
            
            # Simulate a realistic waiting time based on current shortage/demand
            base_wait = 4.0 + (intensity * 1.5)
            shortage_penalty = max(0, (intensity - availability) * 0.1)
            waiting_times.append(base_wait + shortage_penalty)

        # 2. Calculate Fairness Score via inverted Gini Index
        gini_coeff = self._calculate_gini(mei_values)
        fairness_score = max(0.2, min(0.98, 1.0 - gini_coeff))

        # 3. Shape the MEI array into a 3x4 grid for the Cluster A/B/C heatmap layout
        # Maps 12 zones to 3 rows (Clusters) x 4 columns (Z0-Z3)
        mei_matrix = np.array(mei_values).reshape(3, 4).tolist()

        return {
            "fairness_score": fairness_score,
            "average_wait_time": float(np.mean(waiting_times)),
            "zone_mei": mei_matrix
        }
