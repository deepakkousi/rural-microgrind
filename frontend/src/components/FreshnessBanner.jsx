import React from 'react';
import { AlertTriangle, Clock, CheckCircle2, ShieldAlert } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function FreshnessBanner({ freshness, lang = 'en' }) {
  const t = translations[lang] || translations.en;

  if (!freshness) return null;

  const status = freshness.status || 'LIVE';

  const badgeStyles = {
    LIVE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    STALE: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    VERY_STALE: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    MISSING: 'bg-rose-500/10 text-rose-400 border-rose-500/30'
  };

  const statusIcons = {
    LIVE: <CheckCircle2 className="h-4 w-4 text-emerald-400" />,
    STALE: <Clock className="h-4 w-4 text-amber-400" />,
    VERY_STALE: <AlertTriangle className="h-4 w-4 text-orange-400" />,
    MISSING: <ShieldAlert className="h-4 w-4 text-rose-400" />
  };

  return (
    <div className={`px-4 py-2.5 rounded-lg border flex flex-wrap items-center justify-between gap-3 my-4 ${badgeStyles[status]}`}>
      <div className="flex items-center space-x-3">
        {statusIcons[status]}
        <div>
          <span className="font-bold text-sm uppercase tracking-wider">{t.freshness[status.toLowerCase()] || status}</span>
          {freshness.warning_message && (
            <p className="text-xs text-slate-300 mt-0.5">{freshness.warning_message}</p>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-4 text-xs font-mono">
        <div>
          <span className="text-slate-400">{t.freshness.lastUpdated}:</span>{' '}
          <span className="text-slate-200">{freshness.last_updated || 'Just now'}</span>
        </div>
        <div>
          <span className="text-slate-400">{t.freshness.reliability}:</span>{' '}
          <span className="font-semibold text-sky-400">{freshness.recommendation_reliability || 'HIGH'}</span>
        </div>
      </div>
    </div>
  );
}
