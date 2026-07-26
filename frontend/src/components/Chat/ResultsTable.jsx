import React, { useState } from 'react';
import { Table, ChevronLeft, ChevronRight } from 'lucide-react';

export default function ResultsTable({ columns, rows }) {
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 5;

  if (!columns || !rows || rows.length === 0) return null;

  const totalPages = Math.ceil(rows.length / pageSize);
  const paginatedRows = rows.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden my-3">
      <div className="px-4 py-2 bg-slate-900/90 flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Table className="w-4 h-4 text-indigo-400" />
          <span className="text-xs font-semibold text-slate-300">Query Dataset Results ({rows.length} rows)</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 uppercase font-semibold">
            <tr>
              {columns.map((col, idx) => (
                <th key={idx} className="py-2.5 px-3 whitespace-nowrap">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50 text-slate-200">
            {paginatedRows.map((row, rIdx) => (
              <tr key={rIdx} className="hover:bg-slate-800/40 transition-colors">
                {columns.map((col, cIdx) => {
                  const val = row[col];
                  const isNumber = typeof val === 'number';
                  return (
                    <td key={cIdx} className={`py-2 px-3 whitespace-nowrap ${isNumber ? 'text-indigo-300' : 'text-slate-300'}`}>
                      {val === null || val === undefined ? '-' : val.toString()}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="px-4 py-2 bg-slate-950/60 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>Page {currentPage} of {totalPages}</span>
          <div className="flex items-center space-x-1">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              className="p-1 rounded bg-slate-800 text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-700"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              className="p-1 rounded bg-slate-800 text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-700"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
