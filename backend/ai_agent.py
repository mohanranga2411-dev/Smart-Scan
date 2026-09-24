import random
from typing import Dict, Any

class ScanningAI:
    def __init__(self, num_bands: int = 100):
        self.num_bands = num_bands
        self.current_band = 0
        self.history = []

    def decide_next_action(self, last_observation: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyzes the last observation payload and decides the next action.
        Returns an Action payload: {"next_band": int, "dwell_time": float}
        """
        if last_observation is None:
            # Initial state: begin scanning at band 0
            return {"next_band": 0, "dwell_time": 0.10}

        # Store observation history
        self.history.append(last_observation)

        hit = last_observation.get("hit", False)
        confidence = last_observation.get("confidence", 0.0)
        current_band = last_observation.get("selected_band", self.current_band)

        if hit and confidence > 0.70:
            # Target lock: stay on current band longer to collect signal detail
            dwell_time = 0.25
            next_band = current_band
        elif hit:
            # Moderate signal: re-check neighboring band
            dwell_time = 0.15
            next_band = (current_band + 1) % self.num_bands
        else:
            # Clear band: sweep forward quickly
            dwell_time = 0.10
            next_band = (current_band + 5) % self.num_bands

        self.current_band = next_band
        return {
            "next_band": int(next_band),
            "dwell_time": round(float(dwell_time), 2)
        }