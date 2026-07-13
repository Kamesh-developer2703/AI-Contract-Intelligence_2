import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function Header({ toggleMockMode, onOpenSettings }) {
  // Hidden developer helpers in console
  const handleLogoClick = (e) => {
    if (e.detail === 3) {
      console.log("[Dev Tool] Toggling Integration Mode...");
      toggleMockMode();
    }
  };

  const handleSubtitleClick = (e) => {
    if (e.detail === 3) {
      console.log("[Dev Tool] Opening Backend Settings...");
      onOpenSettings();
    }
  };

  return (
    <header className="bg-brand-slate text-brand-white px-6 py-4 shadow-md flex items-center justify-between sticky top-0 z-40 border-b border-brand-slate/40">
      {/* Brand Logo and Title */}
      <div className="flex items-center space-x-3">
        <div 
          onClick={handleLogoClick}
          className="bg-brand-white/10 p-2 rounded-xl flex items-center justify-center cursor-default select-none hover:bg-brand-white/20 transition-all"
          title="AI Contract Analyzer"
        >
          <ShieldCheck className="w-6 h-6 text-brand-blue" />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight text-brand-white select-none">
            AI Contract Intelligence
          </h1>
          <p 
            onClick={handleSubtitleClick}
            className="text-xs text-brand-blue font-medium select-none cursor-default hover:text-brand-white/80 transition-all"
          >
            Professional Legal Risk Assessment
          </p>
        </div>
      </div>

      {/* Corporate Label */}
      <div className="flex items-center space-x-4">
        <div className="hidden sm:flex flex-col text-right">
          <span className="text-xs font-bold text-brand-white">Corporate Client Workspace</span>
          <span className="text-[10px] text-brand-blue/80 font-bold">Standard Review Protocol</span>
        </div>
      </div>
    </header>
  );
}
