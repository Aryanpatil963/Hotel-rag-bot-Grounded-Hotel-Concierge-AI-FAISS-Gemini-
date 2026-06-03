import React from 'react';
import { MessageSquare, BarChart3, Settings, HelpCircle, User } from 'lucide-react';

export default function Sidebar({ activeScreen, setActiveScreen }) {
  return (
    <aside className="w-[250px] bg-brand-primary text-brand-bg flex flex-col justify-between border-r border-brand-secondary/20 h-screen select-none shrink-0">
      {/* Top Section */}
      <div className="pt-8 px-6">
        <div className="mb-8">
          <h1 className="font-display text-2xl font-semibold tracking-wide text-brand-secondary">
            The Grand Estate
          </h1>
          <p className="font-body text-[10px] uppercase tracking-[0.2em] text-brand-tertiary mt-1 font-medium">
            Excellence in Service
          </p>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-2">
          <button
            onClick={() => setActiveScreen('chat')}
            className={`w-full flex items-center gap-3 py-3 px-4 rounded text-left transition-all ${
              activeScreen === 'chat'
                ? 'bg-brand-primary text-white border-l-4 border-brand-secondary font-medium'
                : 'text-brand-tertiary hover:text-brand-secondary hover:bg-brand-primary/40'
            }`}
          >
            <MessageSquare size={18} className={activeScreen === 'chat' ? 'text-brand-secondary' : ''} />
            <span className="font-body text-sm">Guest Assistant</span>
          </button>

          <button
            onClick={() => setActiveScreen('admin')}
            className={`w-full flex items-center gap-3 py-3 px-4 rounded text-left transition-all ${
              activeScreen === 'admin'
                ? 'bg-brand-primary text-white border-l-4 border-brand-secondary font-medium'
                : 'text-brand-tertiary hover:text-brand-secondary hover:bg-brand-primary/40'
            }`}
          >
            <BarChart3 size={18} className={activeScreen === 'admin' ? 'text-brand-secondary' : ''} />
            <span className="font-body text-sm">Admin Analytics</span>
          </button>
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="pb-8 px-6 space-y-6">
        {/* Settings & Support */}
        <div className="space-y-3 border-t border-brand-secondary/10 pt-6">
          <button className="w-full flex items-center gap-3 text-brand-tertiary hover:text-brand-secondary text-left transition-colors">
            <Settings size={16} />
            <span className="font-body text-xs font-medium">Settings</span>
          </button>
          <button className="w-full flex items-center gap-3 text-brand-tertiary hover:text-brand-secondary text-left transition-colors">
            <HelpCircle size={16} />
            <span className="font-body text-xs font-medium">Support</span>
          </button>
        </div>

        {/* Guest Profile */}
        <div className="flex items-center gap-3 bg-brand-primary/60 border border-brand-secondary/15 rounded-lg p-3">
          <div className="w-10 h-10 rounded-full bg-brand-secondary/10 border border-brand-secondary flex items-center justify-center text-brand-secondary">
            <User size={18} />
          </div>
          <div>
            <h4 className="font-body text-xs font-bold text-white">Mr. Sterling</h4>
            <p className="font-body text-[10px] text-brand-secondary mt-0.5">Suite 1204</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
