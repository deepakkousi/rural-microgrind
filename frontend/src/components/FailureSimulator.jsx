import React, { useState } from 'react';
import { AlertCircle, RefreshCw, Radio, Flame } from 'lucide-react';
import { simulateEdgeFailure } from '../services/api';

export default function FailureSimulator({ onTrigger }) {
  const [activeFailure, setActiveFailure] = useState('RESET');
  const [loading, setLoading] = useState(false);

  const handleSimulate = async (type, channel = "water_pump_kw") => {
    setLoading(true);
    try {
      await simulateEdgeFailure(type, 16, channel);
      setActiveFailure(type);
      if (onTrigger) onTrigger(type);
    } catch (err) {
      console.error("Error triggering edge failure:", err);
    } finally {
      setLoading(false);
    }
  };

  const failures = [
    { id: 'RESET', label: 'Normal / Recovered', desc: 'Restore clean telemetry feeds', color: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' },
    { id: 'MISSING_DATA', label: 'Missing Meter Data', desc: 'Simulate telemetry signal dropout', color: 'bg-rose-500/20 text-rose-300 border-rose-500/30' },
    { id: 'STALE_DATA', label: 'Stale Telemetry', desc: 'Simulate 47-min buffer delay', color: 'bg-amber-500/20 text-amber-300 border-amber-500/30' },
    { id: 'STUCK_SENSOR', label: 'Stuck Flatline Sensor', desc: 'Simulate CT transducer flatline', color: 'bg-orange-500/20 text-orange-300 border-orange-500/30' },
    { id: 'NEGATIVE_READING', label: 'Negative Reading', desc: 'Simulate CT wiring polarity inversion', color: 'bg-purple-500/20 text-purple-300 border-purple-500/30' },
    { id: 'TARIFF_REVISION', label: 'Critical Peak Tariff', desc: 'Simulate sudden tariff rate hike', color: 'bg-sky-500/20 text-sky-300 border-sky-500/30' }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 my-6">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Radio className="h-5 w-5 text-sky-400" />
          <h3 className="font-bold text-white text-base">Edge Case & Failure Simulator</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">Phase 11 Protocol Test</span>
      </div>
      <p className="text-xs text-slate-400 mb-4">
        Inject simulated sensor anomalies and network dropouts to verify system resilience, automated freshness downgrades, and safety fallback execution.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
        {failures.map((f) => (
          <button
            key={f.id}
            onClick={() => handleSimulate(f.id)}
            disabled={loading}
            className={`p-3 rounded-lg border text-left transition-all ${
              activeFailure === f.id ? f.color + ' ring-2 ring-sky-400' : 'bg-slate-800/40 border-slate-700/60 text-slate-300 hover:bg-slate-800'
            }`}
          >
            <div className="font-semibold text-sm flex items-center justify-between">
              <span>{f.label}</span>
              {activeFailure === f.id && <span className="text-xs font-bold px-1.5 py-0.5 rounded bg-sky-500 text-white">ACTIVE</span>}
            </div>
            <p className="text-xs text-slate-400 mt-1">{f.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
