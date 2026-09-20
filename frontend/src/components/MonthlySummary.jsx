import React, { useState } from 'react'
import { FileText, ChevronRight, AlertCircle, TrendingUp, CheckCircle, ArrowRight } from 'lucide-react'
import { fetchMonthlySummary, formatMoney } from '../lib/api'

export default function MonthlySummary({ currentMonth = '2026-01' }) {
  const [summary, setSummary] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await fetchMonthlySummary(currentMonth)
      setSummary(data)
    } catch (err) {
      setError(err.message || 'Failed to generate monthly brief.')
    } finally {
      setIsLoading(false)
    }
  }

  const getInsightIcon = (insight) => {
    switch (insight.type) {
      case 'anomaly': return <AlertCircle className="w-4 h-4 text-[#c05346]" />
      case 'budget': return <TrendingUp className="w-4 h-4 text-[#c89234]" />
      case 'goal': return <CheckCircle className="w-4 h-4 text-[#58725b]" />
      default: return <ChevronRight className="w-4 h-4 text-[#78827c]" />
    }
  }

  const getInsightDot = (severity) => {
    if (severity === 'warning') return 'bg-[#c05346]' // Coral
    return 'bg-[#c89234]' // Gold/Info
  }

  if (!summary && !isLoading && !error) {
    return (
      <div className="bg-[#f8faf4] border border-[#e0e5de] rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm mb-6">
        <div>
          <h2 className="font-serif text-xl text-[#1f2724] mb-1">Monthly Executive Brief</h2>
          <p className="text-sm text-[#526057]">Generate a deterministic financial summary and insights for {currentMonth}.</p>
        </div>
        <button 
          onClick={handleGenerate}
          className="flex items-center gap-2 bg-[#1f2724] text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-[#58725b] transition-colors whitespace-nowrap"
        >
          <FileText className="w-4 h-4" /> Generate Brief
        </button>
      </div>
    )
  }

  return (
    <div className="bg-white border border-[#e0e5de] rounded-xl p-6 shadow-sm mb-6">
      <div className="flex items-center justify-between border-b border-[#e5e9e2] pb-4 mb-4">
        <div>
          <h2 className="font-serif text-xl text-[#1f2724]">Executive Brief: {currentMonth}</h2>
          <p className="text-[11px] font-bold uppercase tracking-wider text-[#78827c] mt-1">Deterministic Analysis</p>
        </div>
        <button 
          onClick={handleGenerate}
          disabled={isLoading}
          className="flex items-center gap-1.5 bg-white border border-[#c3c9c3] text-[#1f2724] px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-[#f8faf4] transition-colors disabled:opacity-50"
        >
          <RefreshCwIcon className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} /> Refresh
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-[#f5d5cc] bg-[#fdf2ef] p-3 text-[#c2410c] text-xs flex items-center gap-2 mb-4">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Column 1: Financial Snapshot */}
          <div className="md:col-span-1 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wide text-[#78827c]">Net Position</h3>
            
            <div className="bg-[#f8faf4] p-4 rounded-lg border border-[#e5e9e2]">
              <div className="text-2xl font-serif mb-1">
                {formatMoney(summary.net_minor)}
              </div>
              <div className="text-xs text-[#526057]">
                Net {summary.net_minor >= 0 ? 'Surplus' : 'Deficit'}
              </div>
              
              <div className="mt-4 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#526057]">Income</span>
                  <span className="font-semibold text-[#1f2724]">{formatMoney(summary.income_minor)}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#526057]">Expenses</span>
                  <span className="font-semibold text-[#c05346]">{formatMoney(summary.expense_minor)}</span>
                </div>
              </div>
            </div>

            <h3 className="text-xs font-bold uppercase tracking-wide text-[#78827c] mt-2">Top Drivers</h3>
            <div className="space-y-2">
              {summary.top_categories.map((c, i) => (
                <div key={i} className="flex justify-between text-xs py-1 border-b border-dashed border-[#e5e9e2] last:border-0">
                  <span className="text-[#526057]">{c.category}</span>
                  <span className="font-semibold">{formatMoney(c.amount_minor)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Column 2: Insights */}
          <div className="md:col-span-2">
            <h3 className="text-xs font-bold uppercase tracking-wide text-[#78827c] mb-4">Key Insights</h3>
            
            {summary.insights.length === 0 ? (
              <div className="text-sm text-[#78827c] py-4 bg-[#faf9f5] rounded-lg text-center border border-dashed border-[#e5e9e2]">
                No significant anomalies or warnings detected for this month.
              </div>
            ) : (
              <div className="space-y-3">
                {summary.insights.map((insight, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-[#faf9f5] rounded-lg border border-[#e5e9e2]">
                    <div className="mt-0.5">
                      {getInsightIcon(insight)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className={`w-1.5 h-1.5 rounded-full ${getInsightDot(insight.severity)}`}></span>
                        <h4 className="text-sm font-semibold text-[#1f2724]">{insight.title}</h4>
                      </div>
                      <p className="text-xs text-[#526057] leading-relaxed">
                        {insight.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function RefreshCwIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
      <path d="M3 3v5h5" />
    </svg>
  )
}
