import React, { useState, useEffect } from 'react'
import { Plus, AlertCircle, RefreshCw } from 'lucide-react'
import { fetchBudgets, createBudget, deleteBudget, formatMoney } from '../lib/api'

export default function BudgetTracker() {
  const [budgets, setBudgets] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isCreating, setIsCreating] = useState(false)
  const [showForm, setShowForm] = useState(false)
  
  const [newCategory, setNewCategory] = useState('Groceries')
  const [newLimit, setNewLimit] = useState('')
  const [formError, setFormError] = useState(null)

  const [selectedMonth, setSelectedMonth] = useState('2026-01')

  const loadBudgets = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await fetchBudgets(selectedMonth)
      setBudgets(data.items || [])
    } catch (err) {
      setError(err.message || 'Failed to load budgets.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadBudgets()
  }, [selectedMonth])

  const handleCreate = async (e) => {
    e.preventDefault()
    setFormError(null)
    
    if (!newLimit || isNaN(newLimit) || Number(newLimit) <= 0) {
      setFormError('Please enter a valid limit amount.')
      return
    }

    setIsCreating(true)
    try {
      await createBudget({
        category: newCategory,
        month: selectedMonth,
        limit_minor: Math.round(Number(newLimit) * 100),
        currency: 'USD'
      })
      
      setNewLimit('')
      setShowForm(false)
      await loadBudgets()
    } catch (err) {
      if (err.details?.code === 'duplicate_budget' || err.message.includes('already exists')) {
        setFormError(`A budget for ${newCategory} already exists this month.`)
      } else {
        setFormError(err.message || 'Failed to create budget.')
      }
    } finally {
      setIsCreating(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'on_track': return 'bg-[#58725b]'
      case 'warning': return 'bg-[#c89234]'
      case 'exceeded': return 'bg-[#c05346]'
      default: return 'bg-[#58725b]'
    }
  }

  return (
    <div className="panel budget-goal-card obligations bg-white border border-[#e0e5de] rounded-xl shadow-sm">
      <div className="panel-header">
        <div>
          <h2>Monthly Budgets</h2>
          <p className="muted">Track spending limits for key categories</p>
        </div>
        <div className="flex items-center gap-3">
          <input 
            type="month" 
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className="text-xs p-1 border border-[#c3c9c3] rounded bg-white text-[#526057]"
          />
          <button className="icon-button" onClick={loadBudgets} title="Refresh Budgets">
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-[#f5d5cc] bg-[#fdf2ef] p-3 text-[#c2410c] text-xs flex items-center gap-2 mb-4">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="category-list">
        {budgets.length === 0 && !isLoading && !error && (
          <div className="py-8 flex flex-col items-center justify-center text-center">
            <p className="text-xs text-[#78827c]">No budgets set for this month.</p>
          </div>
        )}
        
        {budgets.map((b) => (
          <div key={b.budget_id} className="category-row">
            <div className="category-meta">
              <span><b>{b.category}</b></span>
              <span>{formatMoney(b.spent_minor)} / {formatMoney(b.limit_minor)}</span>
            </div>
            <div className="h-2 w-full rounded-full bg-[#e5e9e2] overflow-hidden my-2">
              <div className={`h-full rounded-full ${getStatusColor(b.status)}`} style={{ width: `${Math.min(b.percent_used * 100, 100)}%` }}></div>
            </div>
            <div className="text-[10px] text-[#9aa49e] mt-1 flex justify-between">
              <span>{Math.round(b.percent_used * 100)}% used</span>
              <span className={b.remaining_minor < 0 ? "text-[#c05346] font-semibold" : ""}>
                {b.remaining_minor >= 0 ? `${formatMoney(b.remaining_minor)} remaining` : `${formatMoney(Math.abs(b.remaining_minor))} over limit`}
              </span>
            </div>
            <div className="flex justify-end mt-2">
              <button
                type="button"
                onClick={async () => {
                  try {
                    await deleteBudget(b.budget_id)
                    await loadBudgets()
                  } catch (err) {
                    setError(err.message || 'Failed to remove budget.')
                  }
                }}
                className="px-2 py-1 text-[10px] font-semibold text-[#c2410c] hover:bg-[#fdf2ef] rounded border border-[#f5d5cc]"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      {!showForm ? (
        <button 
          onClick={() => setShowForm(true)}
          className="w-full py-2 border border-dashed border-[#c3c9c3] rounded-lg text-xs font-semibold text-[#526057] hover:bg-[#eef1ed] hover:border-[#a2aba4] transition flex items-center justify-center gap-2"
        >
          <Plus className="w-3 h-3" /> Add Budget
        </button>
      ) : (
        <form onSubmit={handleCreate} className="bg-[#f8faf4] p-3 rounded-lg border border-[#e0e5de]">
          <h3 className="text-xs font-semibold mb-3">Create New Budget</h3>
          
          {formError && (
            <div className="mb-3 p-2 bg-[#fdf2ef] text-[#c2410c] text-[10px] rounded border border-[#f5d5cc]">
              {formError}
            </div>
          )}

          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Category</label>
              <select 
                value={newCategory} 
                onChange={e => setNewCategory(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white"
              >
                <option value="Groceries">Groceries</option>
                <option value="Dining">Dining</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Shopping">Shopping</option>
                <option value="Utilities">Utilities</option>
                <option value="Transportation">Transportation</option>
                <option value="Housing">Housing</option>
                <option value="Travel">Travel</option>
              </select>
            </div>
            <div>
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Limit ($)</label>
              <input 
                type="number" 
                min="1"
                step="1"
                placeholder="e.g. 500"
                value={newLimit}
                onChange={e => setNewLimit(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white"
                required
              />
            </div>
          </div>
          
          <div className="flex justify-end gap-2">
            <button 
              type="button" 
              onClick={() => { setShowForm(false); setFormError(null) }}
              className="px-3 py-1.5 text-xs text-[#526057] hover:bg-[#eef1ed] rounded transition"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              disabled={isCreating}
              className="primary-button !py-1.5 !px-3 !text-black disabled:opacity-50"
            >
              {isCreating ? 'Saving...' : 'Save Budget'}
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
