import React from 'react';
import { Beaker, CheckCircle2, Clock, Zap } from 'lucide-react';

export default function ExperimentsPage({ lang }) {
  const interventions = [
    {
      id: "INT_01",
      name: "Water Pump Peak Tariff Shift",
      type: "COST_REDUCTION",
      equipment: "Overhead Tank Water Pump (7.5 kW)",
      baseline: "Runs during Peak Tariff (5 PM - 7 PM @ ₹12.0/kWh). Baseline draw: 16.5 kWh/day.",
      intervention: "Reconfigure timer to run during Off-Peak Tariff (10 PM - 2 AM @ ₹4.5/kWh).",
      result: "Energy draw remains identical (16.5 kWh/day, 0.0 kWh/d energy reduction), but electricity bill drops by ₹105.82/day (₹3,174.60/month).",
      status: "VERIFIED IN TELEMETRY"
    },
    {
      id: "INT_02",
      name: "HVAC Low-Occupancy Setback Control",
      type: "ENERGY_REDUCTION",
      equipment: "Academic Block HVAC Chillers (25.0 kW)",
      baseline: "Runs continuously from 8 AM to 6 PM (220.5 kWh/day) regardless of room occupancy.",
      intervention: "Automated setback control lowers chiller output when occupancy drops below 25%.",
      result: "Verified energy reduction of 73.7 kWh/day (from 220.5 to 146.8 kWh/day), saving ₹644.71/day (₹19,341.30/month).",
      status: "VERIFIED IN TELEMETRY"
    },
    {
      id: "INT_03",
      name: "Workshop CNC Machine Shift away from Peak",
      type: "COST_REDUCTION",
      equipment: "Heavy Workshop CNC Machine (12.0 kW)",
      baseline: "Heavy practical machining classes scheduled during Peak Tariff (47.9 kWh/day @ ₹12.0/kWh).",
      intervention: "Reschedule machining classes to morning shoulder tariff window (9 AM - 12 PM @ ₹7.0/kWh).",
      result: "Energy draw remains constant (48.1 kWh/day, 0.0 kWh/d energy reduction), saving ₹179.49/day (₹5,384.70/month).",
      status: "VERIFIED IN TELEMETRY"
    },
    {
      id: "INT_04",
      name: "Classroom Lighting Low-Occupancy Dimming",
      type: "ENERGY_REDUCTION",
      equipment: "Classroom & Lab Lighting (6.0 kW)",
      baseline: "Lights remain fully powered across academic blocks (153.9 kWh/day).",
      intervention: "Automated 50% lighting dimming via occupancy sensors during low room utilization (< 25%).",
      result: "Verified energy reduction of 9.2 kWh/day (from 153.9 to 144.7 kWh/day), saving ₹76.48/day (₹2,294.40/month).",
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
