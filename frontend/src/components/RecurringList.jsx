import React from 'react'
import { Repeat, Calendar, CheckCircle2 } from 'lucide-react'
import { formatMoney } from '../lib/api'

export default function RecurringList({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 flex flex-col items-center justify-center min-h-[220px] text-center">
        <Repeat className="w-9 h-9 text-slate-600 mb-2" />
        <p className="text-sm font-medium text-slate-300">No Recurring Subscriptions Found</p>
        <p className="text-xs text-slate-500 max-w-sm mt-1">
          Repeated monthly or weekly payments will automatically be detected and projected here.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex flex-col shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-semibold text-white">Recurring Obligations</h2>
          <p className="text-xs text-slate-400">Detected subscriptions & regular bills</p>
        </div>
        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
          {data.length} active
        </span>
      </div>

      <div className="divide-y divide-slate-800/80">
        {data.map((item, idx) => {
          const confidencePct = Math.round((item.confidence || 0) * 100)
          return (
            <div key={idx} className="py-3 flex items-center justify-between gap-4 first:pt-0 last:pb-0">
              <div className="flex items-center gap-3 min-w-0">
                <div className="h-9 w-9 rounded-lg bg-slate-800 flex items-center justify-center text-slate-300 shrink-0 font-bold text-xs uppercase">
                  {item.merchant_name.slice(0, 2)}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-white truncate">{item.merchant_name}</p>
                  <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                    <span className="inline-flex items-center gap-1 text-[11px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 capitalize">
                      {item.frequency}
                    </span>
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-400">
                      <CheckCircle2 className="w-3 h-3" />
                      {confidencePct}% confidence
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-right shrink-0">
                <p className="text-sm font-semibold text-white">
                  {formatMoney(-item.typical_amount_minor)}
                </p>
                {item.next_expected_date && (
                  <p className="text-[11px] text-slate-400 flex items-center justify-end gap-1 mt-0.5">
                    <Calendar className="w-3 h-3 text-slate-500" />
                    Due {item.next_expected_date}
                  </p>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
