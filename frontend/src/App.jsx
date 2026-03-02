import { useState } from 'react'
import {
  Rocket,
  Building2,
  FileText,
  MessageSquare,
  AlertTriangle,
  TrendingUp,
  Download,
  Loader2,
  CheckCircle,
  ChevronDown,
  ChevronRight
} from 'lucide-react'

const TICKERS = [
  { symbol: 'AAPL', name: 'Apple Inc.', cik: '0000320193' },
  { symbol: 'TSLA', name: 'Tesla Inc.', cik: '0001318605' },
  { symbol: 'NVDA', name: 'NVIDIA Corp.', cik: '0001045810' },
  { symbol: 'MSFT', name: 'Microsoft Corp.', cik: '0000789019' },
  { symbol: 'GOOGL', name: 'Alphabet Inc.', cik: '0001652044' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', cik: '0001018724' },
  { symbol: 'META', name: 'Meta Platforms Inc.', cik: '0001326801' },
]

function App() {
  const [selectedTicker, setSelectedTicker] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fetchingData, setFetchingData] = useState(false)
  const [dataFetched, setDataFetched] = useState(false)
  const [report, setReport] = useState(null)
  const [sentiment, setSentiment] = useState(null)
  const [expandedSections, setExpandedSections] = useState({
    summary: true,
    metrics: true,
    questions: true,
    risks: true,
    contradictions: true
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const handleFetchData = async () => {
    if (!selectedTicker) return

    setFetchingData(true)
    try {
      const response = await fetch('/api/fetch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: selectedTicker.symbol })
      })
      const data = await response.json()
      setSentiment(data.sentiment)
      setDataFetched(true)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setFetchingData(false)
    }
  }

  const handleGenerateReport = async () => {
    if (!dataFetched) return

    setLoading(true)
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: selectedTicker.symbol })
      })
      const data = await response.json()
      setReport(data.report)
    } catch (error) {
      console.error('Error generating report:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!report) return

    const markdown = `# Earnings Pilot Report: ${selectedTicker.symbol}

## Executive Summary
${report.summary}

## Key Metrics
- Sentiment: ${sentiment?.sentiment || 'N/A'}
- Positive Keywords: ${sentiment?.positive_count || 0}
- Negative Keywords: ${sentiment?.negative_count || 0}

## Anticipated Analyst Questions
${report.questions}

## Risk Factors
${report.risks || 'Not generated'}

## Contradictions
${report.contradictions}
`

    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedTicker.symbol}_earnings_report.md`
    a.click()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <Rocket className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Earnings Pilot</h1>
                <p className="text-xs text-gray-500">AI-Powered Earnings Call Prep</p>
              </div>
            </div>
            {report && (
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                Download Report
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-24">
              <h2 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
                Select Company
              </h2>

              <div className="space-y-2 mb-6">
                {TICKERS.map((ticker) => (
                  <button
                    key={ticker.symbol}
                    onClick={() => {
                      setSelectedTicker(ticker)
                      setDataFetched(false)
                      setReport(null)
                    }}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                      selectedTicker?.symbol === ticker.symbol
                        ? 'bg-primary-50 border-2 border-primary-500 text-primary-700'
                        : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="font-semibold">{ticker.symbol}</div>
                    <div className="text-xs text-gray-500">{ticker.name}</div>
                  </button>
                ))}
              </div>

              <div className="space-y-3">
                <button
                  onClick={handleFetchData}
                  disabled={!selectedTicker || fetchingData}
                  className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium transition-all ${
                    !selectedTicker || fetchingData
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-primary-600 text-white hover:bg-primary-700'
                  }`}
                >
                  {fetchingData ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Fetching...
                    </>
                  ) : (
                    <>
                      <FileText className="w-4 h-4" />
                      Fetch Filings
                    </>
                  )}
                </button>

                <button
                  onClick={handleGenerateReport}
                  disabled={!dataFetched || loading}
                  className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium transition-all ${
                    !dataFetched || loading
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-gray-900 text-white hover:bg-gray-800'
                  }`}
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Rocket className="w-4 h-4" />
                      Generate Report
                    </>
                  )}
                </button>
              </div>

              {/* Status */}
              {selectedTicker && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      {dataFetched ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <div className="w-4 h-4 rounded-full border-2 border-gray-300" />
                      )}
                      <span className={dataFetched ? 'text-green-700' : 'text-gray-500'}>
                        Data Fetched
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      {report ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <div className="w-4 h-4 rounded-full border-2 border-gray-300" />
                      )}
                      <span className={report ? 'text-green-700' : 'text-gray-500'}>
                        Report Generated
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {!selectedTicker ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <Building2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Select a Company to Begin
                </h3>
                <p className="text-gray-500">
                  Choose a ticker from the sidebar to fetch SEC filings and generate your earnings prep report.
                </p>
              </div>
            ) : !report ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                {loading ? (
                  <>
                    <Loader2 className="w-16 h-16 text-primary-500 mx-auto mb-4 animate-spin" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Generating Report...
                    </h3>
                    <p className="text-gray-500">
                      Analyzing 10-K and transcripts with Claude 3.5 Sonnet
                    </p>
                  </>
                ) : (
                  <>
                    <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {selectedTicker.name}
                    </h3>
                    <p className="text-gray-500 mb-4">
                      {dataFetched
                        ? 'Data fetched successfully. Click "Generate Report" to create your earnings prep.'
                        : 'Click "Fetch Filings" to pull 10-K and earnings transcripts from SEC EDGAR.'}
                    </p>
                    {sentiment && (
                      <div className="inline-flex items-center gap-4 px-6 py-3 bg-gray-50 rounded-lg">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-gray-900">{sentiment.positive_count}</div>
                          <div className="text-xs text-gray-500">Positive</div>
                        </div>
                        <div className="w-px h-8 bg-gray-300" />
                        <div className="text-center">
                          <div className="text-2xl font-bold text-gray-900">{sentiment.negative_count}</div>
                          <div className="text-xs text-gray-500">Negative</div>
                        </div>
                        <div className="w-px h-8 bg-gray-300" />
                        <div className="text-center">
                          <div className={`text-sm font-semibold ${
                            sentiment.sentiment === 'Positive' ? 'text-green-600' :
                            sentiment.sentiment === 'Negative' ? 'text-red-600' : 'text-gray-600'
                          }`}>
                            {sentiment.sentiment}
                          </div>
                          <div className="text-xs text-gray-500">Sentiment</div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            ) : (
              <div className="space-y-6">
                {/* Metrics Bar */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">{selectedTicker.symbol}</h2>
                      <p className="text-gray-500">{selectedTicker.name}</p>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-center px-4">
                        <div className={`text-lg font-semibold ${
                          sentiment?.sentiment === 'Positive' ? 'text-green-600' :
                          sentiment?.sentiment === 'Negative' ? 'text-red-600' : 'text-gray-600'
                        }`}>
                          {sentiment?.sentiment || 'N/A'}
                        </div>
                        <div className="text-xs text-gray-500">Tone</div>
                      </div>
                      <div className="text-center px-4 border-l border-gray-200">
                        <div className="text-lg font-semibold text-gray-900">10-K</div>
                        <div className="text-xs text-gray-500">Filing</div>
                      </div>
                      <div className="text-center px-4 border-l border-gray-200">
                        <div className="text-lg font-semibold text-gray-900">4 Qtrs</div>
                        <div className="text-xs text-gray-500">Transcripts</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Executive Summary */}
                <ReportSection
                  title="Executive Summary"
                  icon={<TrendingUp className="w-5 h-5" />}
                  expanded={expandedSections.summary}
                  onToggle={() => toggleSection('summary')}
                >
                  <div className="prose prose-sm max-w-none">
                    {report.summary}
                  </div>
                </ReportSection>

                {/* Analyst Questions */}
                <ReportSection
                  title="Anticipated Analyst Questions"
                  icon={<MessageSquare className="w-5 h-5" />}
                  expanded={expandedSections.questions}
                  onToggle={() => toggleSection('questions')}
                >
                  <div className="prose prose-sm max-w-none">
                    {report.questions}
                  </div>
                </ReportSection>

                {/* Risk Factors */}
                {report.risks && (
                  <ReportSection
                    title="Risk Factors"
                    icon={<AlertTriangle className="w-5 h-5" />}
                    expanded={expandedSections.risks}
                    onToggle={() => toggleSection('risks')}
                  >
                    <div className="prose prose-sm max-w-none">
                      {report.risks}
                    </div>
                  </ReportSection>
                )}

                {/* Contradictions */}
                <ReportSection
                  title="Potential Contradictions"
                  icon={<AlertTriangle className="w-5 h-5" />}
                  expanded={expandedSections.contradictions}
                  onToggle={() => toggleSection('contradictions')}
                >
                  <div className="prose prose-sm max-w-none">
                    {report.contradictions}
                  </div>
                </ReportSection>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

function ReportSection({ title, icon, children, expanded, onToggle }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="text-primary-600">{icon}</div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
        {expanded ? (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronRight className="w-5 h-5 text-gray-400" />
        )}
      </button>
      {expanded && (
        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
          {children}
        </div>
      )}
    </div>
  )
}

export default App
