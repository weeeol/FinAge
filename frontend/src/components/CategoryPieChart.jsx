import React from 'react'
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from 'recharts'
import { PieChart as PieIcon } from 'lucide-react'
import { formatMoney } from '../lib/api'

// FinAge harmonious editorial palette
const FINAGE_PALETTE = [
  '#1f2724', // ink
  '#15803d', // forest/sage
  '#c2410c', // terracotta/coral
  '#b45309', // gold/amber
  '#334155', // slate
  '#0f766e', // teal
  '#4338ca', // indigo
  '#78716c', // warm stone
]

export default function CategoryPieChart({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-[#e0e5de] bg-white p-6 flex flex-col items-center justify-center min-h-[340px] text-center">
        <div className="h-12 w-12 rounded-xl bg-[#f5f6f2] flex items-center justify-center text-[#78827c] mb-3">
          <PieIcon className="w-6 h-6" />
        </div>
        <p className="font-serif text-base font-medium text-[#1f2724]">No Spending Breakdown</p>
        <p className="text-xs text-[#78827c] max-w-sm mt-1">
          Upload statements to view categorical expense distribution.
        </p>
      </div>
    )
  }

  const chartData = data.slice(0, 6).map((item, idx) => ({
    name: item.category,
    value: item.amount_minor / 100,
    share: (item.share * 100).toFixed(1),
    color: FINAGE_PALETTE[idx % FINAGE_PALETTE.length],
  }))

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const entry = payload[0].payload
      return (
        <div className="rounded-lg border border-[#e0e5de] bg-white p-2.5 shadow-md text-xs space-y-1">
          <p className="font-serif font-bold text-[#1f2724]">{entry.name}</p>
          <p className="text-[#78827c]">
            {formatMoney(entry.value * 100)}{' '}
            <span className="font-medium text-[#1f2724]">({entry.share}%)</span>
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="rounded-xl border border-[#e0e5de] bg-white p-6 shadow-xs flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h2 className="font-serif text-xl font-normal text-[#1f2724]">Expense Allocation</h2>
          <p className="text-xs text-[#78827c] mt-0.5">Top spending categories by proportion</p>
        </div>
      </div>

      <div className="flex flex-col items-center gap-4">
        {/* Donut Chart */}
        <div className="h-48 w-48 shrink-0 relative flex items-center justify-center mt-2">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                innerRadius={50}
                outerRadius={75}
                paddingAngle={3}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} stroke="#fff" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend List */}
        <div className="w-full space-y-2 mt-2">
          {chartData.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between text-xs py-1 border-b border-[#f0f2ee] last:border-none">
              <div className="flex items-center gap-2 truncate">
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                <span className="text-[#1f2724] truncate font-medium">{item.name}</span>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="font-semibold text-[#1f2724]">{formatMoney(item.value * 100)}</span>
                <span className="text-[#78827c] w-10 text-right">{item.share}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
