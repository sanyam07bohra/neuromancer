const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 5000;

// 1. Middleware Setup
// CORS allows our future React app (running on a different port) to talk to this API
app.use(cors()); 
// Allows Express to parse incoming JSON payloads
app.use(express.json());

console.log("\n=========================================");
console.log("   NEUROMANCER - NODE.JS API GATEWAY");
console.log("=========================================\n");

// 2. The Main Gateway Route
app.post('/api/verify', async (req, res) => {
    try {
        console.log('[*] Incoming data received from frontend client...');
        
        // Extract the data from the user's request
        const sensorData = req.body.features;

        // Security Check: Ensure the payload is exactly what the AI expects
        if (!sensorData || !Array.isArray(sensorData) || sensorData.length !== 12) {
            console.log('[!] Blocked malformed request.');
            return res.status(400).json({ error: "Invalid payload. Expected an array of 12 features." });
        }

        // 3. Forward the clean data to the Python AI Engine (Running on Port 8000)
        console.log('[*] Payload verified. Routing to Python AI Core...');
        
        const aiResponse = await axios.post('https://neuromancer.onrender.com', {
            features: sensorData
        });

        console.log('[+] Cryptographic receipt received from Python AI.');
        
        // 4. Send the immutable blockchain receipt back to the React frontend
        res.status(200).json(aiResponse.data);

    } catch (error) {
        console.error('[ERROR] Gateway routing failed:', error.message);
        // Fallback error if the Python server is off or crashes
        res.status(503).json({ 
            error: "AI Engine Offline or Unreachable. Please ensure the Python core is running." 
        });
    }
});

// 3. Start the Server
app.listen(PORT, () => {
    console.log(`[GATEWAY] Security proxy successfully listening on http://localhost:${PORT}`);
    console.log(`[GATEWAY] Standing by to route traffic...`);
});