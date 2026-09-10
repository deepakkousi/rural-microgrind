import React, { useEffect, useState } from 'react';
import { X, TrendingUp, AlertCircle, Info, Calendar, DollarSign, Users } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import { fetchDrilldownEvidence } from '../services/api';

export default function DrillDownModal({ loadId, onClose }) {
  const [evidence, setEvidence] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!loadId) return;
    setLoading(true);
    fetchDrilldownEvidence(loadId)
      .then((data) => setEvidence(data))
      .catch((err) => console.error("Error fetching drilldown evidence:", err))
      .finally(() => setLoading(false));
  }, [loadId]);

  if (!loadId) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl p-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-xl font-bold text-white">{evidence ? evidence.equipment_name : 'Loading Evidence...'}</h2>
              {evidence && (
                <span className={`px-2 py-0.5 text-xs font-semibold rounded-full border ${
                  evidence.load_tier === 'Critical' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                  evidence.load_tier === 'Essential' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                  'bg-sky-500/10 text-sky-400 border-sky-500/30'
                }`}>
                  {evidence.load_tier} Load
                </span>
              )}
            </div>
            {evidence && <p className="text-xs text-slate-400 mt-1">Location: {evidence.location} • Rated Power: {evidence.rated_power_kw} kW</p>}
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            aria-label="Close evidence modal"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {loading ? (
          <div className="py-12 text-center text-slate-400">Loading drill-down telemetry evidence...</div>
        ) : evidence ? (
          <div className="space-y-6">
            {/* Non-Technical Cause & Action Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-800/60 border border-slate-700/60 rounded-lg p-4">
                <div className="flex items-center space-x-2 text-amber-400 mb-2 font-semibold text-sm">
                  <AlertCircle className="h-4 w-4" />
                  <span>Identified Operational Cause</span>
                </div>
                <p className="text-sm text-slate-200">{evidence.cause_explanation}</p>
              </div>

              <div className="bg-slate-800/60 border border-slate-700/60 rounded-lg p-4">
                <div className="flex items-center space-x-2 text-emerald-400 mb-2 font-semibold text-sm">
                  <TrendingUp className="h-4 w-4" />
                  <span>Recommended Action</span>
                </div>
                <p className="text-sm text-slate-200">{evidence.recommended_action}</p>
              </div>
            </div>

            {/* Time Series Alignment Chart */}
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3 flex items-center justify-between">
                <span>24-Hour Telemetry Alignment (Actual vs Expected Schedule)</span>
                <span className="text-xs text-slate-500 font-mono">15-minute resolution</span>
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={evidence.timeseries}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="timestamp" stroke="#64748b" tickFormatter={(ts) => ts.slice(11, 16)} />
                    <YAxis stroke="#64748b" unit=" kW" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                    <Legend />
                    <Line type="monotone" dataKey="actual_kw" stroke="#38bdf8" name="Actual Load (kW)" strokeWidth={2.5} dot={false} />
                    <Line type="monotone" dataKey="expected_kw" stroke="#94a3b8" name="Target Schedule (kW)" strokeDasharray="4 4" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="occupancy_pct" stroke="#34d399" name="Occupancy (%)" yAxisId={0} opacity={0.4} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Contextual Table */}
            <div className="bg-slate-800/40 border border-slate-800 rounded-lg p-4">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Schedule & Tariff Metadata</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                <div>
                  <span className="text-xs text-slate-500 block">Original Schedule</span>
                  <span className="text-slate-200 font-medium">{evidence.schedule}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Load Classification</span>
                  <span className="text-slate-200 font-medium">{evidence.is_essential ? 'Essential (Priority)' : 'Flexible (Deferrable)'}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Location</span>
                  <span className="text-slate-200 font-medium">{evidence.location}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Rated Capacity</span>
                  <span className="text-slate-200 font-medium">{evidence.rated_power_kw} kW</span>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="py-12 text-center text-rose-400">Failed to load evidence.</div>
        )}
      </div>
    </div>
  );
}
