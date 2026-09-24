import asyncio
import json
import websockets
from backend.ai_agent import ScanningAI

async def run_simulation_client(steps: int = 10):
    uri = "ws://127.0.0.1:8000/ws/scan"
    ai = ScanningAI(num_bands=100)
    
    print(f"Connecting to WebSocket engine at {uri}...")
    
    async with websockets.connect(uri) as websocket:
        last_obs = None
        
        for step in range(1, steps + 1):
            # 1. AI decides next action based on previous observation
            action = ai.decide_next_action(last_obs)
            
            # 2. Transmit action over WebSocket
            await websocket.send(json.dumps(action))
            print(f"\n[Step {step}] Sent Action: {action}")
            
            # 3. Receive observation response back from Receiver/Environment
            response = await websocket.recv()
            last_obs = json.loads(response)
            print(f"[Step {step}] Received Obs: {last_obs}")
            
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(run_simulation_client(steps=5))
    print("\nFull end-to-end WebSocket loop passed!")