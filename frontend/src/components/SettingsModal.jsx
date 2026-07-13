import React, { useState, useEffect } from 'react';
import { X, Globe, Wifi, WifiOff, Loader } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose, apiUrl, onSave }) {
  const [tempUrl, setTempUrl] = useState(apiUrl);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    setTempUrl(apiUrl);
    setTestResult(null);
  }, [apiUrl, isOpen]);

  if (!isOpen) return null;

  const testConnection = async () => {
    setTesting(true);
    setTestResult(null);
    const testUrl = `${tempUrl}/`;
    console.log(`[API Settings Test] Requesting GET ${testUrl}`);
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 3000); // 3-second timeout

      const res = await fetch(testUrl, {
        method: 'GET',
        signal: controller.signal
      });
      clearTimeout(id);

      console.log(`[API Settings Test] Response status: ${res.status}`);

      if (res.ok) {
        const data = await res.json();
        console.log("[API Settings Test] Response payload:", data);
        setTestResult({
          status: 'success',
          message: data.message || 'Connection successful!'
        });
      } else {
        let errMsg = `Server returned status: ${res.status}`;
        try {
          const errData = await res.json();
          console.log("[API Settings Test] Error response payload:", errData);
          if (errData && errData.detail) {
            errMsg = errData.detail;
          } else if (errData && errData.message) {
            errMsg = errData.message;
          }
        } catch (_) {}
        setTestResult({
          status: 'error',
          message: errMsg
        });
      }
    } catch (e) {
      console.error(`[API Settings Test] Connection test failed for ${testUrl}:`, e);
      setTestResult({
        status: 'error',
        message: `Could not connect to server: ${e.message}. Ensure CORS is enabled and API is running.`
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    onSave(tempUrl);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center animate-fade-in">
      <div className="bg-brand-white w-full max-w-md rounded-2xl shadow-xl overflow-hidden border border-gray-200">
        {/* Modal Header */}
        <div className="bg-brand-slate text-brand-white px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Globe className="w-5 h-5 text-brand-blue" />
            <h2 className="font-semibold text-lg">API Settings</h2>
          </div>
          <button onClick={onClose} className="text-gray-300 hover:text-brand-white transition-all">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-semibold text-brand-slate mb-1">
              FastAPI Endpoint URL
            </label>
            <input
              type="text"
              value={tempUrl}
              onChange={(e) => setTempUrl(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent text-brand-slate font-mono bg-brand-platinum/30"
              placeholder="http://localhost:8000"
            />
            <p className="text-xs text-gray-500 mt-1">
              Default local API: <code className="bg-brand-platinum px-1 py-0.5 rounded">http://localhost:8000</code>
            </p>
          </div>

          {/* Test Status Info */}
          {testResult && (
            <div
              className={`p-3 rounded-lg border text-xs flex items-start space-x-2 ${
                testResult.status === 'success'
                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                  : 'bg-red-50 text-red-800 border-red-200'
              }`}
            >
              {testResult.status === 'success' ? (
                <Wifi className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
              ) : (
                <WifiOff className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
              )}
              <span>{testResult.message}</span>
            </div>
          )}

          {/* Connection Test Actions */}
          <div className="flex space-x-3 pt-2">
            <button
              onClick={testConnection}
              disabled={testing}
              className="flex-1 px-4 py-2 border border-brand-blue text-brand-blue rounded-lg text-sm font-semibold hover:bg-brand-blue/5 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {testing ? (
                <>
                  <Loader className="w-4 h-4 animate-spin" />
                  <span>Connecting...</span>
                </>
              ) : (
                <span>Test Connection</span>
              )}
            </button>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3 border-t border-gray-100">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 text-brand-slate hover:bg-brand-platinum rounded-lg text-sm font-semibold transition-all"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-brand-slate text-brand-white hover:bg-brand-slate/90 rounded-lg text-sm font-semibold transition-all shadow-sm"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
