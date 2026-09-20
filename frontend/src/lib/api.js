/**
 * API client and utilities for FinAge
 */

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

function apiUrl(path) {
  return `${API_BASE_URL}${path}`
}

export function formatMoney(minorUnits = 0, currency = 'USD') {
  const isNegative = minorUnits < 0
  const abs = Math.abs(minorUnits) / 100
  const formatted = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency || 'USD',
  }).format(abs)

  return isNegative ? `-${formatted}` : formatted
}

async function request(url, options = {}) {
  const res = await fetch(apiUrl(url), options)
  const data = await res.json().catch(() => ({}))

  if (!res.ok) {
    const errorMsg = data?.error?.message || `Request failed with status ${res.status}`
    const error = new Error(errorMsg)
    error.status = res.status
    error.details = data?.error?.details
    throw error
  }

  return data
}

export async function fetchSummary(fromDate = null, toDate = null) {
  const params = new URLSearchParams()
  if (fromDate) params.append('from_date', fromDate)
  if (toDate) params.append('to_date', toDate)
  const qs = params.toString() ? `?${params.toString()}` : ''
  return request(`/api/transactions/summary${qs}`)
}

export async function fetchTransactions({ page = 1, pageSize = 20, category = null, fromDate = null, toDate = null } = {}) {
  const params = new URLSearchParams({ page, page_size: pageSize })
  if (category) params.append('category', category)
  if (fromDate) params.append('from_date', fromDate)
  if (toDate) params.append('to_date', toDate)
  return request(`/api/transactions?${params.toString()}`)
}

export async function fetchMonthlyAnalytics(months = 6) {
  return request(`/api/analytics/monthly?months=${months}`)
}

export async function fetchCategoryAnalytics(month = null) {
  const qs = month ? `?month=${month}` : ''
  return request(`/api/analytics/categories${qs}`)
}

export async function fetchRecurringAnalytics() {
  return request('/api/analytics/recurring')
}

export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(apiUrl('/api/upload'), {
    method: 'POST',
    body: formData,
  })

  const data = await res.json().catch(() => ({}))

  if (!res.ok) {
    const errorMsg = data?.error?.message || `Upload failed with status ${res.status}`
    const error = new Error(errorMsg)
    error.status = res.status
    error.details = data?.error?.details
    throw error
  }

  return data
}

export async function askFinAge(question, fromDate = null, toDate = null) {
  return request('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question,
      from_date: fromDate,
      to_date: toDate,
    }),
  })
}

export async function fetchBudgets(month = null) {
  const qs = month ? `?month=${month}` : ''
  return request(`/api/analytics/budgets${qs}`)
}

export async function createBudget(budgetData) {
  return request('/api/budgets', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(budgetData),
  })
}

export async function deleteBudget(budgetId) {
  return request(`/api/budgets/${budgetId}`, {
    method: 'DELETE',
  })
}

export async function fetchGoals() {
  return request('/api/goals')
}

export async function createGoal(goalData) {
  return request('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(goalData),
  })
}

export async function deleteGoal(goalId) {
  return request(`/api/goals/${goalId}`, {
    method: 'DELETE',
  })
}

export async function fetchMonthlySummary(month) {
  const qs = month ? `?month=${month}` : ''
  return request(`/api/monthly-summary${qs}`)
}

export async function resetDatabase() {
  return request('/api/reset-database', {
    method: 'POST',
  })
}
