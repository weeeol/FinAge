import { useEffect, useState } from 'react'
import {
  ArrowUpRight,
  BarChart3,
  CalendarDays,
  ChevronDown,
  CircleHelp,
  FileUp,
  LayoutDashboard,
  ListFilter,
  MessageCircle,
  MoreHorizontal,
  PiggyBank,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  WalletCards,
} from 'lucide-react'

export default function App() {
  const [healthStatus, setHealthStatus] = useState('checking')

  useEffect(() => {
    fetch('/health')
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'ok') {
          setHealthStatus('connected')
        } else {
          setHealthStatus('error')
        }
      })
      .catch(() => {
        setHealthStatus('disconnected')
      })
  }, [])

  const bars = [34, 48, 42, 66, 57, 75, 63, 82, 69, 88, 76, 92]
  const categories = [
    { name: 'Housing', amount: '$1,240', width: '82%', color: 'bg-ink' },
    { name: 'Food & dining', amount: '$486', width: '48%', color: 'bg-coral' },
    { name: 'Transport', amount: '$218', width: '28%', color: 'bg-sage' },
    { name: 'Subscriptions', amount: '$96', width: '15%', color: 'bg-gold' },
  ]

  return (
    <div className="app-shell min-h-screen text-ink">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">F</span><span>finpilot</span></div>
        <p className="sidebar-label">Workspace</p>
        <nav className="space-y-1">
          <a className="nav-item active" href="#overview"><LayoutDashboard size={17} /> Overview</a>
          <a className="nav-item" href="#transactions"><ListFilter size={17} /> Transactions <span className="nav-count">24</span></a>
          <a className="nav-item" href="#goals"><PiggyBank size={17} /> Budgets & goals</a>
          <a className="nav-item" href="#assistant"><MessageCircle size={17} /> Ask FinPilot</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="integrity-note"><ShieldCheck size={16} /><span>Private by design<br /><small>Your data stays local</small></span></div>
          <a className="nav-item" href="#help"><CircleHelp size={17} /> Help center</a>
          <div className="profile"><span className="avatar">JD</span><span><b>Jordan Davis</b><small>Personal workspace</small></span><MoreHorizontal size={17} /></div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div><p className="eyebrow">Saturday, September 19, 2026</p><h1>Good morning, Jordan.</h1></div>
          <div className="top-actions"><span className={`connection ${healthStatus}`}><i /> {healthStatus === 'connected' ? 'Synced' : healthStatus === 'checking' ? 'Connecting' : 'Offline'}</span><button className="icon-button" title="Refresh data"><RefreshCw size={17} /></button><span className="avatar">JD</span></div>
        </header>

        <section className="notice-bar"><Sparkles size={17} /><span><b>Your September snapshot is ready.</b> You are spending 12% less than your three-month average.</span><button className="text-button">See insight <ArrowUpRight size={15} /></button></section>

        <div className="period-row"><div><h2>September overview</h2><p className="muted">Month to date · Updated just now</p></div><button className="period-button"><CalendarDays size={16} /> Sep 1 – Sep 19 <ChevronDown size={15} /></button></div>

        <section className="snapshot-grid">
          <article className="hero-stat"><div className="stat-heading"><span>Available to spend</span><span className="tag tag-green">On track</span></div><strong>$2,840.50</strong><p><span className="positive">+$420.00</span> from last month</p><div className="progress-line"><span style={{ width: '71%' }} /></div><div className="stat-foot"><span>Monthly income <b>$5,000</b></span><span>Spent <b>$2,159.50</b></span></div></article>
          <article className="stat-card"><div className="stat-heading"><span>Income</span><WalletCards size={18} /></div><strong>$5,000.00</strong><p className="positive">↑ 4.2% <span className="muted">vs. August</span></p><div className="mini-bars">{bars.slice(0, 8).map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}</div></article>
          <article className="stat-card"><div className="stat-heading"><span>Expenses</span><BarChart3 size={18} /></div><strong>$2,159.50</strong><p className="negative">↓ 12.0% <span className="muted">vs. August</span></p><div className="mini-bars coral">{bars.slice(4).map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}</div></article>
        </section>

        <section className="content-grid">
          <article className="panel spending-panel"><div className="panel-header"><div><h3>Spending trend</h3><p className="muted">Your daily spending this month</p></div><button className="dots-button" title="More options"><MoreHorizontal size={18} /></button></div><div className="chart-area"><div className="chart-labels"><span>$500</span><span>$250</span><span>$0</span></div><div className="chart"><div className="chart-grid"><i /><i /><i /></div><div className="chart-bars">{bars.map((height, index) => <i key={index} className={index === 10 ? 'today' : ''} style={{ height: `${height}%` }} />)}</div></div><div className="chart-x"><span>Sep 1</span><span>Sep 7</span><span>Sep 14</span><span>Today</span></div></div><div className="chart-legend"><span><i className="legend-ink" /> Daily spend</span><span><i className="legend-coral" /> 3-month average</span></div></article>
          <article className="panel"><div className="panel-header"><div><h3>Where your money goes</h3><p className="muted">Top categories this month</p></div><button className="dots-button" title="More options"><MoreHorizontal size={18} /></button></div><div className="category-list">{categories.map((category) => <div className="category-row" key={category.name}><div className="category-meta"><span>{category.name}</span><b>{category.amount}</b></div><div className="category-track"><span className={category.color} style={{ width: category.width }} /></div></div>)}</div><button className="view-link">View all transactions <ArrowUpRight size={15} /></button></article>
        </section>

        <section className="bottom-grid"><article className="panel obligations"><div className="panel-header"><div><h3>Coming up</h3><p className="muted">Recurring payments in the next 14 days</p></div><span className="amount-muted">$184.97</span></div><div className="obligation-row"><span className="merchant-icon coral-icon">N</span><span><b>Netflix</b><small>Entertainment · Sep 22</small></span><strong>$22.99</strong></div><div className="obligation-row"><span className="merchant-icon sage-icon">S</span><span><b>Spotify</b><small>Entertainment · Sep 26</small></span><strong>$11.99</strong></div><div className="obligation-row"><span className="merchant-icon gold-icon">◎</span><span><b>Rent</b><small>Housing · Oct 1</small></span><strong>$1,150.00</strong></div></article><article className="panel import-panel"><div className="import-icon"><FileUp size={22} /></div><h3>Bring in your latest statement</h3><p className="muted">CSV, XLSX, or text-based PDF. We’ll sort the rest.</p><button className="primary-button">Upload statement <ArrowUpRight size={16} /></button><p className="tiny-note"><ShieldCheck size={13} /> Your files are processed locally</p></article></section>
      </main>
    </div>
  )
}
