import React from 'react';
import { Bot, User, Sparkles } from 'lucide-react';
import SqlQueryBox from './SqlQueryBox';
import ResultsTable from './ResultsTable';
import DynamicChart from './DynamicChart';

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="flex items-start space-x-2 max-w-2xl">
          <div className="bg-indigo-600 text-white px-4 py-3 rounded-2xl rounded-tr-none shadow-md shadow-indigo-600/20 text-sm">
            {message.text}
          </div>
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0">
            <User className="w-4 h-4" />
          </div>
        </div>
      </div>
    );
  }

  const { data, error } = message;

  return (
    <div className="flex justify-start mb-6">
      <div className="flex items-start space-x-3 max-w-4xl w-full">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center text-white shrink-0 shadow-lg shadow-indigo-500/20">
          <Bot className="w-5 h-5" />
        </div>

        <div className="flex-1 bg-slate-900/90 border border-slate-800 rounded-2xl rounded-tl-none p-4 shadow-xl backdrop-blur-xl">
          
          {error ? (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
              <strong className="font-semibold">Query Error:</strong> {error}
            </div>
          ) : (
            <>
              {/* Executive Insight Card */}
              {data?.business_insight && (
                <div className="mb-3 p-3.5 rounded-xl bg-gradient-to-r from-indigo-500/10 to-blue-500/5 border border-indigo-500/20 flex items-start space-x-3">
                  <Sparkles className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 block mb-1">AI Business Insight</span>
                    <p className="text-sm text-slate-200 leading-relaxed font-sans">{data.business_insight}</p>
                  </div>
                </div>
              )}

              {/* Dynamic Visual Chart */}
              {data?.chart_config && data?.rows && (
                <DynamicChart config={data.chart_config} rows={data.rows} />
              )}

              {/* Data Table */}
              {data?.columns && data?.rows && (
                <ResultsTable columns={data.columns} rows={data.rows} />
              )}

              {/* SQL Query Drawer */}
              {data?.sql_query && (
                <SqlQueryBox sqlQuery={data.sql_query} />
              )}
            </>
          )}

        </div>
      </div>
    </div>
  );
}
