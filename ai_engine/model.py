import torch
import torch.nn as nn

class AnomalyAutoencoder(nn.Module):
    def __init__(self, input_dim=12):
        super(AnomalyAutoencoder, self).__init__()
        
        # 1. ENCODER: Compresses the high-dimensional input data
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8),
            nn.ReLU(),                  # Adds non-linearity to learn complex patterns
            nn.Linear(8, 4),
            nn.ReLU()                   # Latent space bottleneck
        )
        
        # 2. DECODER: Reconstructs the data back to original dimensions
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, input_dim)     # Output must match input_dim exactly
        )

    def forward(self, x):
        """
        Defines the data flow through the network.
        Input Tensor -> Encoder -> Compressed State -> Decoder -> Output Tensor
        """
        compressed = self.encoder(x)
        reconstructed = self.decoder(compressed)
        return reconstructed

# --- SANITY CHECK / DRY RUN ---
if __name__ == "__main__":
    print("[*] Initializing Autoencoder model architecture...")
    model = AnomalyAutoencoder(input_dim=12)
    print("[+] Architecture successfully loaded.")
    print(model)
    
    # Simulate a single user data packet (batch size = 1, features = 12)
    print("\n[*] Simulating a dry run with a dummy data tensor...")
    dummy_input = torch.randn(1, 12)
    print(f"[->] Input shape: {dummy_input.shape}")
    
    # Pass data through model
    try:
        dummy_output = model(dummy_input)
        print(f"[<-] Output shape: {dummy_output.shape}")
        
        if dummy_input.shape == dummy_output.shape:
            print("[SUCCESS] Dimension verification passed! The network structures match perfectly.")
        else:
            print("[FAIL] Dimension mismatch between input and output.")
    except Exception as e:
        print(f"[ERROR] Technical error during forward pass: {str(e)}")