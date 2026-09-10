import React, { useEffect, useState } from 'react';
import { Lightbulb, CheckCircle2, XCircle, Clock, DollarSign, ShieldCheck, AlertTriangle } from 'lucide-react';
import { fetchRecommendations, updateRecommendationStatus } from '../services/api';
import DrillDownModal from '../components/DrillDownModal';

export default function RecommendationsPage({ lang }) {
  const [recommendations, setRecommendations] = useState([]);
  const [selectedLoad, setSelectedLoad] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadRecs = () => {
    setLoading(true);
    fetchRecommendations()
      .then(setRecommendations)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRecs();
  }, []);

  const handleStatusChange = async (recId, newStatus) => {
    try {
      await updateRecommendationStatus(recId, newStatus);
      loadRecs();
    } catch (err) {
      console.error("Failed to update status:", err);
    }
  };

  if (loading) return <div className="py-12 text-center text-slate-400">Loading operational recommendations engine...</div>;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-amber-500/10 text-amber-400 rounded-lg">
            <Lightbulb className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Actionable Operational Recommendations</h2>
            <p className="text-xs text-slate-400 mt-1">
              Context-aware operational recommendations derived from component disaggregation, Time-of-Use tariffs, and room occupancy signals.
            </p>
          </div>
        </div>
      </div>

      {/* Recommendation Cards */}
      <div className="space-y-4">
        {recommendations.length === 0 ? (
          <div className="bg-slate-900 border border-amber-900/40 rounded-xl p-8 text-center text-amber-300">
            <AlertTriangle className="h-8 w-8 mx-auto mb-2 text-amber-400" />
            Recommendations paused or disabled because telemetry feed is stale or missing.
          </div>
        ) : (
          recommendations.map((rec) => (
            <div key={rec.recommendation_id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-md">
              {/* Header info */}
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3 mb-4">
                <div className="flex items-center space-x-3">
                  <span className="font-mono text-xs text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">{rec.recommendation_id}</span>
                  <h3 className="font-bold text-white text-lg">{rec.equipment_name}</h3>
                  <span className={`px-2 py-0.5 text-xs font-semibold rounded ${
                    rec.priority === 'HIGH' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30' :
                    'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                  }`}>
                    {rec.priority} PRIORITY
                  </span>
                </div>

                <div className="flex items-center space-x-3 text-xs font-mono">
                  <span className="text-slate-400">Freshness: <strong className="text-slate-200">{rec.data_freshness}</strong></span>
                  <span className="text-slate-400">Evidence Strength: <strong className="text-sky-400">{Math.round(rec.confidence * 100)} / 100</strong></span>
                  <span className={`px-2 py-0.5 font-bold rounded ${
                    rec.status === 'APPLIED' ? 'bg-emerald-500/20 text-emerald-300' :
                    rec.status === 'REJECTED' ? 'bg-rose-500/20 text-rose-300' :
                    'bg-amber-500/20 text-amber-300'
                  }`}>
                    {rec.status}
                  </span>
                </div>
              </div>

              {/* Problem & Cause explanation */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider block mb-1">WHAT Happened? (Problem)</span>
                  <p className="text-sm text-slate-200">{rec.problem}</p>
                </div>

                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider block mb-1">WHY Did It Happen? (Root Cause)</span>
                  <p className="text-sm text-slate-200">{rec.cause}</p>
                </div>
              </div>

              {/* Evidence & Action */}
              <div className="bg-slate-800/40 p-4 rounded-lg border border-slate-700/60 mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">RECOMMENDED OPERATIONAL ACTION</span>
                  <span className="text-xs text-slate-400 font-mono">Evidence Metric: {rec.evidence.metric}</span>
                </div>
                <p className="text-sm font-semibold text-white mb-2">{rec.recommended_action}</p>
                <p className="text-xs text-slate-400 font-mono bg-slate-950 p-2 rounded border border-slate-800">
                  Evidence Context: {rec.evidence.context}
                </p>
              </div>

              {/* Savings & Action Triggers */}
              <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
                <div className="flex items-center space-x-6 text-sm font-mono">
                  <div>
                    <span className="text-xs text-slate-400 block">Est. Energy Impact</span>
                    <span className="text-sky-400 font-bold">{rec.estimated_energy_saving_kwh > 0 ? `${rec.estimated_energy_saving_kwh} kWh/mo` : '0 kWh (Load Shift)'}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-400 block">Est. Cost Saving</span>
                    <span className="text-emerald-400 font-bold">₹{rec.estimated_cost_saving.toLocaleString()}/mo</span>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => setSelectedLoad(rec.equipment_id)}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded border border-slate-700"
                  >
                    Drill-Down Evidence
                  </button>
                  {rec.status === 'PENDING' && (
                    <>
                      <button
                        onClick={() => handleStatusChange(rec.recommendation_id, 'APPLIED')}
                        className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded flex items-center gap-1 shadow"
                      >
                        <CheckCircle2 className="h-3.5 w-3.5" /> Apply Action
                      </button>
                      <button
                        onClick={() => handleStatusChange(rec.recommendation_id, 'REJECTED')}
                        className="px-3 py-1.5 bg-rose-900/60 hover:bg-rose-800 text-rose-300 text-xs font-semibold rounded flex items-center gap-1 border border-rose-800"
                      >
                        <XCircle className="h-3.5 w-3.5" /> Reject
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {selectedLoad && <DrillDownModal loadId={selectedLoad} onClose={() => setSelectedLoad(null)} />}
    </div>
  );
}
