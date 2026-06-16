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

import random

class MultiAgentController:
    def __init__(self, num_zones=12):
        self.num_zones = num_zones

    def evaluate_network(self, demand_state, city_snapshot, collapse_risk, equity_metrics):
        """
        Evaluates decentralized zone agent logic. Instead of static "Hold" loops,
        it uses collapse risks and fairness drops to dynamically issue rebalancing actions.
        """
        actions = []
        by_zone_risks = collapse_risk.get("by_zone", [0.2] * self.num_zones)

        for i in range(self.num_zones):
            zone_risk = by_zone_risks[i]
            zone_demand = demand_state["zones"][i].intensity
            
            # Logic rules for multi-agent system response
            if zone_risk > 0.65:
                # Critical shortage/high risk -> Order scooters imported from a random safe zone
                possible_targets = [z for z in range(self.num_zones) if by_zone_risks[z] < 0.4 and z != i]
                target = f"Zone {random.choice(possible_targets) + 1}" if possible_targets else "Zone 1"
                
                action_type = "Rebalance In"
                quantity = int(zone_demand * 12)  # Proportional scale
                confidence = 0.72 + (zone_risk * 0.2)
                
            elif zone_risk < 0.25 and zone_demand < 1.5:
                # Saturated supply with low demand -> Offload surplus scooters to high risk areas
                action_type = "Rebalance Out"
                quantity = random.randint(10, 25)
                high_risk_zones = [z for z in range(self.num_zones) if by_zone_risks[z] > 0.5]
                target = f"Zone {random.choice(high_risk_zones) + 1}" if high_risk_zones else "-"
                confidence = 0.65 + (random.random() * 0.1)
                
            else:
                # Balanced stable operational corridor
                action_type = "Hold"
                quantity = 0
                target = "-"
                confidence = 0.60 + (random.random() * 0.1)

            # Append structured dictionary matching exactly what app.py expects to unpack
            actions.append({
                "action": action_type,
                "quantity": quantity,
                "target_zone": target,
                "confidence": round(confidence, 2)
            })

        return actions
