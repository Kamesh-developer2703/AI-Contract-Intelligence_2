import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import IngestionPanel from './components/IngestionPanel';
import RiskDashboard from './components/RiskDashboard';
import MetadataTabs from './components/MetadataTabs';
import SettingsModal from './components/SettingsModal';

// Helper to perform fetch with a timeout to prevent infinite hangs
const fetchWithTimeout = async (url, options = {}, timeoutMs = 60000) => {
  const controller = new AbortController();
  const { signal } = options;
  if (signal) {
    signal.addEventListener('abort', () => controller.abort());
  }
  const timeoutId = setTimeout(() => {
    console.warn(`[API Timeout] Request to ${url} exceeded ${timeoutMs}ms`);
    controller.abort();
  }, timeoutMs);

  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timeoutId);
    return res;
  } catch (err) {
    clearTimeout(timeoutId);
    throw err;
  }
};

export default function App() {
  const [apiUrl, setApiUrl] = useState(() => {
    const stored = localStorage.getItem('contract_api_url');
    if (stored) return stored;

    if (import.meta.env.VITE_API_URL) {
      return import.meta.env.VITE_API_URL;
    }

    // Dynamically match the current browser hostname on port 8000
    if (typeof window !== 'undefined') {
      let hostname = window.location.hostname;
      if (hostname) {
        // Resolve 0.0.0.0 to localhost (browsers cannot fetch directly from 0.0.0.0)
        const targetHost = hostname === '0.0.0.0' ? 'localhost' : hostname;
        return `http://${targetHost}:8000`;
      }
    }
    return 'http://localhost:8000';
  });
  const [isConnected, setIsConnected] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // File pipeline state
  const [fileName, setFileName] = useState('');
  const [stepsStatus, setStepsStatus] = useState({
    step1: 'idle', // 'idle' | 'processing' | 'completed' | 'error'
    step2: 'idle',
    step3: 'idle',
  });

  // Extraction results state
  const [riskScore, setRiskScore] = useState(0);
  const [alerts, setAlerts] = useState([]);
  const [entities, setEntities] = useState({
    ORG: [],
    DATE: [],
    MONEY: [],
    LOCATION: []
  });
  const [clauses, setClauses] = useState([]);

  // Check backend health status silently with logging
  useEffect(() => {
    const checkHealth = async () => {
      const healthUrl = `${apiUrl}/`;
      console.log(`[Health Check] Requesting GET ${healthUrl}`);
      try {
        const res = await fetchWithTimeout(healthUrl, { method: 'GET' }, 2000);
        console.log(`[Health Check] Response status: ${res.status}`);
        if (res.ok) {
          const data = await res.json().catch(() => ({}));
          console.log("[Health Check] Response payload:", data);
          setIsConnected(true);
        } else {
          setIsConnected(false);
        }
      } catch (e) {
        console.error(`[Health Check] Connection failed to ${healthUrl}:`, e);
        setIsConnected(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, [apiUrl]);

  const handleSaveApiUrl = (newUrl) => {
    setApiUrl(newUrl);
    localStorage.setItem('contract_api_url', newUrl);
  };

  // Bind Unified Analysis Payload straight to states
  const bindAnalysisPayload = (payload) => {
    // 1. Map risk_score directly to Risk Assessment Gauge
    setRiskScore(payload.risk_score || 0);

    // 2. Map warnings directly to Critical Risk Warnings list (Translating keys: type -> clause, rec -> recommendation)
    const mappedWarnings = (payload.warnings || []).map(w => ({
      clause: w.type || "General Warning",
      severity: w.severity ? w.severity.replace(" Risk", "") : "High",
      text: w.text || "",
      recommendation: w.rec || w.recommendation || ""
    }));
    setAlerts(mappedWarnings);

    // 3. Map entities.ORG, DATE, MONEY, and LOCATION directly to highlights tabs
    setEntities({
      ORG: payload.entities?.ORG || [],
      DATE: payload.entities?.DATE || [],
      MONEY: payload.entities?.MONEY || [],
      LOCATION: payload.entities?.LOCATION || []
    });

    // 4. Map clauses directly if available, else fallback to text parser
    if (payload.clauses) {
      setClauses(payload.clauses);
    } else if (payload.text) {
      const paragraphs = payload.text.split('\n\n').filter(p => p.trim().length > 30).slice(0, 4);
      const list = paragraphs.map((p, idx) => {
        let type = "General Covenants";
        if (p.toLowerCase().includes("confidential") || p.toLowerCase().includes("disclosure")) {
          type = "Confidentiality Covenants";
        } else if (p.toLowerCase().includes("liability") || p.toLowerCase().includes("cap")) {
          type = "Limitation of Liability";
        } else if (p.toLowerCase().includes("terminate") || p.toLowerCase().includes("notice")) {
          type = "Termination Notice";
        } else if (p.toLowerCase().includes("indemnity") || p.toLowerCase().includes("defend")) {
          type = "Indemnification Covenants";
        }
        return {
          clause_type: type,
          confidence: 0.95 - idx * 0.04,
          text: p.trim(),
          parameters: {}
        };
      });
      setClauses(list);
    } else {
      setClauses([]);
    }
  };

  const handleFileSelected = async (file) => {
    setFileName(file.name);
    
    // Reset output states, clearing out all default dummy fallbacks
    setRiskScore(0);
    setAlerts([]);
    setEntities({ ORG: [], DATE: [], MONEY: [], LOCATION: [] });
    setClauses([]);
    
    try {
      setStepsStatus({ step1: 'processing', step2: 'idle', step3: 'idle' });

      // 1. Upload File binary to /upload
      const formData = new FormData();
      formData.append('file', file);
      
      const uploadUrl = `${apiUrl}/upload`;
      console.log(`[API Request] Posting file to: ${uploadUrl}`);
      
      const uploadRes = await fetchWithTimeout(uploadUrl, {
        method: 'POST',
        body: formData,
      }, 45000); // 45s timeout for file upload

      console.log(`[API Response] Upload status: ${uploadRes.status}`);

      if (!uploadRes.ok) {
        let errMsg = "File upload failed";
        try {
          const errData = await uploadRes.json();
          if (errData && errData.detail) {
            errMsg = errData.detail;
          } else if (errData && errData.message) {
            errMsg = errData.message;
          }
        } catch (_) {}
        throw new Error(errMsg);
      }

      const uploadData = await uploadRes.json();
      console.log("[API Response Payload] Upload success:", uploadData);
      
      // 2. OCR Text Analysis (Step 1 completed, Step 2 processing)
      setStepsStatus(prev => ({ ...prev, step1: 'completed', step2: 'processing' }));
      
      // 3. Run Unified Analysis via GET /analyze (includes OCR, NER, and Classification)
      const analyzeUrl = `${apiUrl}/analyze`;
      console.log(`[API Request] Requesting OCR analyze from: ${analyzeUrl}`);
      
      const analyzeRes = await fetchWithTimeout(analyzeUrl, { method: 'GET' }, 90000); // 90s timeout for OCR & ML
      console.log(`[API Response] Analyze status: ${analyzeRes.status}`);

      if (!analyzeRes.ok) {
        let errMsg = "OCR text extraction failed";
        try {
          const errData = await analyzeRes.json();
          if (errData && errData.detail) {
            errMsg = errData.detail;
          } else if (errData && errData.message) {
            errMsg = errData.message;
          }
        } catch (_) {}
        throw new Error(errMsg);
      }
      
      const analyzeData = await analyzeRes.json();
      console.log("[API Response Payload] Unified analyze success, risk score:", analyzeData.risk_score);

      // 4. Bind Unified Analysis Payload straight to states
      setStepsStatus(prev => ({ ...prev, step2: 'completed', step3: 'processing' }));
      
      bindAnalysisPayload(analyzeData);

      setStepsStatus(prev => ({ ...prev, step3: 'completed' }));
    } catch (err) {
      console.error("[Live API Error] Connection failed: ", err);
      setStepsStatus({ step1: 'error', step2: 'error', step3: 'error' });
      alert(`Backend Analysis Failed: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-brand-platinum flex flex-col font-sans">
      {/* Lawyer Header */}
      <Header
        toggleMockMode={() => {
          console.log("[Dev Mode] Toggle bypassed. Live connection is mandatory.");
        }}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* Main Grid Workspace: Platinum background */}
      <main className="grow p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto w-full">
        {/* Left Column: Upload */}
        <section className="lg:col-span-4 flex flex-col">
          <IngestionPanel
            currentStep={fileName ? (stepsStatus.step3 === 'completed' ? 3 : stepsStatus.step2 === 'completed' ? 2 : 1) : 0}
            fileName={fileName}
            onFileSelected={handleFileSelected}
            stepsStatus={stepsStatus}
          />
        </section>

        {/* Center Column: Risk Assessment Gauge */}
        <section className="lg:col-span-4 flex flex-col">
          <RiskDashboard
            riskScore={riskScore}
            alerts={alerts}
          />
        </section>

        {/* Right Column: Contract Review Tabs */}
        <section className="lg:col-span-4 flex flex-col">
          <MetadataTabs
            entities={entities}
            clauses={clauses}
          />
        </section>
      </main>

      {/* Settings Modal (Developer Gestures Only) */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiUrl={apiUrl}
        onSave={handleSaveApiUrl}
      />
    </div>
  );
}
