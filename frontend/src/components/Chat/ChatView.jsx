import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Sparkles, RefreshCw, Lightbulb } from 'lucide-react';
import ChatMessage from './ChatMessage';
import { sendChatQuery } from '../../services/api';

const SAMPLE_PROMPTS = [
  "What were the top 10 selling products by revenue?",
  "Which region generated the highest revenue?",
  "Show monthly sales trends.",
  "Who are the top 10 customers by total spend?",
  "Show revenue breakdown by product category.",
  "Which products have returned orders?"
];

export default function ChatView() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      data: {
        business_insight: "Welcome to SalesPulse AI Assistant! Ask any sales, revenue, product, or customer question in natural language. I will generate SQL queries, visualize chart trends, and summarize executive insights.",
      }
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (questionText) => {
    const query = (questionText || input).trim();
    if (!query || loading) return;

    const userMsg = { id: Date.now(), sender: 'user', text: query };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const responseData = await sendChatQuery(query);
      const botMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        data: responseData
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to process query';
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          error: errorMsg
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)]">
      
      {/* Top Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white font-outfit flex items-center gap-2">
            AI Sales Analyst <Sparkles className="w-5 h-5 text-indigo-400" />
          </h1>
          <p className="text-xs text-slate-400">Natural Language to SQL Engine with Dynamic Recharts & Executive Insights</p>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {messages.map(msg => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex items-center space-x-3 text-slate-400 text-sm p-4 rounded-xl bg-slate-900/60 border border-slate-800 animate-pulse">
            <RefreshCw className="w-5 h-5 animate-spin text-indigo-400" />
            <span>Analyzing database schema, executing SQL query, and generating visual insights...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompts Pills */}
      <div className="pt-3 pb-2">
        <div className="flex items-center space-x-2 mb-2">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Suggested Questions</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {SAMPLE_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              disabled={loading}
              onClick={() => handleSend(prompt)}
              className="text-xs px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-indigo-500/50 hover:bg-indigo-500/10 transition-all font-medium disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <div className="pt-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center space-x-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a business question (e.g. 'Show monthly sales trends' or 'What were top 5 products?')..."
            className="flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-medium text-sm shadow-lg shadow-indigo-600/20 hover:from-indigo-500 hover:to-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center space-x-2"
          >
            <span>Ask AI</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

    </div>
  );
}
