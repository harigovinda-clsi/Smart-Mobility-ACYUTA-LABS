import numpy as np
from dataclasses import dataclass

@dataclass
class ZoneDemand:
    zone_id: int
    intensity: float
    coherence: float
    origin_distribution: np.ndarray
    destination_distribution: np.ndarray

class DemandGenerator:
    """Generate realistic demand across zones with temporal, weather, and event modulation"""
    
    def __init__(self, num_zones=12):
        self.num_zones = num_zones
        self.base_demand = self._init_base_demand()
    
    def _init_base_demand(self):
        hours = np.arange(24)
        morning_peak = 4.0 * np.exp(-((hours - 7.5)**2) / 2.0)
        evening_peak = 5.5 * np.exp(-((hours - 18)**2) / 2.5)
        midday = 2.0 * np.ones(24)
        return midday + morning_peak + evening_peak
    
    # INDENT THIS WHOLE METHOD BLOCK BY 4 SPACES:
    def generate_demand(
        self,
        time_minutes=0,
        weather_condition="Sunny",
        event_type="None",
        metro_frequency="Medium"):
     
        """
        Generate a synthetic snapshot representing the current state 
        of urban mobility demand. 
        """
        hour = (time_minutes // 60) % 24
        minute = time_minutes % 60
        
        # ... Keep all the internal code inside safely indented ...
        
        return {
            "timestamp": time_minutes,
            "hour": hour,
            "minute": minute,
            "weather": weather_condition,
            "event": event_type,
            "zones": zone_demands,
            "total_rides_per_minute": sum(z.intensity for z in zone_demands)
        }
