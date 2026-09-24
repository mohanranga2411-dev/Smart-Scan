from backend.environment import Environment

def test_environment_step():
    env = Environment(num_bands=100, noise_level=0.20)
    
    # Test action sampling band 10 (STATIC emitter)
    action = {"next_band": 10, "dwell_time": 0.10}
    obs = env.step(action)
    
    print("Observation Output:")
    print(obs)
    
    assert "timestamp" in obs
    assert "hit" in obs
    assert "selected_band" in obs

if __name__ == "__main__":
    test_environment_step()
    print("Environment smoke test passed!")