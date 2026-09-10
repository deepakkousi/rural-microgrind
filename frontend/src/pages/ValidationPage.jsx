import React from 'react';
import { UserCheck, Clock, ShieldCheck, AlertCircle, FileText } from 'lucide-react';

export default function ValidationPage({ lang }) {
  const personas = [
    { role: "Operations Staff", user: "Microgrid Operator", focus: "Identify active load spikes & execute tariff shift recommendations." },
    { role: "Microgrid Manager", user: "Campus Facility Director", focus: "Verify monthly energy savings & baseline reduction percentage." },
    { role: "Technician", user: "Electrician / Instrumentation Tech", focus: "Inspect sensor calibration, flatline stuck sensors & telemetry freshness." },
    { role: "Resident / Non-Technical User", user: "Campus Student / Staff", focus: "Understand non-technical energy disaggregation explanations & savings." }
  ];

  const tasks = [
    { id: 1, name: "Find Biggest Energy Issue", description: "Locate peak tariff water pumping and HVAC low-occupancy waste.", expectedTime: "< 30 sec" },
    { id: 2, name: "Explain Cause of High Energy", description: "Read non-technical root cause explanation (WHAT, WHY, EVIDENCE).", expectedTime: "< 45 sec" },
    { id: 3, name: "Find Recommended Action", description: "Inspect targeted operational action and evidence strength score (0–100).", expectedTime: "< 30 sec" },
    { id: 4, name: "Check Data Freshness Status", description: "Verify telemetry freshness badge (LIVE vs STALE vs MISSING).", expectedTime: "< 15 sec" },
    { id: 5, name: "Understand Expected Saving", description: "Review estimated kWh and monthly monetary savings.", expectedTime: "< 20 sec" }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-amber-500/10 text-amber-400 rounded-lg">
            <UserCheck className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Stakeholder & User Validation Protocol</h2>
            <p className="text-xs text-slate-400 mt-1">
              Structured evaluation protocol for representative user testing across 4 personas.
            </p>
          </div>
        </div>
      </div>

      {/* MANDATORY VALIDATION PENDING BANNER */}
      <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <AlertCircle className="h-5 w-5 text-amber-400" />
          <div>
            <span className="font-bold text-amber-300 text-sm">Status: Validation Pending Field Trial</span>
            <p className="text-xs text-slate-300 mt-0.5">
              Protocol defined for pilot testing. Prototype ready for live stakeholder trial sessions.
            </p>
          </div>
        </div>
        <span className="px-2.5 py-1 bg-amber-500/20 text-amber-300 font-mono text-xs font-bold rounded">PENDING</span>
      </div>

      {/* User Personas */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-bold text-white text-base mb-3">Representative User Personas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {personas.map((p, idx) => (
            <div key={idx} className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider block">{p.role}</span>
              <h4 className="font-bold text-white text-sm mt-0.5">{p.user}</h4>
              <p className="text-xs text-slate-400 mt-1">{p.focus}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Test Tasks Protocol Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-bold text-white text-lg mb-4">Standard User Testing Tasks</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-xs font-mono">
              <tr>
                <th className="px-4 py-3">#</th>
                <th className="px-4 py-3">Task Name</th>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3 text-right">Target Completion Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {tasks.map((t) => (
                <tr key={t.id} className="hover:bg-slate-800/30 transition">
                  <td className="px-4 py-3 font-mono font-bold text-sky-400">{t.id}</td>
                  <td className="px-4 py-3 font-semibold text-white">{t.name}</td>
                  <td className="px-4 py-3 text-slate-400">{t.description}</td>
                  <td className="px-4 py-3 text-right font-mono text-emerald-400">{t.expectedTime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
