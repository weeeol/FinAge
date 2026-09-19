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
    <div className="rounded-xl border border-[#e0e5de] bg-white shadow-xs flex flex-col overflow-hidden">
      <div className="p-6 border-b border-[#e0e5de] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="font-serif text-xl font-normal text-[#1f2724]">Transaction Ledger</h2>
          <p className="text-xs text-[#78827c] mt-0.5">
            {total} normalized statement records
          </p>
        </div>

        {/* Pagination controls */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#78827c]">
            Page {page} of {totalPages}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1 || isLoading}
              className="p-1.5 rounded border border-[#e0e5de] bg-white text-[#78827c] hover:text-[#1f2724] hover:bg-[#edf1ec] disabled:opacity-40 transition"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages || isLoading}
              className="p-1.5 rounded border border-[#e0e5de] bg-white text-[#78827c] hover:text-[#1f2724] hover:bg-[#edf1ec] disabled:opacity-40 transition"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {transactions.length === 0 ? (
        <div className="p-12 flex flex-col items-center justify-center text-center">
          <div className="h-12 w-12 rounded-xl bg-[#f5f6f2] flex items-center justify-center text-[#78827c] mb-2">
            <ListFilter className="w-6 h-6" />
          </div>
          <p className="font-serif text-base font-medium text-[#1f2724]">No Transactions Available</p>
          <p className="text-xs text-[#78827c] mt-1 max-w-sm">
            Upload statements to populate the financial ledger.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#e0e5de] bg-[#fbfcf9] text-[11px] uppercase tracking-wider text-[#78827c]">
                <th className="py-3 px-6 font-semibold">Date</th>
                <th className="py-3 px-6 font-semibold">Description</th>
                <th className="py-3 px-6 font-semibold">Category</th>
                <th className="py-3 px-6 font-semibold text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f0f2ee] text-xs">
              {transactions.map((txn) => {
                const isIncome = txn.amount_minor > 0
                return (
                  <tr key={txn.id} className="hover:bg-[#fbfcf9] transition-colors">
                    <td className="py-3 px-6 text-[#78827c] whitespace-nowrap font-mono text-[11px]">
                      {txn.date}
                    </td>
                    <td className="py-3 px-6 font-medium text-[#1f2724] max-w-xs truncate">
                      <div className="flex items-center gap-2.5">
                        <span className={`h-6 w-6 rounded-md flex items-center justify-center shrink-0 ${
                          isIncome ? 'bg-[#f1f7f4] text-[#15803d]' : 'bg-[#fdf2ef] text-[#c2410c]'
                        }`}>
                          {isIncome ? <ArrowDownLeft className="w-3.5 h-3.5" /> : <ArrowUpRight className="w-3.5 h-3.5" />}
                        </span>
                        <span className="truncate">{txn.description}</span>
                      </div>
                    </td>
                    <td className="py-3 px-6 whitespace-nowrap">
                      <span className="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-[#f5f6f2] border border-[#e0e5de] text-[#526057]">
                        {txn.category || 'Other'}
                      </span>
                    </td>
                    <td className={`py-3 px-6 whitespace-nowrap text-right font-semibold font-mono ${
                      isIncome ? 'text-[#15803d]' : 'text-[#1f2724]'
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
