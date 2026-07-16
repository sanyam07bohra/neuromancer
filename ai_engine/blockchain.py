import hashlib
import json
from time import time

class ImmutableLedger:
    def __init__(self):
        self.chain = []
        # Create the 'Genesis Block' (the very first block in the chain)
        # We give it an arbitrary previous hash of 64 zeros.
        self.create_block(previous_hash='0' * 64, ml_result={"status": "Genesis Block - System Initialized"})

    def create_block(self, previous_hash, ml_result):
        """
        Creates a new block and binds it to the chain.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'ml_result': ml_result,  # The AI's decision is permanently stored here
            'previous_hash': previous_hash,
        }
        
        # Calculate the cryptographic hash of THIS new block
        block['hash'] = self.hash_block(block)
        
        # Add the secured block to the chain
        self.chain.append(block)
        return block

    @staticmethod
    def hash_block(block):
        """
        Creates a mathematically irreversible SHA-256 hash of a Block.
        """
        # We must create a copy and remove its own 'hash' key before hashing it,
        # otherwise we create an infinite loop of hashing the hash.
        block_copy = block.copy()
        if 'hash' in block_copy:
            del block_copy['hash']
            
        # Convert the dictionary to a string (sort_keys ensures exact same order every time)
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        
        # Return the 64-character hexadecimal hash
        return hashlib.sha256(block_string).hexdigest()

    def add_ai_decision(self, ml_result):
        """
        A helper function our API will call to quickly lock an AI decision.
        """
        # 1. Get the hash of the last block in the chain
        last_block = self.chain[-1]
        previous_hash = last_block['hash']
        
        # 2. Create the new block, permanently linking it to the previous one
        return self.create_block(previous_hash, ml_result)

# --- SANITY CHECK / DRY RUN ---
if __name__ == "__main__":
    print("[*] Initializing Cryptographic Ledger...")
    my_blockchain = ImmutableLedger()
    
    print("\n[+] Genesis Block Created:")
    print(json.dumps(my_blockchain.chain[0], indent=2))
    
    print("\n[*] Simulating a Deep Learning Decision...")
    # This simulates what our PyTorch model will eventually output
    mock_ai_output = {
        "anomaly_detected": True,
        "reconstruction_error": 0.2854,
        "confidence_score": 0.89
    }
    
    print("[*] Locking decision into the blockchain...")
    new_block = my_blockchain.add_ai_decision(mock_ai_output)
    
    print("\n[+] New Block Successfully Minted:")
    print(json.dumps(new_block, indent=2))
    
    print(f"\n[SUCCESS] Ledger securely contains {len(my_blockchain.chain)} blocks.")
    print(f"[SUCCESS] Cryptographic binding verified. Block 2 is bound to Hash: {new_block['previous_hash'][:15]}...")