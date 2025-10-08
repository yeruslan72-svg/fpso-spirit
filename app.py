# AVCS DNA v6.0 PRO — Data Simulator
# Simulates Bentley Nevada / OSIsoft / OPC-UA data streams

import asyncio
import json
import random
import time
from datetime import datetime
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI(title="AVCS DNA - Industrial Data Gateway v6.0")

# --- Simulated tag groups ---
TAGS = {
    "VIB": ["VIB_PUMP_A_X", "VIB_PUMP_A_Y", "VIB_PUMP_B_X", "VIB_PUMP_B_Y"],
    "TEMP": ["TEMP_PUMP_A", "TEMP_MOTOR_A"],
    "RPM": ["RPM_PUMP_A"],
    "PRESS": ["PRESS_MAIN_LINE"],
}

def generate_sample():
    """Simulate real sensor data"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "VIB_PUMP_A_X": round(random.uniform(0.3, 7.0), 2),
        "VIB_PUMP_A_Y": round(random.uniform(0.3, 7.0), 2),
        "VIB_PUMP_B_X": round(random.uniform(0.3, 7.0), 2),
        "VIB_PUMP_B_Y": round(random.uniform(0.3, 7.0), 2),
        "TEMP_PUMP_A": round(random.uniform(55, 110), 1),
        "TEMP_MOTOR_A": round(random.uniform(50, 100), 1),
        "RPM_PUMP_A": int(random.uniform(2700, 3100)),
        "PRESS_MAIN_LINE": round(random.uniform(5.5, 9.0), 2),
    }

@app.get("/api/latest")
async def get_latest():
    """REST endpoint for latest snapshot"""
    return generate_sample()

@app.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for live stream"""
    await websocket.accept()
    while True:
        sample = generate_sample()
        await websocket.send_text(json.dumps(sample))
        await asyncio.sleep(0.3)  # 3.3Hz update rate

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
