import React, { useEffect, useState } from 'react';
import { Users, Award, AlertTriangle, UserCheck, HelpCircle, RefreshCw } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { fetchRfmAnalytics } from '../../services/api';

const SEGMENT_COLORS = {
  'Champions': '#10b981',
  'Loyal Customers': '#3b82f6',
  'Potential Loyalists': '#8b5cf6',
  'At Risk': '#f59e0b',
  'Lost / Needs Attention': '#ef4444'
};

export default function RfmView() {
  const [rfmData, setRfmData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadRfm = async () => {
      setLoading(true);
      try {
        const res = await fetchRfmAnalytics();
        setRfmData(res);
      } catch (err) {
        console.error('Failed to fetch RFM metrics:', err);
      } finally {
        setLoading(false);
      }
    };
    loadRfm();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center space-x-3 text-indigo-400 font-medium">
          <RefreshCw className="w-6 h-6 animate-spin" />
          <span>Computing Customer RFM Quintiles & Matrix...</span>
        </div>
      </div>
    );
  }

  const { summary = [], top_customers = [] } = rfmData || {};

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white font-outfit">RFM Customer Segmentation</h1>
        <p className="text-slate-400 text-sm mt-1">
          Behavioral customer clustering based on Recency (last order), Frequency (total orders), and Monetary value (total spend)
        </p>
      </div>

      {/* Segment Summary Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {summary.map((seg, idx) => {
          const color = SEGMENT_COLORS[seg.rfm_segment] || '#6366f1';
          return (
            <div key={idx} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl relative overflow-hidden">
              <div className="h-1 w-full absolute top-0 left-0" style={{ backgroundColor: color }} />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block">{seg.rfm_segment}</span>
              <div className="text-2xl font-bold text-white mt-2 font-outfit">{seg.customer_count} <span className="text-xs text-slate-400 font-normal">users</span></div>
              
              <div className="mt-3 pt-3 border-t border-slate-800 space-y-1 text-xs text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Recency:</span>
                  <span className="font-mono">{seg.avg_recency} days</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Orders:</span>
                  <span className="font-mono">{seg.avg_frequency}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Spend:</span>
                  <span className="font-mono font-semibold text-emerald-400">${seg.avg_monetary.toLocaleString()}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Distribution Chart & Top Customer Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Pie Chart */}
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
          <h3 className="text-base font-bold text-white font-outfit mb-1">Customer Distribution</h3>
          <p className="text-xs text-slate-400 mb-4">Share of total active accounts by segment</p>
          
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={summary}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="customer_count"
                  nameKey="rfm_segment"
                >
                  {summary.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={SEGMENT_COLORS[entry.rfm_segment] || '#6366f1'} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc' }} />
                <Legend formatter={(value) => <span className="text-slate-300 text-xs">{value}</span>} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Customers Table */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white font-outfit">Top Valued Customers (RFM Matrix)</h3>
              <p className="text-xs text-slate-400">High-monetary customer profiles</p>
            </div>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Award className="w-5 h-5" />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold">
                  <th className="pb-3 px-3">Customer Name</th>
                  <th className="pb-3 px-3">Segment</th>
                  <th className="pb-3 px-3 text-center">R-F-M Score</th>
                  <th className="pb-3 px-3 text-right">Last Order</th>
                  <th className="pb-3 px-3 text-right">Orders</th>
                  <th className="pb-3 px-3 text-right">Total Spend</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {top_customers.slice(0, 10).map((cust, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 px-3 font-sans font-medium text-white">{cust.customer_name}</td>
                    <td className="py-2.5 px-3">
                      <span
                        className="px-2 py-0.5 rounded-full text-[10px] font-semibold text-white"
                        style={{ backgroundColor: SEGMENT_COLORS[cust.rfm_segment] || '#6366f1' }}
                      >
                        {cust.rfm_segment}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-center text-indigo-300 font-bold">{cust.r_score}-{cust.f_score}-{cust.m_score}</td>
                    <td className="py-2.5 px-3 text-right text-slate-400">{cust.last_order_date}</td>
                    <td className="py-2.5 px-3 text-right text-slate-300">{cust.frequency}</td>
                    <td className="py-2.5 px-3 text-right font-bold text-emerald-400">${cust.monetary.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </div>
  );
}
