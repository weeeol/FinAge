import React, { useState, useEffect, useCallback } from 'react'
import { AlertCircle, FileSpreadsheet, RefreshCw } from 'lucide-react'

import Header from './components/Header'
import SummaryCards from './components/SummaryCards'
import MonthlyChart from './components/MonthlyChart'
import CategoryPieChart from './components/CategoryPieChart'
import RecurringList from './components/RecurringList'
import TransactionTable from './components/TransactionTable'
import UploadModal from './components/UploadModal'

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
      setError(err.message || 'Failed to load financial analytics from backend.')
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
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
      {/* Top Header */}
      <Header
        onOpenUpload={() => setUploadModalOpen(true)}
        onRefresh={() => loadDashboardData(true)}
        isRefreshing={isRefreshing}
      />

      {/* Main Dashboard Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 flex flex-col gap-6">
        {/* Error Banner */}
        {error && (
          <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-rose-300 text-xs flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => loadDashboardData(true)}
              className="px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/30 font-medium transition"
            >
              Retry
            </button>
          </div>
        )}

        {/* Top Metric Cards */}
        <SummaryCards summary={summary} isLoading={isLoading} />

        {/* Row 1: Monthly Trend BarChart & Category Donut Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <MonthlyChart data={monthlyData} />
          </div>
          <div className="lg:col-span-1">
            <CategoryPieChart data={categoryData} />
          </div>
        </div>

        {/* Row 2: Recurring Payments List & Recent Transaction Ledger */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <RecurringList data={recurringData} />
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
