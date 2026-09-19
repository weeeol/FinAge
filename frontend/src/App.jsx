import React, { useState, useEffect, useCallback } from 'react'
import { AlertCircle, ShieldAlert } from 'lucide-react'

import Header from './components/Header'
import SummaryCards from './components/SummaryCards'
import MonthlyChart from './components/MonthlyChart'
import CategoryPieChart from './components/CategoryPieChart'
import RecurringList from './components/RecurringList'
import TransactionTable from './components/TransactionTable'
import UploadModal from './components/UploadModal'
import AssistantPanel from './components/AssistantPanel'

import BudgetTracker from './components/BudgetTracker'
import GoalTracker from './components/GoalTracker'

import {
  fetchSummary,
  fetchMonthlyAnalytics,
  fetchCategoryAnalytics,
  fetchRecurringAnalytics,
  fetchTransactions,
} from './lib/api'

export default function App() {
  const [summary, setSummary] = useState(null)
  const [monthlyData, setMonthlyData] = useState([])
  const [categoryData, setCategoryData] = useState([])
  const [recurringData, setRecurringData] = useState([])
  const [transactions, setTransactions] = useState([])
  const [totalTransactions, setTotalTransactions] = useState(0)
  const [page, setPage] = useState(1)

  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [error, setError] = useState(null)
  const [uploadModalOpen, setUploadModalOpen] = useState(false)

  const loadDashboardData = useCallback(async (showRefreshing = false) => {
    if (showRefreshing) {
      setIsRefreshing(true)
    } else {
      setIsLoading(true)
    }
    setError(null)

    try {
      const [
        summaryRes,
        monthlyRes,
        categoryRes,
        recurringRes,
        txnsRes,
      ] = await Promise.all([
        fetchSummary(),
        fetchMonthlyAnalytics(6),
        fetchCategoryAnalytics(),
        fetchRecurringAnalytics(),
        fetchTransactions({ page: 1, pageSize: 15 }),
      ])

      setSummary(summaryRes)
      setMonthlyData(monthlyRes.items || [])
      setCategoryData(categoryRes.items || [])
      setRecurringData(recurringRes.items || [])
      setTransactions(txnsRes.items || [])
      setTotalTransactions(txnsRes.total || 0)
      setPage(1)
    } catch (err) {
      setError(err.message || 'Failed to load financial analytics from FinAge backend.')
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }, [])

  const handlePageChange = async (newPage) => {
    try {
      const txnsRes = await fetchTransactions({ page: newPage, pageSize: 15 })
      setTransactions(txnsRes.items || [])
      setTotalTransactions(txnsRes.total || 0)
      setPage(newPage)
    } catch (err) {
      console.error('Failed to paginate transactions:', err)
    }
  }

  useEffect(() => {
    loadDashboardData()
  }, [loadDashboardData])

  return (
    <div className="min-h-screen bg-[#faf9f5] text-[#1f2724] flex flex-col antialiased">
      {/* Top Header */}
      <Header
        onOpenUpload={() => setUploadModalOpen(true)}
        onRefresh={() => loadDashboardData(true)}
        isRefreshing={isRefreshing}
      />

      {/* Main Workspace Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 flex flex-col gap-6">
        {/* Workspace Intro / Notice Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#e0e5de] pb-4">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-[#78827c]">
              Personal Finance Decision Support
            </p>
            <h1 className="font-serif text-2xl sm:text-3xl font-normal text-[#1f2724] tracking-tight mt-0.5">
              Financial Overview & Performance
            </h1>
          </div>
          <div className="flex items-center gap-2 text-xs text-[#78827c] bg-[#f1f5ed] border border-[#dfe9db] rounded-lg px-3 py-1.5 self-start sm:self-auto">
            <span className="h-2 w-2 rounded-full bg-[#15803d]" />
            <span>Deterministic backend calculations active</span>
          </div>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="rounded-xl border border-[#f5d5cc] bg-[#fdf2ef] p-4 text-[#c2410c] text-xs flex items-center justify-between gap-3 shadow-xs">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-[#c2410c] shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => loadDashboardData(true)}
              className="px-3 py-1.5 rounded-lg bg-[#f9e2db] hover:bg-[#f5d5cc] font-semibold transition"
            >
              Retry
            </button>
          </div>
        )}

        {/* Top Metric Snapshot Cards */}
        <SummaryCards summary={summary} isLoading={isLoading} />

        {/* Row 1: Cash Flow BarChart & Expense Allocation Donut */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <MonthlyChart data={monthlyData} />
          </div>
          <div className="lg:col-span-1">
            <CategoryPieChart data={categoryData} />
          </div>
        </div>

        {/* Row 2: Recurring Obligations, Budgets, Goals & Transaction Ledger */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 flex flex-col gap-6">
            <RecurringList data={recurringData} />
            <BudgetTracker />
            <GoalTracker />
          </div>
          <div className="lg:col-span-2">
            <TransactionTable
              transactions={transactions}
              total={totalTransactions}
              page={page}
              pageSize={15}
              onPageChange={handlePageChange}
              isLoading={isLoading}
            />
          </div>
        </div>

        <AssistantPanel />
      </main>

      {/* Statement Upload Modal */}
      <UploadModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onUploadSuccess={() => loadDashboardData(true)}
      />
    </div>
  )
}
