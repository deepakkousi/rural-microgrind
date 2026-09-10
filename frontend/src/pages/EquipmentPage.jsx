import React, { useEffect, useState } from 'react';
import { Cpu, ShieldCheck, Zap, Filter } from 'lucide-react';
import { fetchEquipmentRegistry } from '../services/api';

export default function EquipmentPage({ lang }) {
  const [equipment, setEquipment] = useState([]);
  const [filterTier, setFilterTier] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEquipmentRegistry()
      .then(setEquipment)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = filterTier === 'ALL'
    ? equipment
    : equipment.filter((eq) => eq.load_tier === filterTier);

  if (loading) return <div className="py-12 text-center text-slate-400">Loading equipment metadata registry...</div>;

  return (
    <div className="space-y-6">
      {/* Header & Filter Controls */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
            <Cpu className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Microgrid Equipment Registry</h2>
            <p className="text-xs text-slate-400 mt-1">9 Registered equipment channels classified across Critical, Essential, and Flexible load tiers.</p>
          </div>
        </div>

        {/* Filter buttons */}
        <div className="flex items-center space-x-2 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
          <Filter className="h-3.5 w-3.5 text-slate-400 ml-2" />
          {['ALL', 'Critical', 'Essential', 'Flexible'].map((tier) => (
            <button
              key={tier}
              onClick={() => setFilterTier(tier)}
              className={`px-3 py-1 font-semibold rounded ${
                filterTier === tier ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              {tier}
            </button>
          ))}
        </div>
      </div>

      {/* Equipment Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((eq) => (
          <div key={eq.equipment_id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded">{eq.equipment_id}</span>
                <span className={`px-2 py-0.5 text-xs font-semibold rounded ${
                  eq.load_tier === 'Critical' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30' :
                  eq.load_tier === 'Essential' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30' :
                  'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                }`}>
                  {eq.load_tier}
                </span>
              </div>

              <h3 className="font-bold text-white text-base mb-1">{eq.equipment_name}</h3>
              <p className="text-xs text-slate-400 mb-3">{eq.location}</p>

              <div className="space-y-2 text-xs border-t border-slate-800/80 pt-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Rated Capacity:</span>
                  <span className="font-mono text-white font-bold">{eq.rated_power_kw} kW</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Essential Priority:</span>
                  <span className={eq.is_essential ? 'text-emerald-400 font-semibold' : 'text-slate-400'}>
                    {eq.is_essential ? 'Yes (Essential)' : 'No (Flexible)'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Telemetry Channel:</span>
                  <span className="font-mono text-slate-300">{eq.channel_key}</span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 text-xs">
              <span className="text-slate-500 block mb-0.5">Operating Schedule:</span>
              <span className="text-slate-300 font-medium">{eq.schedule_description}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
