import React from 'react'
import { Repeat, Calendar, CheckCircle2 } from 'lucide-react'
import { formatMoney } from '../lib/api'

export default function RecurringList({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-[#e0e5de] bg-white p-6 flex flex-col items-center justify-center min-h-[260px] text-center">
        <div className="h-10 w-10 rounded-xl bg-[#f5f6f2] flex items-center justify-center text-[#78827c] mb-2">
          <Repeat className="w-5 h-5" />
        </div>
        <p className="font-serif text-base font-medium text-[#1f2724]">No Subscriptions Detected</p>
        <p className="text-xs text-[#78827c] max-w-xs mt-1">
          Regular monthly or weekly obligations are automatically identified from statement history.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-[#e0e5de] bg-white p-6 shadow-xs flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="font-serif text-xl font-normal text-[#1f2724]">Recurring Obligations</h2>
          <p className="text-xs text-[#78827c] mt-0.5">Identified subscriptions & regular bills</p>
        </div>
        <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-[#f1f5ed] text-[#58725b] border border-[#dfe9db]">
          {data.length} active
        </span>
      </div>

      <div className="divide-y divide-[#f0f2ee]">
        {data.map((item, idx) => {
          const confidencePct = Math.round((item.confidence || 0) * 100)
          return (
            <div key={idx} className="py-3 flex items-center justify-between gap-4 first:pt-0 last:pb-0">
              <div className="flex items-center gap-3 min-w-0">
                <div className="h-9 w-9 rounded-lg bg-[#f5f6f2] border border-[#e0e5de] flex items-center justify-center text-[#1f2724] shrink-0 font-serif font-bold text-xs uppercase">
                  {item.merchant_name.slice(0, 2)}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-[#1f2724] truncate">{item.merchant_name}</p>
                  <div className="flex items-center gap-2 text-xs text-[#78827c] mt-0.5">
                    <span className="inline-flex items-center text-[11px] px-1.5 py-0.5 rounded bg-[#f5f6f2] text-[#526057] capitalize">
                      {item.frequency}
                    </span>
                    <span className="inline-flex items-center gap-1 text-[11px] text-[#15803d]">
                      <CheckCircle2 className="w-3 h-3" />
                      {confidencePct}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-right shrink-0">
                <p className="text-sm font-semibold text-[#1f2724]">
                  {formatMoney(-item.typical_amount_minor)}
                </p>
                {item.next_expected_date && (
                  <p className="text-[11px] text-[#78827c] flex items-center justify-end gap-1 mt-0.5">
                    <Calendar className="w-3 h-3 text-[#9aa49e]" />
                    {item.next_expected_date}
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
