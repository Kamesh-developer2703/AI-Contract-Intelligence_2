import React, { useState } from 'react';
import { Tag, FileText, CheckCircle, Percent, MapPin, Landmark, Calendar, DollarSign } from 'lucide-react';

export default function MetadataTabs({ entities, clauses }) {
  const [activeTab, setActiveTab] = useState('highlights');

  const getEntityIcon = (category) => {
    switch (category) {
      case 'ORG':
        return <Landmark className="w-3.5 h-3.5 text-brand-slate" />;
      case 'DATE':
        return <Calendar className="w-3.5 h-3.5 text-blue-600" />;
      case 'MONEY':
        return <DollarSign className="w-3.5 h-3.5 text-emerald-600" />;
      case 'LOCATION':
        return <MapPin className="w-3.5 h-3.5 text-brand-blue" />;
      default:
        return <Tag className="w-3.5 h-3.5" />;
    }
  };

  const getEntityBadgeStyle = (category) => {
    switch (category) {
      case 'ORG':
        return 'bg-brand-slate/10 text-brand-slate border-brand-slate/20';
      case 'DATE':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'MONEY':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'LOCATION':
        return 'bg-brand-blue/10 text-brand-slate border-brand-blue/30';
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200';
    }
  };

  const categories = [
    { key: 'ORG', label: 'Key Parties' },
    { key: 'DATE', label: 'Critical Dates' },
    { key: 'MONEY', label: 'Transaction Values' },
    { key: 'LOCATION', label: 'Jurisdictions & Locations' }
  ];

  const hasEntities = entities && Object.keys(entities).some(key => entities[key] && entities[key].length > 0);
  const hasClauses = clauses && clauses.length > 0;

  return (
    <div className="bg-brand-white rounded-2xl shadow-sm border border-gray-200/80 p-6 flex flex-col h-full space-y-6">
      {/* Tabs Switcher using Pacific Blue accents */}
      <div className="flex border-b border-gray-100 pb-1">
        <button
          onClick={() => setActiveTab('highlights')}
          className={`flex items-center space-x-2 pb-3 px-4 font-bold text-xs uppercase tracking-wider border-b-2 transition-all ${
            activeTab === 'highlights'
              ? 'border-brand-blue text-brand-blue'
              : 'border-transparent text-gray-400 hover:text-brand-slate'
          }`}
        >
          <Tag className="w-4 h-4" />
          <span>Contract Highlights</span>
        </button>
        <button
          onClick={() => setActiveTab('clauses')}
          className={`flex items-center space-x-2 pb-3 px-4 font-bold text-xs uppercase tracking-wider border-b-2 transition-all ${
            activeTab === 'clauses'
              ? 'border-brand-blue text-brand-blue'
              : 'border-transparent text-gray-400 hover:text-brand-slate'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Detailed Clause Check</span>
        </button>
      </div>

      {/* Tabs Content */}
      <div className="flex-1 flex flex-col overflow-y-auto max-h-[460px]">
        {/* Tab 1: Highlights */}
        {activeTab === 'highlights' && (
          <div className="space-y-5 animate-fade-in">
            {!hasEntities ? (
              <div className="border border-dashed border-gray-200 rounded-xl flex flex-col items-center justify-center p-8 text-gray-400 space-y-2 grow bg-gray-50/50">
                <Tag className="w-8 h-8 text-gray-300" />
                <p className="text-xs font-bold">No Summary Available</p>
                <p className="text-[10px] text-gray-400 text-center">Analyze an agreement to display highlights.</p>
              </div>
            ) : (
              <div className="space-y-5">
                {categories.map(({ key, label }) => {
                  const items = entities[key] || [];
                  return (
                    <div key={key} className="space-y-2 border-b border-gray-50 pb-4 last:border-b-0 last:pb-0">
                      <div className="flex items-center justify-between">
                        <h4 className="text-[11px] font-extrabold text-brand-slate uppercase tracking-wider flex items-center space-x-1.5">
                          {getEntityIcon(key)}
                          <span>{label}</span>
                        </h4>
                        <span className="bg-brand-platinum px-2 py-0.5 rounded text-[10px] font-bold text-brand-slate">
                          {items.length}
                        </span>
                      </div>

                      {items.length === 0 ? (
                        <p className="text-[10px] text-gray-400 italic">No matches identified in text</p>
                      ) : (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {items.map((val, i) => (
                            <span
                              key={i}
                              className={`text-xs font-semibold px-2.5 py-1 rounded-lg border flex items-center space-x-1 shadow-sm ${getEntityBadgeStyle(key)}`}
                            >
                              <span>{val}</span>
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Clause Check */}
        {activeTab === 'clauses' && (
          <div className="space-y-4 animate-fade-in grow">
            {!hasClauses ? (
              <div className="border border-dashed border-gray-200 rounded-xl flex flex-col items-center justify-center p-8 text-gray-400 space-y-2 grow bg-gray-50/50">
                <FileText className="w-8 h-8 text-gray-300" />
                <p className="text-xs font-bold">No Clauses Scanned</p>
                <p className="text-[10px] text-gray-400 text-center">Identified contract clauses will be mapped here.</p>
              </div>
            ) : (
              <div className="space-y-3.5">
                {clauses.map((item, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-xl p-4 bg-brand-platinum/10 space-y-3 transition-all hover:bg-brand-platinum/20"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-brand-blue" />
                        <span className="text-xs font-extrabold text-brand-slate uppercase tracking-wider">
                          {item.clause_type}
                        </span>
                      </div>
                      
                      {/* Match Confidence Score */}
                      <div className="flex items-center space-x-1 bg-brand-white border border-gray-200 px-2 py-0.5 rounded text-xs font-extrabold text-brand-blue shadow-sm">
                        <Percent className="w-3.5 h-3.5" />
                        <span>{(item.confidence * 100).toFixed(0)}% Confidence</span>
                      </div>
                    </div>

                    {/* Paragraph excerpt */}
                    <div className="bg-brand-white border border-gray-100 p-3 rounded-lg max-h-24 overflow-y-auto">
                      <p className="text-xs text-gray-600 leading-relaxed italic">
                        "{item.text}"
                      </p>
                    </div>

                    {/* Extracted Metadata attributes */}
                    {item.parameters && Object.keys(item.parameters).length > 0 && (
                      <div className="flex flex-wrap gap-2 pt-1 border-t border-gray-100/50 mt-2">
                        {Object.entries(item.parameters).map(([k, v]) => (
                          <div key={k} className="text-[10px] font-semibold bg-brand-slate/5 border border-brand-slate/10 px-2 py-0.5 rounded-lg text-brand-slate flex items-center space-x-1">
                            <span className="capitalize text-gray-400">{k}:</span>
                            <span className="font-bold">{String(v)}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
