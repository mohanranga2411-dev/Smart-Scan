from backend.environment import Environment
from backend.receiver import Receiver

def test_receiver_pipeline():
    env = Environment(num_bands=100, noise_level=0.20)
    receiver = Receiver(environment=env)

    action = {"next_band": 30, "dwell_time": 0.15}
    obs = receiver.send_action(action)

    print("Receiver Observation Output:")
    print(obs)

    assert obs["selected_band"] == 30
    assert obs["duration_estimate"] == 0.15

# IMPORTANT: Make sure these lines are at the very bottom, unindented:
if __name__ == "__main__":
    test_receiver_pipeline()
    print("Receiver pipeline test passed!")