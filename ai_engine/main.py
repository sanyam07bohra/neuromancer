from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import json
import os

# Import our custom modules from Days 2 & 4
from model import AnomalyAutoencoder
from blockchain import ImmutableLedger

# 1. Initialize the FastAPI Server
app = FastAPI(title="Neuromancer AI Core", version="1.0.0")

# 2. System Startup: Load Brain and Vault
print("[*] Booting Neuromancer Engine...")

# Load the Blockchain
blockchain = ImmutableLedger()

# Load the AI Configuration (Threshold)
config_path = "models/config.json"
if not os.path.exists(config_path):
    raise RuntimeError("config.json not found! Did you run train.py on Day 3?")

with open(config_path, "r") as f:
    config = json.load(f)
THRESHOLD = config["anomaly_threshold"]

# Load the PyTorch Model
model = AnomalyAutoencoder(input_dim=12)
model_path = "models/autoencoder.pth"
if not os.path.exists(model_path):
    raise RuntimeError("autoencoder.pth not found! Did you run train.py on Day 3?")

# Load weights and set to evaluation mode (no more training)
model.load_state_dict(torch.load(model_path))
model.eval() 
print(f"[+] AI Brain loaded. Anomaly Threshold locked at: {THRESHOLD:.4f}")

# 3. Define the Input Data Structure using Pydantic
class SensorData(BaseModel):
    # We expect exactly a list of 12 numbers (floats)
    features: list[float]

# 4. The Main API Endpoint
@app.post("/api/v1/analyze")
async def analyze_data(data: SensorData):
    """
    Receives 12-feature data, scores it with PyTorch, and secures it on the Blockchain.
    """
    if len(data.features) != 12:
        raise HTTPException(status_code=400, detail="Data must contain exactly 12 features.")

    # A. AI Phase: Convert to tensor and calculate reconstruction error
    input_tensor = torch.tensor([data.features], dtype=torch.float32)
    
    with torch.no_grad():
        reconstructed = model(input_tensor)
        # Calculate Mean Squared Error for this single request
        loss = torch.mean((input_tensor - reconstructed) ** 2).item()

    # Determine if it's an anomaly based on the threshold we learned on Day 3
    is_anomaly = bool(loss > THRESHOLD)
    
    # Calculate a simple 0-100% confidence score
    confidence = max(0.0, min(100.0, (1.0 - (loss / (THRESHOLD * 2))) * 100))

    ml_result = {
        "status": "Anomaly Detected" if is_anomaly else "Normal",
        "anomaly_flag": is_anomaly,
        "reconstruction_error": round(loss, 4),
        "confidence_score": f"{round(confidence, 2)}%"
    }

    # B. Blockchain Phase: Lock the decision permanently
    secured_block = blockchain.add_ai_decision(ml_result)

    # Return the cryptographic receipt to the user
    return {
        "message": "AI Analysis complete and secured on the ledger.",
        "receipt": secured_block
    }

# A simple health check route
@app.get("/")
async def health_check():
    return {"status": "Neuromancer Core Online", "blocks_secured": len(blockchain.chain)}