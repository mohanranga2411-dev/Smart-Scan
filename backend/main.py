import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.environment import Environment
from backend.receiver import Receiver

app = FastAPI(title="Smart Scan RF Engine")

# Instantiate persistent core environment and receiver bridge
environment = Environment(num_bands=100, noise_level=0.20)
receiver = Receiver(environment=environment)

@app.get("/")
def read_root():
    return {"status": "Smart Scan API is running", "time": environment.current_time}

@app.websocket("/ws/scan")
async def websocket_scan_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected to WebSocket pipeline.")
    
    try:
        while True:
            # Receive raw action payload from client
            data = await websocket.receive_text()
            action = json.loads(data)

            # Process action through Receiver -> Environment pipeline
            observation = receiver.send_action(action)

            # Transmit observation back to client
            await websocket.send_json(observation)

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket.")
    except Exception as e:
        print(f"Error in WebSocket loop: {e}")
        await websocket.close()