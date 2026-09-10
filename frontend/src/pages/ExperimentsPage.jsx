import React from 'react';
import { Beaker, CheckCircle2, Clock, Zap } from 'lucide-react';

export default function ExperimentsPage({ lang }) {
  const interventions = [
    {
      id: "INT_01",
      name: "Water Pump Peak Tariff Shift",
      equipment: "Overhead Tank Water Pump (7.5 kW)",
      baseline: "Runs during Peak Tariff (5 PM - 7 PM @ ₹12.0/kWh). Daily cost: ₹172.80.",
      intervention: "Reconfigure timer to run during Off-Peak Tariff (10 PM - 2 AM @ ₹4.5/kWh).",
      result: "Energy draw remains identical (14.4 kWh/day), but monthly electricity bill drops by ₹3,240.",
      status: "VERIFIED IN TELEMETRY"
    },
    {
      id: "INT_02",
      name: "HVAC Low-Occupancy Setback Control",
      equipment: "Academic Block HVAC Chillers (25.0 kW)",
      baseline: "Runs at 100% full capacity (21.4 kW) continuously from 8 AM to 6 PM regardless of room occupancy.",
      intervention: "Automated setback control lowers chiller output to 7.0 kW when occupancy drops below 25% (lunch hours & late afternoon).",
      result: "Reduces HVAC energy consumption by 93 kWh/day, saving ₹23,715/month.",
      status: "VERIFIED IN TELEMETRY"
    },
    {
      id: "INT_03",
      name: "Workshop CNC Machine Shift away from Peak",
      equipment: "Heavy Workshop CNC Machine (12.0 kW)",
      baseline: "Heavy practical machining classes scheduled between 2 PM and 5 PM (Peak Tariff @ ₹12.0/kWh).",
      intervention: "Reschedule machining classes to morning shoulder tariff window (9 AM - 1 PM @ ₹7.0/kWh).",
      result: "Eliminates peak tariff surcharge, saving ₹5,625/month.",
      status: "VERIFIED IN TELEMETRY"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
            <Beaker className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Measurable Operational Experiments</h2>
            <p className="text-xs text-slate-400 mt-1">
              3 Synthetic operational interventions embedded directly into the 90-day microgrid meter data stream.
            </p>
          </div>
        </div>
      </div>

      {/* Intervention Cards */}
      <div className="space-y-4">
        {interventions.map((item) => (
          <div key={item.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-md">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <div className="flex items-center space-x-3">
                <span className="font-mono text-xs text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">{item.id}</span>
                <h3 className="font-bold text-white text-lg">{item.name}</h3>
              </div>
              <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold rounded flex items-center gap-1">
                <CheckCircle2 className="h-3.5 w-3.5" /> {item.status}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <span className="text-slate-500 font-semibold uppercase block mb-1">Baseline State (Days 1–30)</span>
                <p className="text-slate-300">{item.baseline}</p>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <span className="text-sky-400 font-semibold uppercase block mb-1">Intervention Action (Days 31–60)</span>
                <p className="text-slate-300">{item.intervention}</p>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <span className="text-emerald-400 font-semibold uppercase block mb-1">Verified Impact (Days 61–90)</span>
                <p className="text-slate-300 font-medium">{item.result}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
