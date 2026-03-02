import React, { useState } from 'react'
import {
  FileText,
  TrendingUp,
  AlertTriangle,
  MessageSquare,
  Download,
  Search,
  ChevronRight,
  BarChart3,
  Zap,
  Target,
  Clock,
  CheckCircle
} from 'lucide-react'

const TICKERS = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META']

export default function App() {
  const [ticker, setTicker] = useState('AAPL')
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState(null)
  const [sentiment, setSentiment] = useState(null)
  const [activeTab, setActiveTab] = useState('summary')

  const handleFetch = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/fetch/${ticker}`)
      const data = await response.json()
      setSentiment(data.sentiment)
    } catch (error) {
      console.error('Fetch error:', error)
    }
    setLoading(false)
  }

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/generate/${ticker}`)
      const data = await response.json()
      setReport(data)
    } catch (error) {
      console.error('Generate error:', error)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 sidebar text-white p-6">
        <div className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg">Earnings</h1>
              <p className="text-xs text-gray-400">Copilot</p>
            </div>
          </div>
        </div>

        <nav className="space-y-2">
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg bg-white/10 text-white">
            <BarChart3 className="w-5 h-5" />
            Dashboard
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <FileText className="w-5 h-5" />
            Reports
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <Clock className="w-5 h-5" />
            History
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:bg-white/5">
            <Target className="w-5 h-5" />
            Settings
          </a>
        </nav>

        <div className="absolute bottom-6 left-6 right-6">
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-xs text-gray-400 mb-2">API Status</p>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span className="text-sm">Connected</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        {/* Header */}
        <header className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Earnings Call Prep</h1>
            <p className="text-gray-500">AI-powered analysis for your next quarterly call</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <select
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                className="pl-10 pr-4 py-2 border rounded-lg bg-white min-w-[200px]"
              >
                {TICKERS.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <button
              onClick={handleFetch}
              disabled={loading}
              className="btn-secondary"
            >
              Fetch Filings
            </button>
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Generating...' : 'Generate Report'}
            </button>
          </div>
        </header>

        {/* Stats Cards */}
        {sentiment && (
          <div className="grid grid-cols-4 gap-6 mb-8">
            <div className="stat-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Sentiment</p>
                  <p className="text-2xl font-bold text-gray-800">{sentiment.sentiment}</p>
                </div>
                <div className="icon blue">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
            <div className="stat-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Positive Words</p>
                  <p className="text-2xl font-bold text-green-600">{sentiment.positive_count}</p>
                </div>
                <div className="icon green">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
            <div className="stat-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Negative Words</p>
                  <p className="text-2xl font-bold text-red-600">{sentiment.negative_count}</p>
                </div>
                <div className="icon orange">
                  <AlertTriangle className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
            <div className="stat-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Ticker</p>
                  <p className="text-2xl font-bold text-gray-800">{ticker}</p>
                </div>
                <div className="icon purple">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Report Content */}
        {report ? (
          <div className="grid grid-cols-3 gap-6">
            {/* Main Report Area */}
            <div className="col-span-2 space-y-6">
              {/* Tabs */}
              <div className="flex gap-2 border-b">
                {['summary', 'questions', 'contradictions'].map(tab => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-4 py-2 font-medium capitalize ${
                      activeTab === tab
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500'
                    }`}
                  >
                    {tab.replace('_', ' ')}
                  </button>
                ))}
              </div>

              {/* Executive Summary */}
              {activeTab === 'summary' && (
                <div className="report-section fade-in">
                  <h3>
                    <FileText className="inline w-5 h-5 mr-2" />
                    Executive Summary
                  </h3>
                  <div className="prose max-w-none">
                    {report.summary?.split('\n').map((p, i) => (
                      <p key={i} className="mb-4 text-gray-700">{p}</p>
                    ))}
                  </div>
                </div>
              )}

              {/* Analyst Questions */}
              {activeTab === 'questions' && (
                <div className="report-section fade-in">
                  <h3>
                    <MessageSquare className="inline w-5 h-5 mr-2" />
                    Anticipated Analyst Questions
                  </h3>
                  <div className="space-y-4">
                    {report.questions?.split('\n\n').map((q, i) => (
                      <div key={i} className="bg-gray-50 rounded-lg p-4">
                        <p className="text-gray-800">{q}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Contradictions */}
              {activeTab === 'contradictions' && (
                <div className="report-section fade-in">
                  <h3>
                    <AlertTriangle className="inline w-5 h-5 mr-2" />
                    Potential Contradictions
                  </h3>
                  <div className="prose max-w-none">
                    {report.contradictions?.split('\n').map((p, i) => (
                      <p key={i} className="mb-4 text-gray-700">{p}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              <div className="report-section">
                <h3>Quick Actions</h3>
                <div className="space-y-3">
                  <button className="w-full btn-secondary flex items-center justify-between">
                    <span>Download PDF</span>
                    <Download className="w-4 h-4" />
                  </button>
                  <button className="w-full btn-secondary flex items-center justify-between">
                    <span>Export to Doc</span>
                    <FileText className="w-4 h-4" />
                  </button>
                  <button className="w-full btn-secondary flex items-center justify-between">
                    <span>Share Report</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="report-section">
                <h3>Report Info</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Generated</span>
                    <span className="font-medium">Just now</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Ticker</span>
                    <span className="font-medium">{ticker}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Filing Type</span>
                    <span className="font-medium">10-K</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Transcripts</span>
                    <span className="font-medium">4 quarters</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Empty State */
          <div className="card p-12 text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
              <FileText className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">No Report Generated</h3>
            <p className="text-gray-500 mb-6">
              Select a ticker and click "Generate Report" to create an earnings call prep document.
            </p>
            <button onClick={handleGenerate} className="btn-primary">
              Generate Your First Report
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
