import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import DisaggregationPage from './pages/DisaggregationPage';
import RecommendationsPage from './pages/RecommendationsPage';
import EquipmentPage from './pages/EquipmentPage';
import VerificationPage from './pages/VerificationPage';
import QualityPage from './pages/QualityPage';
import ExperimentsPage from './pages/ExperimentsPage';
import ValidationPage from './pages/ValidationPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentRole, setRole] = useState('operations');
  const [lang, setLang] = useState('en');

  const renderPage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard currentRole={currentRole} lang={lang} onNavigate={setActiveTab} />;
      case 'disaggregation':
        return <DisaggregationPage lang={lang} />;
      case 'recommendations':
        return <RecommendationsPage lang={lang} />;
      case 'equipment':
        return <EquipmentPage lang={lang} />;
      case 'verification':
        return <VerificationPage lang={lang} />;
      case 'quality':
        return <QualityPage lang={lang} />;
      case 'experiments':
        return <ExperimentsPage lang={lang} />;
      case 'validation':
        return <ValidationPage lang={lang} />;
      default:
        return <Dashboard currentRole={currentRole} lang={lang} onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentRole={currentRole}
        setRole={setRole}
        lang={lang}
        setLang={setLang}
      />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {renderPage()}
      </main>
      <footer className="bg-slate-900 border-t border-slate-800 text-center py-4 text-xs text-slate-500 font-mono">
        Rural Microgrid Intelligence Platform • Phase 1 - 23 Complete Prototype • Academic & Production Prototype
      </footer>
    </div>
  );
}
