import React, { useEffect, useState } from 'react';
import { ShieldAlert, AlertCircle, ArrowUpRight, CheckCircle2 } from 'lucide-react';

export default function RiskDashboard({ riskScore, alerts }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = riskScore;
    if (start === end) {
      setAnimatedScore(end);
      return;
    }
    
    const duration = 800; // ms
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / end));
    
    const timer = setInterval(() => {
      start += increment;
      setAnimatedScore(start);
      if (start === end) {
        clearInterval(timer);
      }
    }, Math.max(stepTime, 10));

    return () => clearInterval(timer);
  }, [riskScore]);

  // SVG Circular Configuration
  const radius = 70;
  const strokeWidth = 14;
  const circumference = 2 * Math.PI * radius;
  // Dynamically calculate progress stroke fill based on riskScore
  const offset = circumference - (animatedScore / 100) * circumference;

  // Determine colors: Tangerine Dream (#E39774) if score > 50, else Pacific Blue (#5C9EAD)
  const isHighRisk = riskScore > 50;
  const gaugeColor = isHighRisk ? '#E39774' : '#5C9EAD';
  const textClass = isHighRisk ? 'text-brand-tangerine' : 'text-brand-blue';
  const borderClass = isHighRisk ? 'border-brand-tangerine/30' : 'border-brand-blue/30';
  const bgClass = isHighRisk ? 'bg-brand-tangerine/5' : 'bg-brand-blue/5';
  
  return (
    <div className="bg-brand-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col h-full space-y-6">
      {/* Panel Header - Lawyer Friendly */}
      <div>
        <h2 className="text-lg font-bold text-brand-slate tracking-tight">Risk Assessment Gauge</h2>
        <p className="text-xs text-gray-400 font-semibold">Overall legal liability profile of the contract</p>
      </div>

      {/* Circle Scorer Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center border-b border-gray-100 pb-6">
        {/* Dynamic SVG Gauge */}
        <div className="flex flex-col items-center justify-center relative">
          <svg className="w-40 h-40 transform -rotate-90">
            <circle
              cx="80"
              cy="80"
              r={radius}
              stroke="#EEEEEE"
              strokeWidth={strokeWidth}
              fill="transparent"
            />
            <circle
              cx="80"
              cy="80"
              r={radius}
              stroke={gaugeColor}
              strokeWidth={strokeWidth}
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className="transition-all duration-500 ease-out"
            />
          </svg>
          
          <div className="absolute flex flex-col items-center justify-center">
            <span className="text-4xl font-extrabold tracking-tighter text-brand-slate">
              {riskScore > 0 ? animatedScore : '0'}
            </span>
            <span className="text-[10px] uppercase font-bold tracking-widest text-gray-400">
              Risk Index
            </span>
          </div>
        </div>

        {/* Dynamic Status Tag */}
        <div className="flex flex-col justify-center space-y-2">
          <div className={`px-4 py-2.5 rounded-xl border ${bgClass} ${borderClass} ${textClass} flex items-center space-x-2.5 shadow-sm`}>
            <ShieldAlert className="w-5 h-5 shrink-0" />
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wider">Analysis Status</p>
              <p className="text-sm font-extrabold">
                {riskScore === 0 ? 'No Data Loaded' : isHighRisk ? 'High Risk Warnings' : 'Standard Risk Level'}
              </p>
            </div>
          </div>
          <p className="text-[11px] text-gray-500 leading-relaxed font-semibold">
            {riskScore > 0 
              ? `The automated reviewer computed a score of ${riskScore} based on warning triggers and critical safety controls.`
              : 'Upload a contract document to execute the legal risk evaluation.'
            }
          </p>
        </div>
      </div>

      {/* Critical Risk Warnings List */}
      <div className="flex-1 flex flex-col space-y-3 min-h-[220px]">
        <h3 className="text-xs font-bold text-brand-slate uppercase tracking-wider">
          Critical Risk Warnings ({alerts.length})
        </h3>
        
        {alerts.length === 0 ? (
          <div className="grow border border-dashed border-gray-200 rounded-xl flex flex-col items-center justify-center p-6 text-gray-400 space-y-2 bg-gray-50/50">
            <CheckCircle2 className="w-8 h-8 text-gray-300" />
            <p className="text-xs font-bold">No Risk Warnings Identified</p>
            <p className="text-[10px] text-gray-400 text-center">Analyze an agreement to scan for critical risks.</p>
          </div>
        ) : (
          <div className="space-y-3 max-h-[260px] overflow-y-auto pr-1">
            {alerts.map((alert, index) => {
              const isHigh = alert.severity === 'High';
              return (
                <div
                  key={index}
                  className={`border rounded-xl p-4 transition-all duration-300 shadow-sm hover:shadow-md animate-fade-in bg-brand-white ${
                    isHigh ? 'border-brand-tangerine bg-brand-tangerine/5' : 'border-brand-blue/30'
                  }`}
                  style={{ animationDelay: `${index * 80}ms` }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-2">
                      <span className={`w-2 h-2 rounded-full ${isHigh ? 'bg-brand-tangerine animate-pulse' : 'bg-brand-blue'}`} />
                      <span className="text-xs font-bold text-brand-slate tracking-wide">
                        Warning: {alert.clause}
                      </span>
                    </div>
                    <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${
                      isHigh ? 'bg-brand-tangerine/20 text-brand-tangerine' : 'bg-brand-blue/20 text-brand-blue'
                    }`}>
                      {alert.severity} Risk
                    </span>
                  </div>

                  <div className="mt-2 bg-brand-white border border-gray-100 p-2.5 rounded-lg">
                    <p className="text-[11px] text-gray-600 leading-normal font-semibold italic">"{alert.text}"</p>
                  </div>

                  <div className="mt-2.5 flex items-start space-x-1.5 text-xs text-brand-slate font-semibold">
                    <ArrowUpRight className="w-4 h-4 text-brand-blue shrink-0 mt-0.5" />
                    <p className="leading-tight text-gray-600">
                      <span className="font-extrabold text-brand-slate">Action Required: </span>
                      {alert.recommendation}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
