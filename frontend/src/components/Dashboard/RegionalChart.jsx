import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function RegionalChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
      <div className="mb-4">
        <h3 className="text-base font-bold text-white font-outfit">Top Regional Sales (By State)</h3>
        <p className="text-xs text-slate-400">Highest grossing shipping destinations</p>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
            <XAxis type="number" stroke="#94a3b8" tick={{ fontSize: 11 }} tickFormatter={(val) => `$${(val/1000).toFixed(0)}k`} />
            <YAxis dataKey="state" type="category" stroke="#94a3b8" tick={{ fontSize: 12 }} width={45} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc' }}
              formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
            />
            <Bar dataKey="total_revenue" fill="#3b82f6" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
