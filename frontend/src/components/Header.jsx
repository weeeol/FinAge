import React from 'react'
import { ShieldCheck, Upload, RefreshCw } from 'lucide-react'

export default function Header({ onOpenUpload, onRefresh, isRefreshing }) {
  return (
    <header className="border-b border-[#e0e5de] bg-[#fbfcf9] sticky top-0 z-40 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Brand & Subtitle */}
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-[#1f2724] flex items-center justify-center font-serif text-[#e8bb62] font-bold text-base shadow-sm">
            FA
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-serif text-xl font-bold tracking-tight text-[#1f2724]">FinAge</h1>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded bg-[#edf1ec] text-[#58725b] border border-[#dfe9db]">
                Workspace
              </span>
            </div>
            <p className="text-xs text-[#78827c]">Personal Finance Decision Support</p>
          </div>
        </div>

        {/* Center disclaimer badge */}
        <div className="hidden lg:flex items-center gap-2 text-xs text-[#58725b] bg-[#f1f5ed] border border-[#dfe9db] rounded-full px-3.5 py-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-[#58725b]" />
          <span>Decision support • Not investment advice</span>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="p-2 rounded-lg border border-[#e0e5de] bg-white text-[#78827c] hover:text-[#1f2724] hover:bg-[#edf1ec] transition disabled:opacity-50"
            title="Refresh dashboard data"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-[#1f2724]' : ''}`} />
          </button>

          <button
            onClick={onOpenUpload}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1f2724] hover:bg-[#2d3834] active:bg-[#151c19] text-white text-xs font-semibold shadow-sm transition"
          >
            <Upload className="w-4 h-4 text-[#e8bb62]" />
            <span>Upload Statement</span>
          </button>
        </div>
      </div>
    </header>
  )
}
