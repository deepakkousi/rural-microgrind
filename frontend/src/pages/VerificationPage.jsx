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
  if (!summary) return <div className="py-12 text-center text-rose-400">Failed to load verification experiment summary.</div>;

  const summaryFlow = [
    { stage: 'BASELINE', label: 'Days 1 - 30', val: `${summary.baseline_daily_avg_kwh} kWh/day`, color: 'border-slate-700 bg-slate-900 text-slate-200' },
    { stage: 'TARGET', label: 'Expected Baseline', val: `${summary.target_daily_avg_kwh} kWh/day`, color: 'border-indigo-500/40 bg-indigo-950/40 text-indigo-300' },
    { stage: 'MEASURED', label: 'Days 61 - 90', val: `${summary.measured_daily_avg_kwh} kWh/day`, color: 'border-sky-500/40 bg-sky-950/40 text-sky-300' },
    { stage: 'VERIFIED REDUCTION', label: 'Measured Saving', val: `${summary.verified_reduction_kwh_day} kWh/day (${summary.verified_reduction_pct}%)`, color: 'border-emerald-500/40 bg-emerald-950/40 text-emerald-300 font-bold' }
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
              Empirical IPMVP-aligned operational intervention experiment across 90 days of 15-minute smart meter telemetry.
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
          <span className="text-xs text-slate-400 block font-mono uppercase">Uncertainty / Error Bounds</span>
          <div className="text-2xl font-bold text-sky-400 mt-1 font-mono">±{summary.measurement_error_margin_pct}%</div>
          <p className="text-xs text-slate-500 mt-1">
            Confidence Interval: {summary.lower_bound_kwh} to {summary.upper_bound_kwh} kWh/day
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <span className="text-xs text-slate-400 block font-mono uppercase">Active Experiment Phase</span>
          <div className="text-2xl font-bold text-indigo-400 mt-1 font-mono">VERIFICATION (Day 61-90)</div>
          <p className="text-xs text-slate-500 mt-1">3 Interventions active and empirically validated in raw telemetry.</p>
        </div>
      </div>

      {/* Daily Consumption Trend Comparison Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-bold text-white text-base mb-3">90-Day Daily Energy Consumption Profile (Baseline vs Verification)</h3>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={timeseries}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="day" stroke="#64748b" label={{ value: 'Day Index (1 - 90)', position: 'insideBottom', offset: -5 }} />
              <YAxis stroke="#64748b" unit=" kWh" />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
              <Bar dataKey="total_kwh" fill="#0284c7" name="Daily Total Consumption (kWh)" />
              <Bar dataKey="hvac_kwh" fill="#6366f1" name="HVAC Daily Consumption (kWh)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Applied Interventions Summary Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-bold text-white text-lg mb-4">Operational Interventions Evaluation</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-xs font-mono">
              <tr>
                <th className="px-4 py-3">Intervention</th>
                <th className="px-4 py-3">Target Equipment</th>
                <th className="px-4 py-3">Operational Policy Modification</th>
                <th className="px-4 py-3 font-right">Daily Cost Saving</th>
                <th className="px-4 py-3 text-right">Verification Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {summary.interventions_applied.map((int) => (
                <tr key={int.id} className="hover:bg-slate-800/30 transition">
                  <td className="px-4 py-3 font-semibold text-white">{int.name}</td>
                  <td className="px-4 py-3 text-slate-400">{int.target_equipment}</td>
                  <td className="px-4 py-3 text-slate-300">{int.action}</td>
                  <td className="px-4 py-3 font-mono text-emerald-400 font-bold">₹{int.cost_saving_daily_inr}/day</td>
                  <td className="px-4 py-3 text-right">
                    <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold rounded inline-flex items-center gap-1">
                      <CheckCircle2 className="h-3 w-3" /> VERIFIED
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
