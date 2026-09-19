import React from 'react'
import { ArrowDownLeft, ArrowUpRight, ChevronLeft, ChevronRight, ListFilter } from 'lucide-react'
import { formatMoney } from '../lib/api'

export default function TransactionTable({
  transactions = [],
  total = 0,
  page = 1,
  pageSize = 15,
  onPageChange,
  isLoading = false,
}) {
  const totalPages = Math.ceil(total / pageSize) || 1

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 backdrop-blur flex flex-col shadow-sm overflow-hidden">
      <div className="p-5 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-white">Transaction Ledger</h2>
          <p className="text-xs text-slate-400">
            {total} total records normalized in minor units
          </p>
        </div>

        {/* Pagination controls */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">
            Page {page} of {totalPages}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1 || isLoading}
              className="p-1.5 rounded border border-slate-800 bg-slate-900 text-slate-400 hover:text-white disabled:opacity-40 transition"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages || isLoading}
              className="p-1.5 rounded border border-slate-800 bg-slate-900 text-slate-400 hover:text-white disabled:opacity-40 transition"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {transactions.length === 0 ? (
        <div className="p-10 flex flex-col items-center justify-center text-center">
          <ListFilter className="w-8 h-8 text-slate-600 mb-2" />
          <p className="text-sm font-medium text-slate-300">No Transactions Found</p>
          <p className="text-xs text-slate-500 mt-1">
            Upload your first statement to populate the financial ledger.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-950/40 text-[11px] uppercase tracking-wider text-slate-400">
                <th className="py-3 px-5 font-semibold">Date</th>
                <th className="py-3 px-5 font-semibold">Description</th>
                <th className="py-3 px-5 font-semibold">Category</th>
                <th className="py-3 px-5 font-semibold text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs text-slate-200">
              {transactions.map((txn) => {
                const isIncome = txn.amount_minor > 0
                return (
                  <tr key={txn.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-5 text-slate-400 whitespace-nowrap font-mono text-[11px]">
                      {txn.date}
                    </td>
                    <td className="py-3 px-5 font-medium text-white max-w-xs truncate">
                      <div className="flex items-center gap-2">
                        <span className={`h-6 w-6 rounded-md flex items-center justify-center shrink-0 ${
                          isIncome ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                        }`}>
                          {isIncome ? <ArrowDownLeft className="w-3.5 h-3.5" /> : <ArrowUpRight className="w-3.5 h-3.5" />}
                        </span>
                        <span className="truncate">{txn.description}</span>
                      </div>
                    </td>
                    <td className="py-3 px-5 whitespace-nowrap">
                      <span className="inline-block px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-800 border border-slate-700/60 text-slate-300">
                        {txn.category || 'Other'}
                      </span>
                    </td>
                    <td className={`py-3 px-5 whitespace-nowrap text-right font-semibold font-mono ${
                      isIncome ? 'text-emerald-400' : 'text-slate-100'
                    }`}>
                      {isIncome ? `+${formatMoney(txn.amount_minor, txn.currency)}` : formatMoney(txn.amount_minor, txn.currency)}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
