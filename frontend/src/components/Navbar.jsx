import React from 'react';
import { Zap, Shield, UserCheck, Globe, Activity } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function Navbar({ activeTab, setActiveTab, currentRole, setRole, lang, setLang }) {
  const t = translations[lang] || translations.en;

  const tabs = [
    { id: 'dashboard', label: t.nav.dashboard },
    { id: 'disaggregation', label: t.nav.disaggregation },
    { id: 'recommendations', label: t.nav.recommendations },
    { id: 'equipment', label: t.nav.equipment },
    { id: 'verification', label: t.nav.verification },
    { id: 'quality', label: t.nav.quality },
    { id: 'experiments', label: t.nav.experiments },
    { id: 'validation', label: t.nav.validation },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Platform Name */}
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sky-500/10 text-sky-400 rounded-lg border border-sky-500/20">
              <Zap className="h-6 w-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white leading-tight">{t.appTitle}</h1>
              <span className="text-xs text-sky-400 font-mono flex items-center gap-1">
                <Activity className="h-3 w-3 inline" /> Rural Microgrid Telemetry v1.0
              </span>
            </div>
          </div>

          {/* Controls: Role Selector & Language Switch */}
          <div className="flex items-center space-x-4">
            {/* Role Dropdown */}
            <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              <UserCheck className="h-4 w-4 text-sky-400" />
              <label htmlFor="role-select" className="sr-only">Select User Role</label>
              <select
                id="role-select"
                value={currentRole}
                onChange={(e) => setRole(e.target.value)}
                className="bg-transparent text-sm font-medium text-slate-200 focus:outline-none cursor-pointer"
              >
                <option value="operations" className="bg-slate-900">{t.roles.operations}</option>
                <option value="manager" className="bg-slate-900">{t.roles.manager}</option>
                <option value="technician" className="bg-slate-900">{t.roles.technician}</option>
                <option value="resident" className="bg-slate-900">{t.roles.resident}</option>
              </select>
            </div>

            {/* Language Toggle */}
            <div className="flex items-center space-x-1 bg-slate-800/80 px-2 py-1 rounded-lg border border-slate-700">
              <Globe className="h-4 w-4 text-emerald-400" />
              <button
                onClick={() => setLang('en')}
                className={`px-2 py-0.5 text-xs font-semibold rounded ${lang === 'en' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'}`}
                aria-label="Switch to English language"
              >
                EN
              </button>
              <button
                onClick={() => setLang('hi')}
                className={`px-2 py-0.5 text-xs font-semibold rounded ${lang === 'hi' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'}`}
                aria-label="Switch to Hindi language"
              >
                HI
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 overflow-x-auto py-2 scrollbar-none border-t border-slate-800/60" aria-label="Main Navigation">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 text-sm font-medium rounded-md whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
              aria-current={activeTab === tab.id ? 'page' : undefined}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
