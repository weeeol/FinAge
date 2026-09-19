import React, { useState, useRef } from 'react'
import { X, UploadCloud, FileText, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react'
import { uploadFile } from '../lib/api'

export default function UploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const inputRef = useRef(null)

  if (!isOpen) return null

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = (file) => {
    setSelectedFile(file)
    setError(null)
    setResult(null)
  }

  const handleUploadSubmit = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setError(null)
    setResult(null)

    try {
      const response = await uploadFile(selectedFile)
      setResult(response)
      if (onUploadSuccess) {
        onUploadSuccess()
      }
    } catch (err) {
      setError(err.message || 'An error occurred during statement upload.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h3 className="text-lg font-semibold text-white">Upload Financial Statement</h3>
            <p className="text-xs text-slate-400 mt-0.5">Accepts CSV and Excel (.xlsx) bank records</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="py-5">
          {!result ? (
            <>
              {/* Dropzone */}
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
                className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition ${
                  dragActive
                    ? 'border-indigo-500 bg-indigo-500/10'
                    : 'border-slate-700 hover:border-indigo-500/50 hover:bg-slate-800/40 bg-slate-950/40'
                }`}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleChange}
                  className="hidden"
                />
                <div className="h-12 w-12 rounded-full bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-3">
                  <UploadCloud className="w-6 h-6" />
                </div>
                <p className="text-sm font-medium text-white">
                  {selectedFile ? selectedFile.name : 'Click to browse or drop statement here'}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  {selectedFile
                    ? `${(selectedFile.size / 1024).toFixed(1)} KB`
                    : 'CSV, XLSX up to 10MB • Columns auto-detected'}
                </p>
              </div>

              {/* Error Alert */}
              {error && (
                <div className="mt-4 p-3 rounded-lg border border-rose-500/30 bg-rose-500/10 text-rose-300 text-xs flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}
            </>
          ) : (
            /* Result Summary */
            <div className="space-y-4">
              <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 flex items-center gap-3 text-emerald-300">
                <CheckCircle className="w-6 h-6 text-emerald-400 shrink-0" />
                <div>
                  <h4 className="text-sm font-semibold text-white">Import Complete</h4>
                  <p className="text-xs text-emerald-300/90 mt-0.5">
                    Your financial statement was parsed and normalized.
                  </p>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-lg border border-slate-800 bg-slate-950/50 text-center">
                  <p className="text-[11px] text-slate-400 font-medium">Imported</p>
                  <p className="text-lg font-bold text-emerald-400 mt-0.5">{result.imported}</p>
                </div>
                <div className="p-3 rounded-lg border border-slate-800 bg-slate-950/50 text-center">
                  <p className="text-[11px] text-slate-400 font-medium">Skipped</p>
                  <p className="text-lg font-bold text-amber-400 mt-0.5">{result.skipped}</p>
                </div>
                <div className="p-3 rounded-lg border border-slate-800 bg-slate-950/50 text-center">
                  <p className="text-[11px] text-slate-400 font-medium">Categorized</p>
                  <p className="text-lg font-bold text-indigo-400 mt-0.5">{result.categories_assigned}</p>
                </div>
              </div>

              {/* Warnings if any */}
              {result.warnings && result.warnings.length > 0 && (
                <div className="p-3 rounded-lg border border-slate-800 bg-slate-950/50 max-h-36 overflow-y-auto">
                  <p className="text-[11px] font-semibold text-slate-400 mb-1">Processing Notes:</p>
                  <ul className="text-[11px] text-slate-400 space-y-1 list-disc list-inside">
                    {result.warnings.slice(0, 5).map((w, idx) => (
                      <li key={idx} className="truncate">{w}</li>
                    ))}
                    {result.warnings.length > 5 && (
                      <li className="text-slate-500 italic">+{result.warnings.length - 5} more warnings</li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
          {!result ? (
            <>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg text-xs font-medium text-slate-400 hover:text-white transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleUploadSubmit}
                disabled={!selectedFile || isUploading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition disabled:opacity-40"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing statement...</span>
                  </>
                ) : (
                  <span>Upload & Ingest</span>
                )}
              </button>
            </>
          ) : (
            <div className="flex items-center gap-2 w-full justify-between">
              <button
                type="button"
                onClick={handleReset}
                className="text-xs font-medium text-indigo-400 hover:underline"
              >
                Upload another file
              </button>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition"
              >
                Done
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
