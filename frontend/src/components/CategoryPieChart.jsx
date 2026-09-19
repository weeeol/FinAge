import React from 'react'
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from 'recharts'
import { PieChart as PieIcon } from 'lucide-react'

const PALETTE = [
  '#6366f1', // indigo
  '#ec4899', // pink
  '#f59e0b', // amber
  '#10b981', // emerald
  '#3b82f6', // blue
  '#8b5cf6', // purple
  '#14b8a6', // teal
  '#f97316', // orange
  '#64748b', // slate
]

export default function CategoryPieChart({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 flex flex-col items-center justify-center min-h-[320px] text-center">
        <PieIcon className="w-10 h-10 text-slate-600 mb-2" />
        <p className="text-sm font-medium text-slate-300">No Category Data</p>
        <p className="text-xs text-slate-500 max-w-sm mt-1">
          Upload statements to view categorical spending breakdown.
        </p>
      </div>
    )
  }

  const chartData = data.slice(0, 6).map((item, idx) => ({
    name: item.category,
    value: item.amount_minor / 100,
    share: (item.share * 100).toFixed(1),
    color: PALETTE[idx % PALETTE.length],
  }))

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const entry = payload[0].payload
      return (
        <div className="rounded-lg border border-slate-700 bg-slate-900 p-2.5 shadow-xl text-xs space-y-1">
          <p className="font-semibold text-white">{entry.name}</p>
          <p className="text-slate-300">
            ${entry.value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
            <span className="text-indigo-400">({entry.share}%)</span>
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 backdrop-blur flex flex-col shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h2 className="text-base font-semibold text-white">Expense Distribution</h2>
          <p className="text-xs text-slate-400">Top spending categories by share</p>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center gap-4">
        {/* Donut Chart */}
        <div className="h-56 w-56 shrink-0 relative flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                innerRadius={55}
                outerRadius={80}
                paddingAngle={3}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend List */}
        <div className="flex-1 w-full space-y-2">
          {chartData.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between text-xs py-1 border-b border-slate-800/60 last:border-none">
              <div className="flex items-center gap-2 truncate">
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                <span className="text-slate-300 truncate font-medium">{item.name}</span>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="font-semibold text-white">${item.value.toFixed(0)}</span>
                <span className="text-slate-500 w-10 text-right">{item.share}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
