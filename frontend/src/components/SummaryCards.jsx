import React from 'react'
import { TrendingUp, TrendingDown, Wallet, Hash } from 'lucide-react'
import { formatMoney } from '../lib/api'

export default function SummaryCards({ summary, isLoading }) {
  const income = summary?.income_minor ?? 0
  const expense = summary?.expense_minor ?? 0
  const net = summary?.net_minor ?? 0
  const count = summary?.transaction_count ?? 0
  const currency = summary?.currency ?? 'INR'

  const isNetPositive = net >= 0

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Hero Stat: Net Savings / Balance */}
      <div className="rounded-xl border border-[#e0e5de] bg-[#1f2724] text-[#f8faf4] p-5 shadow-sm flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-[#aebbb0] uppercase tracking-wider">Net Surplus</p>
          <div className="h-8 w-8 rounded-lg bg-[#29483d] flex items-center justify-center text-[#a4d0a7]">
            <Wallet className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3">
          <p className="font-serif text-3xl font-normal tracking-tight text-[#f8faf4]">
            {isLoading ? <span className="opacity-40 animate-pulse">...</span> : formatMoney(net, currency)}
          </p>
          <div className="flex items-center gap-2 mt-2">
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${
              isNetPositive ? 'bg-[#29483d] text-[#a4d0a7]' : 'bg-[#4d2d27] text-[#e89d8f]'
            }`}>
              {isNetPositive ? '+ Retained Cash' : '- Outflow Deficit'}
            </span>
          </div>
        </div>
      </div>

      {/* Inflow / Total Income */}
      <div className="rounded-xl border border-[#e0e5de] bg-white p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-[#78827c] uppercase tracking-wider">Total Inflow</p>
          <div className="h-8 w-8 rounded-lg bg-[#f1f7f4] border border-[#d6e8de] flex items-center justify-center text-[#2e7d32]">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3">
          <p className="font-serif text-3xl font-normal tracking-tight text-[#1f2724]">
            {isLoading ? <span className="text-[#a5ada7] animate-pulse">...</span> : formatMoney(income, currency)}
          </p>
          <p className="text-[11px] font-medium text-[#2e7d32] mt-2">
            Income & credits
          </p>
        </div>
      </div>

      {/* Outflow / Total Expenses */}
      <div className="rounded-xl border border-[#e0e5de] bg-white p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-[#78827c] uppercase tracking-wider">Total Outflow</p>
          <div className="h-8 w-8 rounded-lg bg-[#fdf2ef] border border-[#f5d5cc] flex items-center justify-center text-[#c2410c]">
            <TrendingDown className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3">
          <p className="font-serif text-3xl font-normal tracking-tight text-[#1f2724]">
            {isLoading ? <span className="text-[#a5ada7] animate-pulse">...</span> : formatMoney(-expense, currency)}
          </p>
          <p className="text-[11px] font-medium text-[#c2410c] mt-2">
            Expenses & bills
          </p>
        </div>
      </div>

      {/* Total Transactions */}
      <div className="rounded-xl border border-[#e0e5de] bg-white p-5 shadow-xs flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-[#78827c] uppercase tracking-wider">Transactions</p>
          <div className="h-8 w-8 rounded-lg bg-[#f7f5ed] border border-[#e8e2cf] flex items-center justify-center text-[#b45309]">
            <Hash className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3">
          <p className="font-serif text-3xl font-normal tracking-tight text-[#1f2724]">
            {isLoading ? <span className="text-[#a5ada7] animate-pulse">...</span> : count}
          </p>
          <p className="text-[11px] font-medium text-[#78827c] mt-2">
            Normalized ledger records
          </p>
        </div>
      </div>
    </div>
  )
}
