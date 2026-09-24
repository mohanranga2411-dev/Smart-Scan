import numpy as np
from enum import Enum
from typing import Dict, Any, List

class EmitterType(Enum):
    STATIC = "STATIC"
    PERIODIC = "PERIODIC"
    INTERMITTENT = "INTERMITTENT"
    BURST = "BURST"
    FREQUENCY_AGILE = "FREQUENCY_AGILE"

class Emitter:
    def __init__(self, emitter_id: int, emitter_type: EmitterType, initial_band: int):
        self.id = emitter_id
        self.type = emitter_type
        self.current_band = initial_band
        self.active = True
        
        # Internal state tracking for dynamic behaviors
        self.period = 5.0          # For PERIODIC
        self.active_duration = 2.0  # For INTERMITTENT/BURST
        self.idle_duration = 3.0    # For INTERMITTENT
        self.burst_count = 0       # For BURST tracking

    def update_state(self, current_time: float, total_bands: int) -> None:
        """Update emitter state based on its specific behavior pattern."""
        if self.type == EmitterType.STATIC:
            # Stays on the same band and remains active continuously
            self.active = True

        elif self.type == EmitterType.PERIODIC:
            # Toggles active state predictably based on period
            cycle = current_time % self.period
            self.active = cycle < (self.period / 2.0)

        elif self.type == EmitterType.INTERMITTENT:
            # Alternates active and idle phases
            cycle = current_time % (self.active_duration + self.idle_duration)
            self.active = cycle < self.active_duration

        elif self.type == EmitterType.BURST:
            # Brief, high-density transmissions followed by longer quiet periods
            cycle = current_time % 10.0
            self.active = cycle < 0.5  # Active for short 0.5s window

        elif self.type == EmitterType.FREQUENCY_AGILE:
            # Active continuously but hops across different frequency bands
            self.active = True
            if int(current_time * 2) % 2 == 0:  # Hop every 0.5 seconds
                self.current_band = int((self.current_band + 7) % total_bands)


class Environment:
    def __init__(self, num_bands: int = 100, noise_level: float = 0.20):
        self.num_bands = num_bands
        self.noise_level = noise_level
        self.current_time = 0.0
        self.emitters: List[Emitter] = []
        self._initialize_default_emitters()

    def _initialize_default_emitters(self) -> None:
        """Instantiate the 5 required emitter behaviors."""
        types = [
            (EmitterType.STATIC, 10),
            (EmitterType.PERIODIC, 30),
            (EmitterType.INTERMITTENT, 50),
            (EmitterType.BURST, 70),
            (EmitterType.FREQUENCY_AGILE, 90),
        ]
        for idx, (e_type, band) in enumerate(types):
            self.emitters.append(Emitter(emitter_id=idx + 1, emitter_type=e_type, initial_band=band))

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advance simulation time based on dwell_time and evaluate chosen band.
        
        Action Contract input: {"next_band": int, "dwell_time": float}
        Observation Contract output: Matching Phase 1 frozen schema
        """
        selected_band = action.get("next_band", 0)
        dwell_time = max(action.get("dwell_time", 0.1), 0.01)

        # Advance environment clock
        self.current_time += dwell_time

        # Update all emitters to the new current time
        for emitter in self.emitters:
            emitter.update_state(self.current_time, self.num_bands)

        # Check for signal presence in the selected band
        detected_signal = False
        signal_power = 0.0

        for emitter in self.emitters:
            if emitter.active and emitter.current_band == selected_band:
                detected_signal = True
                signal_power = max(signal_power, 0.85)  # Simulated signal magnitude

        # Add Gaussian thermal noise floor
        noise = float(np.random.normal(0, self.noise_level))
        total_signal_strength = max(0.0, min(1.0, (signal_power if detected_signal else 0.0) + noise))

        # Determine detection hit threshold
        hit = total_signal_strength > 0.40
        confidence = min(1.0, max(0.0, (total_signal_strength - 0.2) / 0.8)) if hit else (1.0 - total_signal_strength)

        # Construct payload matching Person 2 -> Person 1 Observation Contract
        observation = {
            "timestamp": round(self.current_time, 2),
            "selected_band": selected_band,
            "hit": hit,
            "confidence": round(float(confidence), 2),
            "signal_strength": round(float(total_signal_strength), 2),
            "duration_estimate": round(dwell_time, 2),
            "features": {}
        }

        return observation