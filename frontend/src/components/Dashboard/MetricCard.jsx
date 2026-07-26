import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function MetricCard({ title, value, subtitle, change, icon: Icon, color = 'indigo' }) {
  const colorStyles = {
    indigo: {
      bg: 'bg-indigo-500/10',
      border: 'border-indigo-500/20',
      text: 'text-indigo-400',
      gradient: 'from-indigo-500/20 to-blue-500/5',
    },
    emerald: {
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-500/20',
      text: 'text-emerald-400',
      gradient: 'from-emerald-500/20 to-teal-500/5',
    },
    amber: {
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/20',
      text: 'text-amber-400',
      gradient: 'from-amber-500/20 to-yellow-500/5',
    },
    violet: {
      bg: 'bg-violet-500/10',
      border: 'border-violet-500/20',
      text: 'text-violet-400',
      gradient: 'from-violet-500/20 to-purple-500/5',
    },
  };

  const currentStyle = colorStyles[color] || colorStyles.indigo;
  const isPositive = change >= 0;

  return (
    <div className={`p-5 rounded-2xl border ${currentStyle.border} bg-gradient-to-br ${currentStyle.gradient} backdrop-blur-xl transition-all duration-300 hover:scale-[1.02] hover:shadow-xl`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
        <div className={`p-2.5 rounded-xl ${currentStyle.bg} ${currentStyle.text}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline justify-between">
        <div className="text-2xl font-bold text-white font-outfit">{value}</div>
        {change !== undefined && change !== null && (
          <div className={`flex items-center text-xs font-bold px-2 py-0.5 rounded-full ${
            isPositive ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
          }`}>
            {isPositive ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
            {isPositive ? `+${change}%` : `${change}%`}
          </div>
        )}
      </div>

      {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
    </div>
  );
}
