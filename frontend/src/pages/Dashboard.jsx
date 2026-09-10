import React, { useEffect, useState } from 'react';
import { Zap, Sun, Shield, DollarSign, Activity, AlertTriangle, ArrowRight, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import FreshnessBanner from '../components/FreshnessBanner';
import RoleViewWrapper from '../components/RoleViewWrapper';
import DrillDownModal from '../components/DrillDownModal';
import { fetchMeterData, fetchDisaggregation, fetchRecommendations, fetchVerificationSummary, fetchFreshnessStatus } from '../services/api';
import { translations } from '../i18n/translations';

export default function Dashboard({ currentRole, lang, onNavigate }) {
  const t = translations[lang] || translations.en;
  const [telemetry, setTelemetry] = useState([]);
  const [disaggregation, setDisaggregation] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [verification, setVerification] = useState(null);
  const [freshness, setFreshness] = useState(null);
  const [selectedLoad, setSelectedLoad] = useState(null);

  useEffect(() => {
    fetchMeterData(48).then(setTelemetry).catch(console.error);
    fetchDisaggregation().then(setDisaggregation).catch(console.error);
    fetchRecommendations().then(setRecommendations).catch(console.error);
    fetchVerificationSummary().then(setVerification).catch(console.error);
    fetchFreshnessStatus().then(setFreshness).catch(console.error);
  }, []);

  const latest = telemetry.length > 0 ? telemetry[telemetry.length - 1] : {};

  const pieData = disaggregation ? [
    { name: 'Critical Load', value: disaggregation.tiers.critical.kw, color: '#f43f5e' },
    { name: 'Essential Load', value: disaggregation.tiers.essential.kw, color: '#f59e0b' },
    { name: 'Flexible Load', value: disaggregation.tiers.flexible.kw, color: '#0284c7' }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Freshness Banner */}
      <FreshnessBanner freshness={freshness} lang={lang} />

      {/* Role Context Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
        <div>
          <span className="text-xs text-sky-400 font-mono uppercase tracking-wider">Active Perspective</span>
          <h2 className="text-lg font-bold text-white mt-0.5">{t.roles[currentRole]} View</h2>
        </div>
        <div className="text-right text-xs text-slate-400">
          {currentRole === 'operations' && 'Prioritizing Real-time Alerts & Equipment Control'}
          {currentRole === 'manager' && 'Prioritizing Financial ROI & Verified Savings'}
          {currentRole === 'technician' && 'Prioritizing Telemetry Quality & Sensor Calibration'}
          {currentRole === 'resident' && 'Prioritizing Simple Energy Explanations & Advice'}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <span>{t.metrics.totalLoad}</span>
            <Zap className="h-5 w-5 text-sky-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2 font-mono">{latest.total_kw || 0} kW</div>
          <div className="text-xs text-slate-400 mt-1 flex justify-between">
            <span>Solar: {latest.solar_gen_kw || 0} kW</span>
            <span className={latest.net_grid_kw < 0 ? "text-amber-400 font-semibold" : "text-emerald-400"}>
              {latest.net_grid_kw < 0 ? `Export: ${Math.abs(latest.net_grid_kw)} kW` : `Net Grid: ${latest.net_grid_kw || 0} kW`}
            </span>
          </div>
        </div>

        <RoleViewWrapper currentRole={currentRole} allowedRoles={['operations', 'manager', 'technician']}>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between text-slate-400 text-sm">
              <span>{t.metrics.occupancy}</span>
              <Activity className="h-5 w-5 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2 font-mono">{latest.occupancy || 0}%</div>
            <div className="text-xs text-slate-400 mt-1">
              Tariff Period: <span className="font-semibold text-amber-400">{latest.tariff_period} (₹{latest.tariff_rate}/kWh)</span>
            </div>
          </div>
        </RoleViewWrapper>

        <RoleViewWrapper currentRole={currentRole} allowedRoles={['manager', 'operations']}>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between text-slate-400 text-sm">
              <span>{t.metrics.costSaving}</span>
              <DollarSign className="h-5 w-5 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-emerald-400 mt-2 font-mono">
              {verification && verification.status !== 'DATA_UNAVAILABLE' && verification.cost_saving_total != null
                ? `₹${verification.cost_saving_total.toLocaleString()}`
                : 'Pending Telemetry'}
            </div>
            <div className="text-xs text-slate-400 mt-1">Verified across 30-day verification period</div>
          </div>
        </RoleViewWrapper>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <span>{t.metrics.energyReduction}</span>
            <Shield className="h-5 w-5 text-sky-400" />
          </div>
          <div className="text-2xl font-bold text-sky-400 mt-2 font-mono">
            {verification && verification.status !== 'DATA_UNAVAILABLE' && verification.verified_reduction_pct != null
              ? `${verification.verified_reduction_pct}%`
              : 'Pending Telemetry'}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            {verification && verification.status !== 'DATA_UNAVAILABLE' && verification.baseline_daily_avg_kwh != null
              ? `Baseline (${verification.baseline_daily_avg_kwh} kWh) vs Measured (${verification.measured_daily_avg_kwh} kWh)`
              : 'Telemetry comparison in progress'}
          </div>
        </div>
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Real-time Telemetry Trend */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="font-bold text-white text-base mb-3 flex items-center justify-between">
            <span>Real-time Microgrid Load Profile (24 Hours)</span>
            <span className="text-xs text-slate-500 font-mono">15-minute intervals</span>
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={telemetry}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="timestamp" stroke="#64748b" tickFormatter={(ts) => ts.slice(11, 16)} />
                <YAxis stroke="#64748b" unit=" kW" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Area type="monotone" dataKey="total_kw" stroke="#0284c7" fill="#0284c7" fillOpacity={0.2} name="Total Load (kW)" />
                <Area type="monotone" dataKey="solar_gen_kw" stroke="#34d399" fill="#34d399" fillOpacity={0.2} name="Solar Gen (kW)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Load Tier Disaggregation Summary */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-white text-base mb-3">Load Tier Breakdown</h3>
            {disaggregation && (
              <div className="h-52 w-full flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={4}>
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {disaggregation && (
            <div className="space-y-2 text-xs font-mono border-t border-slate-800 pt-3">
              <div className="flex justify-between items-center text-rose-400">
                <span>Critical (24/7):</span>
                <span className="font-bold">{disaggregation.tiers.critical.kw} kW ({disaggregation.tiers.critical.pct}%)</span>
              </div>
              <div className="flex justify-between items-center text-amber-400">
                <span>Essential:</span>
                <span className="font-bold">{disaggregation.tiers.essential.kw} kW ({disaggregation.tiers.essential.pct}%)</span>
              </div>
              <div className="flex justify-between items-center text-sky-400">
                <span>Flexible (Deferrable):</span>
                <span className="font-bold">{disaggregation.tiers.flexible.kw} kW ({disaggregation.tiers.flexible.pct}%)</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Top Actionable Recommendations */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-white text-lg">Top Actionable Recommendations</h3>
            <p className="text-xs text-slate-400">Detected operational inefficiencies with non-technical root causes and evidence.</p>
          </div>
          <button
            onClick={() => onNavigate('recommendations')}
            className="text-xs text-sky-400 hover:text-sky-300 font-medium flex items-center gap-1"
          >
            View All ({recommendations.length}) <ArrowRight className="h-3 w-3" />
          </button>
        </div>

        <div className="space-y-3">
          {recommendations.slice(0, 2).map((rec) => (
            <div key={rec.recommendation_id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-white text-sm">{rec.equipment_name}</span>
                  <span className="text-xs px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">{rec.priority} PRIORITY</span>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                    rec.action_type === 'ENERGY_REDUCTION' ? 'bg-indigo-500/20 text-indigo-300' : 'bg-amber-500/20 text-amber-300'
                  }`}>
                    {rec.action_type === 'ENERGY_REDUCTION' ? 'ENERGY REDUCTION' : 'LOAD SHIFT (COST)'}
                  </span>
                </div>
                <p className="text-xs text-amber-300">{rec.problem}</p>
                <p className="text-xs text-slate-400">{rec.cause}</p>
              </div>

              <div className="flex items-center space-x-3 shrink-0">
                <div className="text-right text-xs font-mono">
                  <div className="text-emerald-400 font-bold">Save ₹{rec.estimated_cost_saving.toLocaleString()}/mo</div>
                  <div className="text-slate-400">
                    {rec.estimated_energy_saving_kwh > 0 ? `${rec.estimated_energy_saving_kwh} kWh/mo` : '0 kWh (Shift)'}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedLoad(rec.equipment_id)}
                  className="px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-medium rounded-md shadow transition"
                >
                  View Evidence
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Drill-down evidence modal */}
      {selectedLoad && <DrillDownModal loadId={selectedLoad} onClose={() => setSelectedLoad(null)} />}
    </div>
  );
}
