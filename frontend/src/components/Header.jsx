import React from 'react'
import { ShieldCheck, Upload, RefreshCw } from 'lucide-react'

export default function Header({ onOpenUpload, onRefresh, isRefreshing }) {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Logo & Subtitle */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center font-black text-white shadow-lg shadow-indigo-500/25">
            FP
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">FinPilot</h1>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                MVP
              </span>
            </div>
            <p className="text-xs text-slate-400">AI Personal Finance Decision Support</p>
          </div>
        </div>

        {/* Center disclaimer badge */}
        <div className="hidden lg:flex items-center gap-2 text-xs text-slate-400 bg-slate-900/60 border border-slate-800/80 rounded-full px-3.5 py-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
          <span>Decision support • Not investment advice</span>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="p-2 rounded-lg border border-slate-800 bg-slate-900/60 text-slate-400 hover:text-white hover:bg-slate-800/80 transition disabled:opacity-50"
            title="Refresh dashboard data"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-indigo-400' : ''}`} />
          </button>

          <button
            onClick={onOpenUpload}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-sm font-medium shadow-lg shadow-indigo-600/25 transition"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Statement</span>
          </button>
        </div>
      </div>
    </header>
  )
}
