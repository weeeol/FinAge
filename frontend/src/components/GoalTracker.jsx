import React, { useState, useEffect } from 'react'
import { Plus, AlertCircle, RefreshCw } from 'lucide-react'
import { fetchGoals, createGoal, formatMoney } from '../lib/api'

export default function GoalTracker() {
  const [goals, setGoals] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isCreating, setIsCreating] = useState(false)
  const [showForm, setShowForm] = useState(false)
  
  const [newName, setNewName] = useState('')
  const [newTarget, setNewTarget] = useState('')
  const [newCurrent, setNewCurrent] = useState('0')
  const [newDate, setNewDate] = useState('')
  const [formError, setFormError] = useState(null)

  const loadGoals = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await fetchGoals()
      setGoals(data.items || [])
    } catch (err) {
      setError(err.message || 'Failed to load goals.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadGoals()
  }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setFormError(null)
    
    if (!newName.trim()) {
      setFormError('Goal name is required.')
      return
    }
    if (!newTarget || isNaN(newTarget) || Number(newTarget) <= 0) {
      setFormError('Please enter a valid target amount.')
      return
    }
    if (isNaN(newCurrent) || Number(newCurrent) < 0) {
      setFormError('Current saved amount must be zero or greater.')
      return
    }

    setIsCreating(true)
    try {
      await createGoal({
        name: newName.trim(),
        target_minor: Math.round(Number(newTarget) * 100),
        current_minor: Math.round(Number(newCurrent) * 100),
        target_date: newDate || null,
        currency: 'USD'
      })
      
      setNewName('')
      setNewTarget('')
      setNewCurrent('0')
      setNewDate('')
      setShowForm(false)
      loadGoals()
    } catch (err) {
      setFormError(err.message || 'Failed to create goal.')
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className="panel obligations">
      <div className="panel-header mb-2">
        <div>
          <h2>Financial Goals</h2>
          <p className="muted">Track your savings and targets</p>
        </div>
        <button className="icon-button" onClick={loadGoals} title="Refresh Goals">
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
        </button>
      </div>
      
      <p className="text-[9px] text-[#9aa49e] uppercase tracking-wide font-bold mb-4">
        Decision support indicator. Not investment or financial product advice.
      </p>

      {error && (
        <div className="rounded-xl border border-[#f5d5cc] bg-[#fdf2ef] p-3 text-[#c2410c] text-xs flex items-center gap-2 mb-4">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="category-list">
        {goals.length === 0 && !isLoading && !error && (
          <div className="py-8 flex flex-col items-center justify-center text-center">
            <p className="text-xs text-[#78827c]">No goals set yet.</p>
          </div>
        )}
        
        {goals.map((g) => (
          <div key={g.id} className="category-row">
            <div className="category-meta">
              <span><b>{g.name}</b></span>
              <span>{formatMoney(g.current_minor)} / {formatMoney(g.target_minor)}</span>
            </div>
            <div className="h-2 w-full rounded-full bg-[#e5e9e2] overflow-hidden my-2">
              <div className="h-full rounded-full bg-[#58725b]" style={{ width: `${Math.min(g.progress * 100, 100)}%` }}></div>
            </div>
            <div className="text-[10px] text-[#9aa49e] mt-1 flex justify-between">
              <span>{Math.round(g.progress * 100)}% completed</span>
              {g.progress >= 1 ? (
                <span className="text-[#15803d] font-semibold">Goal Reached!</span>
              ) : (
                <span>
                  {formatMoney(Math.max(g.target_minor - g.current_minor, 0))} left
                  {g.target_date && ` by ${g.target_date}`}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {!showForm ? (
        <button 
          onClick={() => setShowForm(true)}
          className="w-full py-2 border border-dashed border-[#c3c9c3] rounded-lg text-xs font-semibold text-[#526057] hover:bg-[#eef1ed] hover:border-[#a2aba4] transition flex items-center justify-center gap-2"
        >
          <Plus className="w-3 h-3" /> Add Goal
        </button>
      ) : (
        <form onSubmit={handleCreate} className="bg-[#f8faf4] p-3 rounded-lg border border-[#e0e5de]">
          <h3 className="text-xs font-semibold mb-3">Create New Goal</h3>
          
          {formError && (
            <div className="mb-3 p-2 bg-[#fdf2ef] text-[#c2410c] text-[10px] rounded border border-[#f5d5cc]">
              {formError}
            </div>
          )}

          <div className="grid grid-cols-1 gap-3 mb-3">
            <div>
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Goal Name</label>
              <input 
                type="text" 
                placeholder="e.g. Emergency Fund"
                value={newName}
                onChange={e => setNewName(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Target ($)</label>
              <input 
                type="number" 
                min="1"
                step="1"
                placeholder="e.g. 5000"
                value={newTarget}
                onChange={e => setNewTarget(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white"
                required
              />
            </div>
            <div>
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Saved ($)</label>
              <input 
                type="number" 
                min="0"
                step="1"
                placeholder="e.g. 1000"
                value={newCurrent}
                onChange={e => setNewCurrent(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white"
              />
            </div>
            <div className="col-span-2">
              <label className="block text-[10px] uppercase font-bold text-[#9aa49e] mb-1">Target Date (Optional)</label>
              <input 
                type="date" 
                value={newDate}
                onChange={e => setNewDate(e.target.value)}
                className="w-full text-xs p-1.5 border border-[#c3c9c3] rounded bg-white text-[#526057]"
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
              className="primary-button !py-1.5 !px-3 disabled:opacity-50"
            >
              {isCreating ? 'Saving...' : 'Save Goal'}
            </button>
          </div>
        </form>
      )}
    </div>
  )
}
