import numpy as np
import pandas as pd
import os

def generate_clean_dataset():
    print("[*] Generating simulation data for Deep Learning training...")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Simulate 2,000 normal records, each containing 12 distinct numeric features
    # Representing a stable system with slight natural variance
    np.random.seed(42)
    normal_records = np.random.normal(loc=0.5, scale=0.1, size=(2000, 12))
    
    # Convert to standard Pandas DataFrame
    feature_names = [f"feature_{i}" for i in range(12)]
    df = pd.DataFrame(normal_records, columns=feature_names)
    
    # Save to a clean CSV file inside our data directory
    csv_path = 'data/normal_training_data.csv'
    df.to_csv(csv_path, index=False)
    print(f"[+] Dataset created successfully at: {csv_path}")
    print(f"[+] Shape of training data matrix: {df.shape}")
    print("\nFirst 3 records as a preview:")
    print(df.head(3))

if __name__ == "__main__":
    generate_clean_dataset()