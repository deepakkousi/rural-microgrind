import React, { useEffect, useState } from 'react';
import { Layers, Activity, Eye, CheckCircle2 } from 'lucide-react';
import { fetchDisaggregation } from '../services/api';
import DrillDownModal from '../components/DrillDownModal';

export default function DisaggregationPage({ lang }) {
  const [data, setData] = useState(null);
  const [selectedLoad, setSelectedLoad] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDisaggregation()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="py-12 text-center text-slate-400">Loading load disaggregation engine...</div>;
  if (!data) return <div className="py-12 text-center text-rose-400">Failed to load disaggregation data.</div>;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-sky-500/10 text-sky-400 rounded-lg">
            <Layers className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Scenario Load Disaggregation Engine</h2>
            <p className="text-xs text-slate-400 mt-1">
              Methodology: Scenario-based synthetic load disaggregation using known component meter channels, equipment schedules, and contextual occupancy/tariff signals.
            </p>
          </div>
        </div>
      </div>

      {/* Accuracy Evaluation Metrics (MAE, RMSE, MAPE) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 block font-mono uppercase">Mean Absolute Error (MAE)</span>
          <div className="text-2xl font-bold text-sky-400 mt-1 font-mono">{data.evaluation_metrics.mae_kw} kW</div>
          <p className="text-xs text-slate-500 mt-1">Average magnitude of estimation error across 15-min intervals.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 block font-mono uppercase">Root Mean Square Error (RMSE)</span>
          <div className="text-2xl font-bold text-indigo-400 mt-1 font-mono">{data.evaluation_metrics.rmse_kw} kW</div>
          <p className="text-xs text-slate-500 mt-1">Penalizes large outlier disaggregation deviations.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-400 block font-mono uppercase">Mean Absolute Pct Error (MAPE)</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1 font-mono">{data.evaluation_metrics.mape_pct}%</div>
          <p className="text-xs text-slate-500 mt-1">High accuracy disaggregation benchmark score.</p>
        </div>
      </div>

      {/* Tier Disaggregation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-rose-950/60 rounded-xl p-5">
          <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">Critical Load Tier</span>
          <div className="text-3xl font-bold text-white mt-2 font-mono">{data.tiers.critical.kw} kW</div>
          <div className="text-xs text-rose-400 mt-1 font-mono">{data.tiers.critical.pct}% of total grid load</div>
          <p className="text-xs text-slate-400 mt-3">24/7 Uninterruptible power (Server racks, core WiFi switches, emergency comms).</p>
        </div>

        <div className="bg-slate-900 border border-amber-950/60 rounded-xl p-5">
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">Essential Load Tier</span>
          <div className="text-3xl font-bold text-white mt-2 font-mono">{data.tiers.essential.kw} kW</div>
          <div className="text-xs text-amber-400 mt-1 font-mono">{data.tiers.essential.pct}% of total grid load</div>
          <p className="text-xs text-slate-400 mt-3">Priority operational loads (Security corridor lighting, water pump, mess kitchen).</p>
        </div>

        <div className="bg-slate-900 border border-sky-950/60 rounded-xl p-5">
          <span className="text-xs font-bold text-sky-400 uppercase tracking-wider block">Flexible Load Tier</span>
          <div className="text-3xl font-bold text-white mt-2 font-mono">{data.tiers.flexible.kw} kW</div>
          <div className="text-xs text-sky-400 mt-1 font-mono">{data.tiers.flexible.pct}% of total grid load</div>
          <p className="text-xs text-slate-400 mt-3">Deferrable / Schedulable loads (Academic HVAC chillers, workshop CNC, 3D printers).</p>
        </div>
      </div>

      {/* Equipment Level Breakdown Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-bold text-white text-lg mb-4">Disaggregated Equipment Telemetry Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-xs font-mono">
              <tr>
                <th className="px-4 py-3">Equipment</th>
                <th className="px-4 py-3">Tier</th>
                <th className="px-4 py-3">Location</th>
                <th className="px-4 py-3">Rated Power</th>
                <th className="px-4 py-3">Active Load</th>
                <th className="px-4 py-3">Contribution</th>
                <th className="px-4 py-3 text-right">Drill-Down</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {data.detailed_loads.map((eq) => (
                <tr key={eq.equipment_id} className="hover:bg-slate-800/30 transition">
                  <td className="px-4 py-3 font-semibold text-white">{eq.equipment_name}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 text-xs font-semibold rounded ${
                      eq.load_tier === 'Critical' ? 'bg-rose-500/10 text-rose-400' :
                      eq.load_tier === 'Essential' ? 'bg-amber-500/10 text-amber-400' :
                      'bg-sky-500/10 text-sky-400'
                    }`}>
                      {eq.load_tier}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-400">{eq.location}</td>
                  <td className="px-4 py-3 font-mono">{eq.rated_power_kw} kW</td>
                  <td className="px-4 py-3 font-mono text-sky-400 font-bold">{eq.current_power_kw} kW</td>
                  <td className="px-4 py-3 font-mono">{eq.percentage}%</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => setSelectedLoad(eq.equipment_id)}
                      className="px-2.5 py-1 bg-sky-600/80 hover:bg-sky-500 text-white text-xs font-medium rounded flex items-center gap-1 ml-auto"
                    >
                      <Eye className="h-3.5 w-3.5" /> Evidence
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Drill-down modal */}
      {selectedLoad && <DrillDownModal loadId={selectedLoad} onClose={() => setSelectedLoad(null)} />}
    </div>
  );
}
