import React, { useState } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/Dashboard/DashboardView';
import ChatView from './components/Chat/ChatView';
import RfmView from './components/Analytics/RfmView';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && <DashboardView />}
        {activeTab === 'chat' && <ChatView />}
        {activeTab === 'rfm' && <RfmView />}
      </main>

      <footer className="border-t border-slate-800/80 py-4 bg-slate-950/60 text-center text-xs text-slate-500">
        <p>AI Sales Analytics Engine • FastAPI, PostgreSQL, SQLAlchemy, React, Recharts & Gemini/OpenAI</p>
      </footer>
    </div>
  );
}
