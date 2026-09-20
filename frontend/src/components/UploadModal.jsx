import React, { useState, useRef } from 'react'
import { X, UploadCloud, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react'
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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
      <div className="relative w-full max-w-lg rounded-2xl border border-[#e0e5de] bg-white p-6 shadow-xl">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-[#e0e5de]">
          <div>
            <h3 className="font-serif text-lg font-bold text-[#1f2724]">Upload Statement</h3>
            <p className="text-xs text-[#78827c] mt-0.5">Ingest CSV, Excel, or PDF financial records</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-[#78827c] hover:text-[#1f2724] hover:bg-[#f5f6f2] transition"
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
                    ? 'border-[#1f2724] bg-[#f5f6f2]'
                    : 'border-[#d0d7cf] hover:border-[#1f2724] bg-[#fbfcf9]'
                }`}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls,.pdf,application/pdf"
                  onChange={handleChange}
                  className="hidden"
                />
                <div className="h-12 w-12 rounded-full bg-[#f1f5ed] text-[#58725b] flex items-center justify-center mb-3">
                  <UploadCloud className="w-6 h-6" />
                </div>
                <p className="text-sm font-medium text-[#1f2724]">
                  {selectedFile ? selectedFile.name : 'Select or drop statement file'}
                </p>
                <p className="text-xs text-[#78827c] mt-1">
                  {selectedFile
                    ? `${(selectedFile.size / 1024).toFixed(1)} KB`
                    : 'CSV, XLSX, PDF up to 10MB • Columns auto-detected'}
                </p>
              </div>

              {/* Error Alert */}
              {error && (
                <div className="mt-4 p-3 rounded-lg border border-[#f5d5cc] bg-[#fdf2ef] text-[#c2410c] text-xs flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-[#c2410c] shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}
            </>
          ) : (
            /* Result Summary */
            <div className="space-y-4">
              <div className="p-4 rounded-xl border border-[#d6e8de] bg-[#f1f7f4] flex items-center gap-3 text-[#15803d]">
                <CheckCircle className="w-6 h-6 text-[#15803d] shrink-0" />
                <div>
                  <h4 className="font-serif text-sm font-bold text-[#1f2724]">Statement Ingestion Complete</h4>
                  <p className="text-xs text-[#526057] mt-0.5">
                    Records normalized and categorized into ledger.
                  </p>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-lg border border-[#e0e5de] bg-[#fbfcf9] text-center">
                  <p className="text-[11px] text-[#78827c] font-medium">Imported</p>
                  <p className="font-serif text-xl font-bold text-[#15803d] mt-0.5">{result.imported}</p>
                </div>
                <div className="p-3 rounded-lg border border-[#e0e5de] bg-[#fbfcf9] text-center">
                  <p className="text-[11px] text-[#78827c] font-medium">Skipped</p>
                  <p className="font-serif text-xl font-bold text-[#b45309] mt-0.5">{result.skipped}</p>
                </div>
                <div className="p-3 rounded-lg border border-[#e0e5de] bg-[#fbfcf9] text-center">
                  <p className="text-[11px] text-[#78827c] font-medium">Categorized</p>
                  <p className="font-serif text-xl font-bold text-[#1f2724] mt-0.5">{result.categories_assigned}</p>
                </div>
              </div>

              {/* Warnings if any */}
              {result.warnings && result.warnings.length > 0 && (
                <div className="p-3 rounded-lg border border-[#e0e5de] bg-[#fbfcf9] max-h-36 overflow-y-auto">
                  <p className="text-[11px] font-semibold text-[#78827c] mb-1">Processing Notes:</p>
                  <ul className="text-[11px] text-[#78827c] space-y-1 list-disc list-inside">
                    {result.warnings.slice(0, 5).map((w, idx) => (
                      <li key={idx} className="truncate">{w}</li>
                    ))}
                    {result.warnings.length > 5 && (
                      <li className="text-[#a5ada7] italic">+{result.warnings.length - 5} more notes</li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-[#e0e5de]">
          {!result ? (
            <>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg text-xs font-medium text-[#78827c] hover:text-[#1f2724] transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleUploadSubmit}
                disabled={!selectedFile || isUploading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1f2724] hover:bg-[#2d3834] active:bg-[#151c19] text-white text-xs font-semibold shadow-xs transition disabled:opacity-40"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-[#e8bb62]" />
                    <span>Ingesting records...</span>
                  </>
                ) : (
                  <span>Import Records</span>
                )}
              </button>
            </>
          ) : (
            <div className="flex items-center gap-2 w-full justify-between">
              <button
                type="button"
                onClick={handleReset}
                className="text-xs font-medium text-[#1f2724] underline hover:text-[#2e7d32]"
              >
                Upload another statement
              </button>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-lg bg-[#1f2724] hover:bg-[#2d3834] text-white text-xs font-semibold shadow-xs transition"
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
