🛡️ Neuromancer

Decentralized Cloud Infrastructure Validator

Neuromancer is a full-stack, cloud-native microservice architecture designed to ingest real-time server telemetry, detect infrastructure anomalies using Deep Learning (PyTorch), and permanently lock those security verdicts into an immutable cryptographic ledger.

🚀 Live Deployment

Frontend Dashboard (Vercel): https://neuromancer-ochre.vercel.app/

Node.js API Gateway (Render): https://neuromancer-1.onrender.com

Python AI Core (Render): https://neuromancer.onrender.com

🧠 System Architecture

This project is built using a modern Microservices approach, completely separating the user interface, the security routing, and the heavy machine learning computations.

The Client (React & Recharts): A dark-themed, responsive dashboard that visualizes a 12-dimensional vector of server telemetry (CPU, RAM, Network Traffic, etc.) using dynamic radar charts.

The API Gateway (Node.js & Express): Acts as a secure middleware proxy. It sanitizes incoming telemetry streams, handles CORS, and routes verified payloads to the internal AI cluster.

The AI Core (Python & FastAPI): The brain of the operation. It houses a trained PyTorch Neural Network and a custom Blockchain.

The Autoencoder: A deep learning model trained on normal server behavior. It calculates a "Reconstruction Error" for incoming data to flag anomalies.

The Cryptographic Ledger: A custom blockchain implementation. Every AI decision is hashed (SHA-256) and chained to the previous block, creating an unalterable audit trail of system health.

🛠️ Technology Stack

Frontend:

React.js

Tailwind CSS (Styling & UI)

Recharts (Data Visualization)

Lucide React (Iconography)

Backend / Middleware:

Node.js

Express.js

Axios

AI & Cryptography Core:

Python 3

PyTorch (Deep Learning / Autoencoder)

FastAPI (High-performance API generation)

Pandas & NumPy (Data processing)

Hashlib (SHA-256 Cryptography)

💻 Local Setup & Installation

Because Neuromancer uses a microservice architecture, you will need to start three separate local servers to run the complete pipeline.

1. Start the Python AI Core

cd ai_engine
python -m venv venv
# On Windows: .\venv\Scripts\activate | On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000


2. Start the Node.js API Gateway

Open a new terminal window:

cd gateway
npm install
node server.js


3. Start the React Frontend

Open a third terminal window:

cd client
npm install
npm start


The application will now be running on http://localhost:3000.

🛡️ Security & Blockchain Mechanics

The ledger guarantees that once the AI flags an anomaly, it cannot be silently deleted or altered by a bad actor.

If a hacker attempts to modify a past AI verdict stored in the database, the SHA-256 hash of that block will instantly change. Because the next block mathematically relies on that original hash, the entire chain will immediately break, exposing the tampering.