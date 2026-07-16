import React, { useState } from 'react';
import { Shield, Server, Lock, Activity, CheckCircle, XCircle, Cpu } from 'lucide-react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';

export default function App() {
  const [payload, setPayload] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [receipt, setReceipt] = useState(null);
  const [error, setError] = useState(null);

  // Real-world server metric categories
  const serverMetrics = [
    'CPU Load', 'RAM Usage', 'Disk IOPS', 'Net Incoming', 
    'Net Outgoing', 'Core Temp', 'Cache Misses', 'Thread Count', 
    'Sys Errors', 'Latency', 'DB Queries', 'Active Sessions'
  ];

  const generateData = () => {
    // Generates an array of 12 realistic normalized floats
    const newData = Array.from({ length: 12 }, () => parseFloat(Math.random().toFixed(4)));
    setPayload(newData);
    setReceipt(null);
    setError(null);
  };

  const submitForAnalysis = async () => {
    if (payload.length !== 12) return;
    
    setIsAnalyzing(true);
    setError(null);
    
    try {
      const response = await fetch('https://neuromancer-1.onrender.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features: payload })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Gateway validation failed');
      }

      setReceipt(data.receipt);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const chartData = payload.map((val, index) => ({
    feature: serverMetrics[index],
    value: val,
    fullMark: 1,
  }));

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans selection:bg-green-900">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <header className="flex items-center space-x-4 border-b border-gray-800 pb-6">
          <Shield className="w-10 h-10 text-green-500" />
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">Neuromancer <span className="text-green-500 text-lg">v1.0</span></h1>
            <p className="text-gray-400">Decentralized Cloud Infrastructure Validator</p>
          </div>
        </header>

        <div className="grid md:grid-cols-2 gap-8">
          
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-2xl">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold flex items-center">
                <Cpu className="w-5 h-5 mr-2 text-blue-400" /> 
                Server Telemetry
              </h2>
            </div>
            
            <p className="text-sm text-gray-400 mb-4">
              Simulate an incoming 12-dimensional telemetry packet from the master server cluster.
            </p>
            
            <button 
              onClick={generateData}
              className="w-full bg-gray-800 hover:bg-gray-700 text-white font-medium py-3 px-4 rounded-lg transition-colors border border-gray-700 mb-6 flex justify-center items-center"
            >
              <Activity className="w-4 h-4 mr-2" /> Capture Telemetry
            </button>

            {payload.length > 0 && (
              <div className="mb-6 h-64 w-full bg-gray-950 border border-gray-800 rounded-lg p-2">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="65%" data={chartData}>
                    <PolarGrid stroke="#374151" />
                    <PolarAngleAxis dataKey="feature" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
                    <Radar 
                      name="Server Status" 
                      dataKey="value" 
                      stroke="#3B82F6" 
                      fill="#3B82F6" 
                      fillOpacity={0.4} 
                    />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#60A5FA' }} 
                      itemStyle={{ color: '#60A5FA' }} 
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            )}

            {payload.length > 0 && (
              <div className="bg-gray-950 p-4 rounded-lg font-mono text-xs text-blue-300 break-all border border-gray-800">
                [{payload.join(', ')}]
              </div>
            )}

            <button 
              onClick={submitForAnalysis}
              disabled={payload.length === 0 || isAnalyzing}
              className={`w-full mt-6 flex items-center justify-center font-bold py-3 px-4 rounded-lg transition-all ${
                payload.length === 0 
                  ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
                  : 'bg-green-600 hover:bg-green-500 text-white shadow-[0_0_15px_rgba(22,163,74,0.4)]'
              }`}
            >
              {isAnalyzing ? (
                <span className="animate-pulse">Routing via Gateway...</span>
              ) : (
                <>
                  <Server className="w-5 h-5 mr-2" /> Validate via AI Core
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-4 bg-red-900/30 border border-red-800 text-red-400 rounded-lg text-sm flex items-start">
                <XCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                {error}
              </div>
            )}
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-2xl relative overflow-hidden">
            <h2 className="text-xl font-semibold flex items-center mb-6">
              <Lock className="w-5 h-5 mr-2 text-yellow-400" /> 
              Cryptographic Ledger
            </h2>
            
            {!receipt ? (
              <div className="flex flex-col items-center justify-center h-48 text-gray-600">
                <Lock className="w-12 h-12 mb-3 opacity-20" />
                <p>Awaiting verified block...</p>
              </div>
            ) : (
              <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                
                <div className={`p-4 rounded-lg border flex items-center justify-between ${
                  receipt.ml_result.anomaly_flag 
                    ? 'bg-red-900/20 border-red-500/50 text-red-400' 
                    : 'bg-green-900/20 border-green-500/50 text-green-400'
                }`}>
                  <div className="flex items-center">
                    {receipt.ml_result.anomaly_flag ? <XCircle className="w-6 h-6 mr-3" /> : <CheckCircle className="w-6 h-6 mr-3" />}
                    <div>
                      <div className="font-bold text-lg">{receipt.ml_result.status}</div>
                      <div className="text-sm opacity-80">Confidence: {receipt.ml_result.confidence_score}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs uppercase tracking-wider opacity-60">Error Rate</div>
                    <div className="font-mono">{receipt.ml_result.reconstruction_error}</div>
                  </div>
                </div>

                <div className="bg-gray-950 rounded-lg p-4 border border-gray-800">
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Block Index</div>
                  <div className="font-mono text-gray-300 mb-4">#{receipt.index}</div>
                  
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Timestamp</div>
                  <div className="font-mono text-gray-300 mb-4">{new Date(receipt.timestamp * 1000).toISOString()}</div>

                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Block Hash (SHA-256)</div>
                  <div className="font-mono text-yellow-500 text-xs break-all bg-yellow-900/10 p-2 rounded border border-yellow-700/30">
                    {receipt.hash}
                  </div>
                  
                  <div className="text-xs text-gray-500 uppercase tracking-wider mt-4 mb-1">Previous Hash (Link)</div>
                  <div className="font-mono text-gray-500 text-xs break-all">
                    {receipt.previous_hash}
                  </div>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}