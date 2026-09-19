import React from 'react'
import { TrendingUp, TrendingDown, Wallet, Hash } from 'lucide-react'
import { formatMoney } from '../lib/api'

export default function SummaryCards({ summary, isLoading }) {
  const income = summary?.income_minor ?? 0
  const expense = summary?.expense_minor ?? 0
  const net = summary?.net_minor ?? 0
  const count = summary?.transaction_count ?? 0
  const currency = summary?.currency ?? 'USD'

  const isNetPositive = net >= 0

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Total Income */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex items-center justify-between shadow-sm">
        <div>
          <p className="text-xs font-medium text-slate-400">Total Income</p>
          <p className="text-2xl font-bold tracking-tight text-white mt-1">
            {isLoading ? <span className="text-slate-600 animate-pulse">...</span> : formatMoney(income, currency)}
          </p>
          <span className="inline-block text-[11px] font-medium text-emerald-400 mt-1">
            Inflow credits
          </span>
        </div>
        <div className="h-11 w-11 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
          <TrendingUp className="w-5 h-5" />
        </div>
      </div>

      {/* Total Expenses */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex items-center justify-between shadow-sm">
        <div>
          <p className="text-xs font-medium text-slate-400">Total Expenses</p>
          <p className="text-2xl font-bold tracking-tight text-white mt-1">
            {isLoading ? <span className="text-slate-600 animate-pulse">...</span> : formatMoney(-expense, currency)}
          </p>
          <span className="inline-block text-[11px] font-medium text-rose-400 mt-1">
            Outflow spending
          </span>
        </div>
        <div className="h-11 w-11 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
          <TrendingDown className="w-5 h-5" />
        </div>
      </div>

      {/* Net Balance / Savings */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex items-center justify-between shadow-sm">
        <div>
          <p className="text-xs font-medium text-slate-400">Net Savings</p>
          <p className={`text-2xl font-bold tracking-tight mt-1 ${isNetPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
            {isLoading ? <span className="text-slate-600 animate-pulse">...</span> : formatMoney(net, currency)}
          </p>
          <span className="inline-block text-[11px] font-medium text-slate-400 mt-1">
            {isNetPositive ? 'Surplus balance' : 'Deficit balance'}
          </span>
        </div>
        <div className={`h-11 w-11 rounded-xl border flex items-center justify-center ${
          isNetPositive ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
        }`}>
          <Wallet className="w-5 h-5" />
        </div>
      </div>

      {/* Transaction Count */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex items-center justify-between shadow-sm">
        <div>
          <p className="text-xs font-medium text-slate-400">Transactions</p>
          <p className="text-2xl font-bold tracking-tight text-white mt-1">
            {isLoading ? <span className="text-slate-600 animate-pulse">...</span> : count}
          </p>
          <span className="inline-block text-[11px] font-medium text-indigo-400 mt-1">
            Normalized records
          </span>
        </div>
        <div className="h-11 w-11 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
          <Hash className="w-5 h-5" />
        </div>
      </div>
    </div>
  )
}
