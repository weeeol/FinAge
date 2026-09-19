import React, { useState } from 'react'
import { ArrowUpRight, Bot, Loader2, Send, Sparkles } from 'lucide-react'
import { askFinAge, formatMoney } from '../lib/api'

const suggestions = [
  'Where did I spend the most?',
  'What recurring payments should I expect?',
  'How much did I spend this month?',
]

export default function AssistantPanel() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [sources, setSources] = useState([])
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const submitQuestion = async (event, suggestedQuestion = null) => {
    event?.preventDefault()
    const nextQuestion = (suggestedQuestion || question).trim()
    if (!nextQuestion || isLoading) return

    setQuestion(nextQuestion)
    setError(null)
    setAnswer(null)
    setSources([])
    setIsLoading(true)

    try {
      const response = await askFinAge(nextQuestion)
      setAnswer(response.answer)
      setSources(response.sources || [])
    } catch (err) {
      setError(err.message || 'FinAge could not answer that question.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="rounded-xl border border-[#e0e5de] bg-[#f1f5ed] p-6 shadow-xs">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-3">
          <div className="h-9 w-9 rounded-lg bg-[#1f2724] text-[#e8bb62] flex items-center justify-center shrink-0">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-serif text-xl font-normal text-[#1f2724]">Ask FinAge</h2>
              <Sparkles className="w-4 h-4 text-[#b28d43]" />
            </div>
            <p className="text-xs text-[#78827c] mt-0.5">Ask about stored spending facts. Answers never change your financial data.</p>
          </div>
        </div>
        <span className="text-[10px] font-semibold uppercase tracking-wider text-[#58725b] bg-white border border-[#dfe9db] rounded-full px-2.5 py-1">
          Grounded answers
        </span>
      </div>

      <form onSubmit={submitQuestion} className="mt-5 flex flex-col sm:flex-row gap-2">
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Try: where did I spend the most?"
          maxLength={1000}
          className="min-w-0 flex-1 rounded-lg border border-[#d6e0d5] bg-white px-3.5 py-2.5 text-xs text-[#1f2724] outline-none placeholder:text-[#a1aaa3] focus:border-[#7da18a] focus:ring-2 focus:ring-[#dfe9db]"
        />
        <button type="submit" disabled={!question.trim() || isLoading} className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#1f2724] px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-[#2d3834] disabled:cursor-not-allowed disabled:opacity-45">
          {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4 text-[#e8bb62]" />}
          Ask
        </button>
      </form>

      <div className="mt-3 flex flex-wrap gap-2">
        {suggestions.map((suggestion) => (
          <button key={suggestion} type="button" onClick={(event) => submitQuestion(event, suggestion)} className="rounded-full border border-[#d6e0d5] bg-white px-3 py-1.5 text-[11px] text-[#66746b] transition hover:border-[#9bb5a0] hover:text-[#1f2724]">
            {suggestion}
          </button>
        ))}
      </div>

      {(answer || error || isLoading) && (
        <div className="mt-5 rounded-lg border border-[#dfe9db] bg-white p-4">
          {isLoading && <p className="text-xs text-[#78827c]">Reviewing your structured financial data...</p>}
          {error && <p className="text-xs text-[#b45309]">{error}</p>}
          {answer && <><p className="text-sm leading-6 text-[#38453d]">{answer}</p>{sources.length > 0 && <div className="mt-4 flex flex-wrap gap-2">{sources.slice(0, 4).map((source, index) => <span key={`${source.label}-${index}`} className="inline-flex items-center gap-1 rounded-full bg-[#f5f6f2] px-2.5 py-1 text-[10px] text-[#66746b]"><span>{source.label}</span>{source.amount_minor !== null && source.amount_minor !== undefined && <b>{formatMoney(source.amount_minor)}</b>}<ArrowUpRight className="w-3 h-3" /></span>)}</div>}</>}
        </div>
      )}
    </section>
  )
}
