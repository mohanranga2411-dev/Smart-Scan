from typing import Dict, Any
from backend.environment import Environment

class Receiver:
    def __init__(self, environment: Environment):
        self.env = environment
        self.last_observation: Dict[str, Any] = {}

    def send_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives an Action payload from Person 1 (AI),
        passes it to the Environment, and returns the resulting Observation.
        
        Action Contract: {"next_band": int, "dwell_time": float}
        """
        # Validate action contract parameters
        next_band = action.get("next_band", 0)
        dwell_time = action.get("dwell_time", 0.10)

        # Pass action to environment step
        observation = self.env.step({
            "next_band": next_band,
            "dwell_time": dwell_time
        })

        self.last_observation = observation
        return observation