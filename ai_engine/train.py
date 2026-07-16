import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

# Import the architecture we built yesterday
from model import AnomalyAutoencoder 

def train_model():
    print("[*] Initializing Training Sequence...")
    
    # 1. Load the Training Data from Day 1
    data_path = 'data/normal_training_data.csv'
    if not os.path.exists(data_path):
        print(f"[ERROR] Could not find {data_path}. Did you run prepare_data.py?")
        return
        
    df = pd.read_csv(data_path)
    # Convert Pandas DataFrame to a PyTorch Tensor
    tensor_data = torch.tensor(df.values, dtype=torch.float32)
    print(f"[+] Loaded {len(tensor_data)} records for training.")

    # 2. Initialize Model, Loss Function, and Optimizer
    model = AnomalyAutoencoder(input_dim=12)
    criterion = nn.MSELoss() # Mean Squared Error calculates the reconstruction difference
    optimizer = optim.Adam(model.parameters(), lr=0.01) # Learning rate of 0.01

    # 3. The Training Loop
    epochs = 50
    print(f"[*] Beginning training for {epochs} epochs...")
    
    for epoch in range(epochs):
        optimizer.zero_grad()               # Clear old gradients
        reconstructed = model(tensor_data)  # Forward pass: compress and rebuild
        loss = criterion(reconstructed, tensor_data) # Calculate how badly it did
        
        loss.backward()                     # Backpropagation: calculate adjustments
        optimizer.step()                    # Update the weights
        
        # Print progress every 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"    Epoch [{epoch+1}/{epochs}], Loss/Error: {loss.item():.4f}")

    print("[+] Training Complete!")

    # 4. Calculate the Anomaly Threshold
    # Let's find the maximum error it made on this 'normal' dataset
    model.eval() # Put model in evaluation mode
    with torch.no_grad():
        final_reconstruction = model(tensor_data)
        # Calculate error for each individual row
        row_errors = torch.mean((tensor_data - final_reconstruction) ** 2, dim=1)
        max_normal_error = torch.max(row_errors).item()
        
    # We set our threshold slightly higher than the max normal error (adding a 20% buffer)
    recommended_threshold = max_normal_error * 1.2 
    print(f"[*] Max error on normal data: {max_normal_error:.4f}")
    print(f"[!] Recommended Anomaly Threshold set to: {recommended_threshold:.4f}")

    # 5. Save the Brain (Weights) and Config
    os.makedirs('models', exist_ok=True)
    
    # Save the PyTorch weights
    model_path = 'models/autoencoder.pth'
    torch.save(model.state_dict(), model_path)
    
    # Save the threshold so our API knows what to use later
    config = {"anomaly_threshold": recommended_threshold}
    with open('models/config.json', 'w') as f:
        json.dump(config, f)
        
    print(f"[SUCCESS] Model weights saved to {model_path}")
    print("[SUCCESS] Threshold configuration saved to models/config.json")

if __name__ == "__main__":
    train_model()