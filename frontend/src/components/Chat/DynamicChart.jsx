import React from 'react';
import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, CartesianGrid, Legend
} from 'recharts';

const PALETTE = ['#6366f1', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#3b82f6'];

export default function DynamicChart({ config, rows }) {
  if (!config || !config.chart_type || config.chart_type === 'none' || !rows || rows.length === 0) {
    return null;
  }

  const { chart_type, x_key, y_keys } = config;
  const primaryYKey = y_keys && y_keys.length > 0 ? y_keys[0] : Object.keys(rows[0])[1];

  // 1. Single Metric Display
  if (chart_type === 'metric') {
    const val = rows[0][primaryYKey];
    return (
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 my-3 text-center">
        <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider">{primaryYKey.replace(/_/g, ' ')}</span>
        <div className="text-3xl font-extrabold text-indigo-400 mt-1 font-outfit">
          {typeof val === 'number' ? val.toLocaleString() : val}
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 my-3">
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {chart_type === 'line' ? (
            <LineChart data={rows} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey={x_key} stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f8fafc' }} />
              {y_keys.map((yKey, idx) => (
                <Line key={yKey} type="monotone" dataKey={yKey} stroke={PALETTE[idx % PALETTE.length]} strokeWidth={3} dot={{ r: 4 }} />
              ))}
            </LineChart>
          ) : chart_type === 'pie' ? (
            <PieChart>
              <Pie
                data={rows}
                cx="50%"
                cy="50%"
                innerRadius={45}
                outerRadius={75}
                paddingAngle={4}
                dataKey={primaryYKey}
                nameKey={x_key}
              >
                {rows.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={PALETTE[index % PALETTE.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f8fafc' }} />
              <Legend formatter={(val) => <span className="text-slate-300 text-xs">{val}</span>} />
            </PieChart>
          ) : (
            /* Bar Chart (Default) */
            <BarChart data={rows} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey={x_key} stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f8fafc' }} />
              {y_keys.map((yKey, idx) => (
                <Bar key={yKey} dataKey={yKey} fill={PALETTE[idx % PALETTE.length]} radius={[4, 4, 0, 0]} />
              ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
