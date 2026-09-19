import React from 'react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts'
import { Calendar } from 'lucide-react'

export default function MonthlyChart({ data = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-[#e0e5de] bg-white p-6 flex flex-col items-center justify-center min-h-[340px] text-center">
        <div className="h-12 w-12 rounded-xl bg-[#f5f6f2] flex items-center justify-center text-[#78827c] mb-3">
          <Calendar className="w-6 h-6" />
        </div>
        <p className="font-serif text-base font-medium text-[#1f2724]">No Cash Flow Data</p>
        <p className="text-xs text-[#78827c] max-w-sm mt-1">
          Upload statements to visualize your monthly inflow vs. outflow history.
        </p>
      </div>
    )
  }

  const formattedData = data.map((d) => ({
    month: d.month,
    Inflows: d.income_minor / 100,
    Outflows: d.expense_minor / 100,
    Net: d.net_minor / 100,
  }))

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="rounded-lg border border-[#e0e5de] bg-white p-3 shadow-md text-xs space-y-1">
          <p className="font-serif font-bold text-[#1f2724] border-b border-[#f0f2ee] pb-1 mb-1">{label}</p>
          {payload.map((entry, index) => (
            <div key={`item-${index}`} className="flex items-center justify-between gap-4">
              <span className="flex items-center gap-1.5 text-[#78827c]">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
                {entry.name}:
              </span>
              <span className="font-semibold text-[#1f2724]">
                ${entry.value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="rounded-xl border border-[#e0e5de] bg-white p-6 shadow-xs flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="font-serif text-xl font-normal text-[#1f2724]">Cash Flow Overview</h2>
          <p className="text-xs text-[#78827c] mt-0.5">Monthly inflow vs. outflow progression</p>
        </div>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={formattedData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f2ee" vertical={false} />
            <XAxis dataKey="month" stroke="#78827c" fontSize={11} tickLine={false} />
            <YAxis
              stroke="#78827c"
              fontSize={11}
              tickLine={false}
              tickFormatter={(v) => `$${v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: 12, paddingTop: 12 }} />
            <Bar dataKey="Inflows" fill="#15803d" radius={[4, 4, 0, 0]} maxBarSize={36} />
            <Bar dataKey="Outflows" fill="#c2410c" radius={[4, 4, 0, 0]} maxBarSize={36} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
