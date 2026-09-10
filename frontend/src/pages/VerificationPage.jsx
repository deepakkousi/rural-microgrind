import React, { useEffect, useState } from 'react';
import { ShieldCheck, TrendingDown, DollarSign, AlertCircle, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import { fetchVerificationSummary, fetchVerificationTimeseries } from '../services/api';

export default function VerificationPage({ lang }) {
  const [summary, setSummary] = useState(null);
  const [timeseries, setTimeseries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchVerificationSummary(), fetchVerificationTimeseries()])
      .then(([sumData, tsData]) => {
        setSummary(sumData);
        setTimeseries(tsData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="py-12 text-center text-slate-400">Loading energy reduction verification model...</div>;

  if (!summary || summary.status === "DATA_UNAVAILABLE") {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center max-w-2xl mx-auto my-12">
        <AlertCircle className="h-10 w-10 text-rose-400 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-white mb-1">Verification Unavailable</h3>
        <p className="text-sm text-slate-400 mb-4">{summary ? summary.message : "Insufficient meter data to compute baseline verification."}</p>
        <div className="bg-slate-950 p-3 rounded text-xs font-mono text-slate-500 border border-slate-800">
          Verification unavailable — insufficient meter data.
        </div>
      </div>
    );
  }

  const summaryFlow = [
    { stage: 'BASELINE', label: 'Days 1 - 30 (Historical)', val: `${summary.baseline_daily_avg_kwh} kWh/day`, color: 'border-slate-700 bg-slate-900 text-slate-200' },
    { stage: 'TARGET', label: '15% Goal Target', val: `${summary.target_daily_avg_kwh} kWh/day`, color: 'border-indigo-500/40 bg-indigo-950/40 text-indigo-300' },
    { stage: 'MEASURED', label: 'Days 61 - 90 (Actual)', val: `${summary.measured_daily_avg_kwh} kWh/day`, color: 'border-sky-500/40 bg-sky-950/40 text-sky-300' },
    { stage: 'VERIFIED REDUCTION', label: 'Measured Energy Saving', val: `${summary.verified_reduction_kwh_day} kWh/day (${summary.verified_reduction_pct}%)`, color: 'border-emerald-500/40 bg-emerald-950/40 text-emerald-300 font-bold' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Baseline vs. Measured Energy Reduction Experiment</h2>
            <p className="text-xs text-slate-400 mt-1">
              Empirical historical baseline model across 90 days of 15-minute smart meter telemetry.
            </p>
          </div>
        </div>
      </div>

      {/* Mandatory Flow Banner: BASELINE -> TARGET -> MEASURED -> VERIFIED */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryFlow.map((s, i) => (
          <div key={i} className={`border rounded-xl p-5 flex flex-col justify-between ${s.color}`}>
            <div>
              <span className="text-xs uppercase tracking-wider font-mono font-bold block">{s.stage}</span>
              <span className="text-xs text-slate-400 block mt-0.5">{s.label}</span>
              <div className="text-xl font-bold mt-3 font-mono">{s.val}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Verified Financial & Error Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <span className="text-xs text-slate-400 block font-mono uppercase">Verified Daily Cost Saving</span>
          <div className="text-3xl font-bold text-emerald-400 mt-1 font-mono">₹{summary.cost_saving_daily.toLocaleString()}/day</div>
          <p className="text-xs text-slate-500 mt-1">30-Day Verification Period Total: ₹{summary.cost_saving_total.toLocaleString()}</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <span className="text-xs text-slate-400 block font-mono uppercase">Target Achievement Ratio</span>
          <div className="text-3xl font-bold text-sky-400 mt-1 font-mono">{summary.target_achievement_pct}%</div>
          <p className="text-xs text-slate-500 mt-1">Target Reduction: {summary.error_analysis.target_reduction_kwh_day} kWh/day</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <span className="text-xs text-slate-400 block font-mono uppercase">Error Analysis & Uncertainty</span>
          <div className="text-xl font-bold text-indigo-400 mt-1 font-mono">Err: {summary.error_analysis.absolute_error_kwh} kWh ({summary.error_analysis.percentage_error}%)</div>
          <p className="text-xs text-slate-500 mt-1">{summary.error_analysis.sensor_uncertainty}</p>
        </div>
      </div>

      {/* Applied Interventions Evaluation Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-white text-lg">Operational Interventions Evaluation</h3>
            <p className="text-xs text-slate-400">Explicitly distinguishes Energy Reduction (kWh) from Cost Reduction (Load Shift).</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-xs font-mono">
              <tr>
                <th className="px-4 py-3">Intervention</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Energy Impact (kWh/day)</th>
                <th className="px-4 py-3 font-right">Cost Impact (₹/day)</th>
                <th className="px-4 py-3">Explanation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {summary.interventions_applied.map((int) => (
                <tr key={int.id} className="hover:bg-slate-800/30 transition">
                  <td className="px-4 py-3 font-semibold text-white">
                    {int.name}
                    <span className="block text-xs text-slate-500">{int.target_equipment}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 text-xs font-bold rounded ${
                      int.type === 'ENERGY_REDUCTION' ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30' :
                      'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    }`}>
                      {int.type === 'ENERGY_REDUCTION' ? 'ENERGY REDUCTION' : 'COST REDUCTION (LOAD SHIFT)'}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-mono font-bold text-sky-400">
                    {int.energy_saving_kwh_day > 0 ? `-${int.energy_saving_kwh_day} kWh` : '0 kWh (Load Shift)'}
                  </td>
                  <td className="px-4 py-3 font-mono text-emerald-400 font-bold">
                    -₹{int.cost_saving_daily_inr}/day
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-400">{int.explanation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mathematical Reconciliation Panel */}
      {summary.reconciliation && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-bold text-white text-base">Mathematical Reconciliation: Feeder Total vs. Submeter Interventions</h3>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded">
              Reconciled Balance
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 font-mono text-sm">
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
              <span className="text-xs text-slate-400 block font-sans">Main Feeder Net Reduction</span>
              <div className="text-lg font-bold text-sky-400 mt-1">
                {summary.reconciliation.main_meter_reduction_kwh_day} kWh/day ({summary.reconciliation.main_meter_reduction_pct}%)
              </div>
              <span className="text-xs text-emerald-400 mt-0.5 block font-sans">₹{summary.reconciliation.main_meter_daily_cost_saving_inr.toLocaleString()}/day saving</span>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
              <span className="text-xs text-slate-400 block font-sans">Sum of Submeter Interventions</span>
              <div className="text-lg font-bold text-indigo-400 mt-1">
                {summary.reconciliation.sum_submeter_reductions_kwh_day} kWh/day
              </div>
              <span className="text-xs text-emerald-400 mt-0.5 block font-sans">₹{summary.reconciliation.sum_submeter_daily_cost_savings_inr.toLocaleString()}/day subtotal</span>
            </div>

            <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
              <span className="text-xs text-slate-400 block font-sans">Background & Unmetered Variance</span>
              <div className="text-lg font-bold text-amber-400 mt-1">
                {summary.reconciliation.background_unmetered_variance_kwh_day} kWh/day
              </div>
              <span className="text-xs text-amber-400 mt-0.5 block font-sans">₹{summary.reconciliation.background_cost_variance_inr}/day net variance</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed border-t border-slate-800/80 pt-3">
            {summary.reconciliation.explanation}
          </p>
        </div>
      )}
    </div>
  );
}
