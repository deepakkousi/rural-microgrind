import React, { useEffect, useState } from 'react';
import { Activity, ShieldAlert, CheckCircle2, RefreshCw, AlertTriangle } from 'lucide-react';
import FreshnessBanner from '../components/FreshnessBanner';
import FailureSimulator from '../components/FailureSimulator';
import { fetchFreshnessStatus, fetchAnomalies } from '../services/api';

export default function QualityPage({ lang }) {
  const [freshness, setFreshness] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadQualityData = () => {
    setLoading(true);
    Promise.all([fetchFreshnessStatus(), fetchAnomalies()])
      .then(([fData, aData]) => {
        setFreshness(fData);
        setAnomalies(aData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadQualityData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-rose-500/10 text-rose-400 rounded-lg">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Data Quality & Freshness Monitoring</h2>
            <p className="text-xs text-slate-400 mt-1">
              Automated freshness status, sensor flatline detection, polarity error filtering, and edge failure simulation.
            </p>
          </div>
        </div>
      </div>

      {/* Freshness Status Banner */}
      <FreshnessBanner freshness={freshness} lang={lang} />

      {/* Interactive Failure Case Simulator */}
      <FailureSimulator onTrigger={() => loadQualityData()} />

      {/* Detected Sensor Anomalies Log */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-white text-lg flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-amber-400" /> Sensor Health & Telemetry Anomaly Log
          </h3>
          <button
            onClick={loadQualityData}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1 font-mono"
          >
            <RefreshCw className="h-3.5 w-3.5" /> Refresh Quality Audit
          </button>
        </div>

        {anomalies.length === 0 ? (
          <div className="py-8 text-center bg-slate-950 rounded-lg border border-slate-800 text-emerald-400 font-medium text-sm flex items-center justify-center gap-2">
            <CheckCircle2 className="h-4 w-4" /> All sensor telemetry feeds are healthy with zero abnormal readings.
          </div>
        ) : (
          <div className="space-y-3">
            {anomalies.map((anom, idx) => (
              <div key={idx} className="bg-slate-950 border border-rose-900/40 rounded-lg p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-white text-sm">{anom.sensor}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30">
                      {anom.issue_type}
                    </span>
                    <span className="text-xs text-slate-500 font-mono">Severity: {anom.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{anom.description}</p>
                </div>

                <div className="text-right shrink-0">
                  <span className="text-xs text-slate-400 block font-mono">Action Required:</span>
                  <span className="text-xs text-amber-400 font-semibold">{anom.recommended_action}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
