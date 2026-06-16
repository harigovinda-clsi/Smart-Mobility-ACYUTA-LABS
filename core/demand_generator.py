"""
Demand Generator - Time-varying synthetic demand patterns
Mirrors AquaEdgeAI's demand synthesis but for scooter ride requests
"""

import numpy as np
from dataclasses import dataclass

@dataclass
class ZoneDemand:
    zone_id: int
    intensity: float  # rides per minute
    coherence: float  # Phi_t: 1=organized, 0=fragmented
    origin_distribution: np.ndarray
    destination_distribution: np.ndarray

class DemandGenerator:
    """Generate realistic demand across zones with temporal, weather, and event modulation"""
    
    def __init__(self, num_zones=12):
        self.num_zones = num_zones
        self.base_demand = self._init_base_demand()
    
    def _init_base_demand(self):
        """Base hourly demand curve (6am-midnight)"""
        # Two peaks: morning (7-9am), evening (5-7pm)
        hours = np.arange(24)
        morning_peak = 4.0 * np.exp(-((hours - 7.5)**2) / 2.0)
        evening_peak = 5.5 * np.exp(-((hours - 18)**2) / 2.5)
        midday = 2.0 * np.ones(24)
        return midday + morning_peak + evening_peak
    
    def generate_demand(self, time_minutes=0, weather_condition="Sunny", event_type="None", metro_frequency="Medium"):
        """Generate demand state for current simulation time"""
        
        hour = (time_minutes // 60) % 24
        minute = time_minutes % 60
        
        # Base hourly demand
        base_intensity = self.base_demand[int(hour)]
        
        # Weather modulation
        weather_factor = {
            "Sunny": 1.0,
            "Cloudy": 0.85,
            "Light Rain": 0.6,
            "Heavy Rain": 0.3
        }.get(weather_condition, 1.0)
        
        # Event modulation
        event_factor = {
            "None": 1.0,
            "Festival": 2.5,
            "Concert": 2.2,
            "Accident": 0.4,
            "Metro Delay": 1.8
        }.get(event_type, 1.0)
        
        # Metro frequency modulation (affects scooter reliance)
        metro_factor = {
            "Low": 1.4,
            "Medium": 1.0,
            "High": 0.7
        }.get(metro_frequency, 1.0)
        
        # Compute zone-level demands
        zone_demands = []
        for i in range(self.num_zones):
            is_peripheral = i >= 6
            
            # Peripheral zones have LOWER base demand but HIGHER spikes during events
            zone_base = (1.2 if is_peripheral else 1.0) * base_intensity
            
            # Coherence: high during off-peak, drops during rush (fragmented demand)
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                coherence = 0.5 + 0.2 * np.random.random()  # Fragmented rush
            else:
                coherence = 0.8 + 0.1 * np.random.random()  # Organized off-peak
            
            intensity = zone_base * weather_factor * event_factor * metro_factor
            intensity += np.random.normal(0, intensity * 0.1)  # Add noise
            intensity = max(0.1, intensity)
            
            zone_demands.append(ZoneDemand(
                zone_id=i,
                intensity=intensity,
                coherence=coherence,
                origin_distribution=np.random.dirichlet(np.ones(self.num_zones)),
                destination_distribution=np.random.dirichlet(np.ones(self.num_zones))
            ))
        
        return {
            "timestamp": time_minutes,
            "hour": hour,
            "minute": minute,
            "weather": weather_condition,
            "event": event_type,
            "zones": zone_demands,
            "total_rides_per_minute": sum(z.intensity for z in zone_demands)
        }

