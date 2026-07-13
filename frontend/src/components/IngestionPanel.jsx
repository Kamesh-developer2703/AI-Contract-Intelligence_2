import React, { useRef, useState } from 'react';
import { Upload, FileText, CheckCircle2, Loader2, AlertTriangle, XCircle } from 'lucide-react';

export default function IngestionPanel({ currentStep, fileName, onFileSelected, stepsStatus }) {
  const fileInputRef = useRef(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      validateAndProcessFile(file);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndProcessFile(e.target.files[0]);
    }
  };

  const validateAndProcessFile = (file) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
    const ext = file.name.split('.').pop().toLowerCase();
    if (validTypes.includes(file.type) || ['pdf', 'docx', 'doc'].includes(ext)) {
      onFileSelected(file);
    } else {
      alert("Invalid file type. Please upload a PDF or Word document (.docx/.doc).");
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="bg-brand-white rounded-2xl shadow-sm border border-gray-200/80 p-6 flex flex-col h-full space-y-6">
      {/* Panel Header */}
      <div>
        <h2 className="text-lg font-bold text-brand-slate tracking-tight">Contract Upload</h2>
        <p className="text-xs text-gray-400 font-semibold">Select a contract agreement for instant legal review</p>
      </div>

      {/* Styled File Upload Area (Pacific Blue border / hover) */}
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={triggerFileInput}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 flex flex-col items-center justify-center space-y-3 grow ${
          isDragActive
            ? 'border-brand-blue bg-brand-blue/5'
            : fileName
            ? 'border-emerald-300 bg-emerald-50/20'
            : 'border-brand-blue/60 hover:border-brand-blue hover:bg-brand-blue/5'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          className="hidden"
        />

        {fileName ? (
          <>
            <div className={`p-3 rounded-full border shadow-inner ${
              stepsStatus.step1 === 'error' || stepsStatus.step2 === 'error' || stepsStatus.step3 === 'error'
                ? 'bg-red-50 text-red-600 border-red-200'
                : stepsStatus.step3 === 'completed'
                ? 'bg-emerald-50 text-emerald-600 border-emerald-200'
                : 'bg-brand-blue/10 text-brand-blue border-brand-blue/20 animate-pulse'
            }`}>
              {stepsStatus.step1 === 'error' || stepsStatus.step2 === 'error' || stepsStatus.step3 === 'error' ? (
                <XCircle className="w-8 h-8" />
              ) : stepsStatus.step3 === 'completed' ? (
                <CheckCircle2 className="w-8 h-8" />
              ) : (
                <FileText className="w-8 h-8" />
              )}
            </div>
            <div>
              <p className="text-sm font-bold text-brand-slate max-w-[200px] truncate" title={fileName}>
                {fileName}
              </p>
              {stepsStatus.step1 === 'error' || stepsStatus.step2 === 'error' || stepsStatus.step3 === 'error' ? (
                <p className="text-xs text-red-500 mt-1 font-bold">Analysis Failed. Click to retry.</p>
              ) : stepsStatus.step3 === 'completed' ? (
                <p className="text-xs text-emerald-600 mt-1 font-bold">Analysis Completed</p>
              ) : (
                <p className="text-xs text-brand-blue mt-1 font-semibold animate-pulse">Analysis In Progress...</p>
              )}
            </div>
          </>
        ) : (
          <>
            <div className="bg-brand-blue/10 text-brand-blue p-4 rounded-full border border-brand-blue/20 shadow-sm">
              <Upload className="w-8 h-8" />
            </div>
            <div>
              <p className="text-sm font-bold text-brand-slate">
                Drag & Drop Document
              </p>
              <p className="text-xs text-gray-400 mt-1">or click to browse local files</p>
            </div>
            
            <div className="text-[9px] text-gray-400 font-bold uppercase tracking-wider bg-brand-platinum/70 px-2 py-0.5 rounded">
              PDF, DOC, DOCX
            </div>
          </>
        )}
      </div>

      {/* Steps Pipeline Tracker */}
      <div className="border-t border-gray-100 pt-6">
        <h3 className="text-xs font-bold text-brand-slate uppercase tracking-wider mb-4">
          Document Analysis Status
        </h3>
        
        <div className="relative pl-6 border-l border-gray-200 ml-3 space-y-6">
          {/* Step 1 */}
          <div className="relative">
            <div className={`absolute -left-[30px] top-0.5 rounded-full p-0.5 border ${
              stepsStatus.step1 === 'completed'
                ? 'bg-emerald-50 border-emerald-500 text-emerald-600'
                : stepsStatus.step1 === 'processing'
                ? 'bg-brand-blue/10 border-brand-blue text-brand-blue'
                : 'bg-brand-white border-gray-200 text-gray-300'
            }`}>
              {stepsStatus.step1 === 'completed' ? (
                <CheckCircle2 className="w-4 h-4 shrink-0" />
              ) : stepsStatus.step1 === 'processing' ? (
                <Loader2 className="w-4 h-4 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 flex items-center justify-center text-[10px] font-bold">1</div>
              )}
            </div>
            <div>
              <p className={`text-xs font-bold ${
                stepsStatus.step1 === 'completed'
                  ? 'text-brand-slate'
                  : stepsStatus.step1 === 'processing'
                  ? 'text-brand-blue'
                  : 'text-gray-400'
              }`}>
                Step 1: Reading Document
              </p>
              <p className="text-[10px] text-gray-400 mt-0.5 font-medium">
                Parsing agreement text & layout hierarchy.
              </p>
            </div>
          </div>

          {/* Step 2 */}
          <div className="relative">
            <div className={`absolute -left-[30px] top-0.5 rounded-full p-0.5 border ${
              stepsStatus.step2 === 'completed'
                ? 'bg-emerald-50 border-emerald-500 text-emerald-600'
                : stepsStatus.step2 === 'processing'
                ? 'bg-brand-blue/10 border-brand-blue text-brand-blue'
                : 'bg-brand-white border-gray-200 text-gray-300'
            }`}>
              {stepsStatus.step2 === 'completed' ? (
                <CheckCircle2 className="w-4 h-4 shrink-0" />
              ) : stepsStatus.step2 === 'processing' ? (
                <Loader2 className="w-4 h-4 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 flex items-center justify-center text-[10px] font-bold">2</div>
              )}
            </div>
            <div>
              <p className={`text-xs font-bold ${
                stepsStatus.step2 === 'completed'
                  ? 'text-brand-slate'
                  : stepsStatus.step2 === 'processing'
                  ? 'text-brand-blue'
                  : 'text-gray-400'
              }`}>
                Step 2: Checking Parties & Dates
              </p>
              <p className="text-[10px] text-gray-400 mt-0.5 font-medium">
                Identifying key stakeholders, dates, and jurisdictions.
              </p>
            </div>
          </div>

          {/* Step 3 */}
          <div className="relative">
            <div className={`absolute -left-[30px] top-0.5 rounded-full p-0.5 border ${
              stepsStatus.step3 === 'completed'
                ? 'bg-emerald-50 border-emerald-500 text-emerald-600'
                : stepsStatus.step3 === 'processing'
                ? 'bg-brand-blue/10 border-brand-blue text-brand-blue'
                : 'bg-brand-white border-gray-200 text-gray-300'
            }`}>
              {stepsStatus.step3 === 'completed' ? (
                <CheckCircle2 className="w-4 h-4 shrink-0" />
              ) : stepsStatus.step3 === 'processing' ? (
                <Loader2 className="w-4 h-4 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 flex items-center justify-center text-[10px] font-bold">3</div>
              )}
            </div>
            <div>
              <p className={`text-xs font-bold ${
                stepsStatus.step3 === 'completed'
                  ? 'text-brand-slate'
                  : stepsStatus.step3 === 'processing'
                  ? 'text-brand-blue'
                  : 'text-gray-400'
              }`}>
                Step 3: Calculating Risk Profile
              </p>
              <p className="text-[10px] text-gray-400 mt-0.5 font-medium">
                Generating risk metrics & anomalous language logs.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
