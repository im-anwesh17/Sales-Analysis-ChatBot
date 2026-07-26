import React from 'react';
import { Package, TrendingUp } from 'lucide-react';

export default function TopProductsTable({ products }) {
  if (!products || products.length === 0) return null;

  return (
    <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-white font-outfit">Top 10 Performing Products</h3>
          <p className="text-xs text-slate-400">Ranked by revenue contribution</p>
        </div>
        <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
          <Package className="w-5 h-5" />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-800 text-xs font-semibold uppercase text-slate-400">
              <th className="pb-3 px-3">Product Name</th>
              <th className="pb-3 px-3">Category</th>
              <th className="pb-3 px-3 text-right">Units Sold</th>
              <th className="pb-3 px-3 text-right">Total Revenue</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {products.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3 px-3 font-medium text-white flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-800 text-slate-400 text-xs flex items-center justify-center font-bold">
                    {idx + 1}
                  </span>
                  {item.product_name}
                </td>
                <td className="py-3 px-3">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-indigo-300 border border-slate-700">
                    {item.category}
                  </span>
                </td>
                <td className="py-3 px-3 text-right text-slate-300 font-mono">{item.total_units_sold.toLocaleString()}</td>
                <td className="py-3 px-3 text-right font-bold text-emerald-400 font-mono">${item.total_revenue.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
