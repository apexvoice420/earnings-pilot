import React, { useState, useEffect } from 'react';
import {
    BarChart3,
    Search,
    RefreshCw,
    AlertTriangle,
    Download,
    Share2,
    ChevronRight,
    Plus,
    ArrowUpRight,
    TrendingUp,
    MessageSquare,
    FileSearch,
    CheckCircle2,
    Zap
} from 'lucide-react';
import StatCard from '../components/StatCard';
import ReportSection from '../components/ReportSection';
import Button from '../components/Button';

// Backend API URL - Railway backend
const API_URL = 'https://earnings-pilot-production.up.railway.app';

const Dashboard = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [ticker, setTicker] = useState('AAPL');
    const [hasReport, setHasReport] = useState(false);
    const [activeTab, setActiveTab] = useState('summary');
    const [reportData, setReportData] = useState(null);
    const [fetchData, setFetchData] = useState(null);

    const fetchFilings = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch(`${API_URL}/api/fetch/${ticker}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            setFetchData(data);
            return data;
        } catch (err) {
            setError(err.message);
            return null;
        } finally {
            setLoading(false);
        }
    };

    const generateReport = async () => {
        setLoading(true);
        setError(null);
        setHasReport(false);

        try {
            // First fetch the filings
            const filingData = await fetchFilings();
            if (!filingData) return;
            
            // Then generate the report
            const response = await fetch(`${API_URL}/api/generate/${ticker}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            setReportData(data);
            setHasReport(true);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const getSentimentColor = (sentiment) => {
        if (!sentiment) return 'text-gray-500';
        if (sentiment.toLowerCase() === 'positive') return 'text-green-600';
        if (sentiment.toLowerCase() === 'negative') return 'text-red-600';
        return 'text-yellow-600';
    };

    return (
        <div className="pt-24 pb-12 bg-background min-h-screen">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header Actions */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6 bg-white p-8 rounded-[32px] border border-gray-100 shadow-sm animate-fade-in-up">
                    <div className="space-y-1">
                        <h1 className="text-3xl font-headings text-primary tracking-tight">Intelligence Dashboard</h1>
                        <p className="text-gray-400 text-sm font-medium uppercase tracking-widest flex items-center">
                            <CheckCircle2 className="w-4 h-4 mr-2 text-green-500" />
                            System Ready · Real SEC Data
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
                        <div className="relative group flex-grow">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                            <input
                                type="text"
                                value={ticker}
                                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                                placeholder="Enter Ticker (e.g. MSFT)"
                                className="pl-11 pr-4 py-4 bg-gray-50 border border-transparent focus:bg-white focus:border-blue-500/30 rounded-2xl text-sm font-bold w-full outline-none transition-all"
                            />
                        </div>
                        <Button
                            onClick={generateReport}
                            className="py-4 px-8 min-w-[200px]"
                            disabled={loading || !ticker}
                            icon={loading ? RefreshCw : Plus}
                        >
                            {loading ? 'Analyzing...' : 'Generate Prep'}
                        </Button>
                    </div>
                </div>

                {loading ? (
                    <div className="py-32 flex flex-col items-center justify-center space-y-8 animate-pulse">
                        <div className="relative">
                            <div className="w-24 h-24 border-4 border-blue-100 border-t-blue-500 rounded-full animate-spin" />
                            <Zap className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-blue-500" />
                        </div>
                        <div className="text-center space-y-2">
                            <h3 className="text-xl font-bold text-primary">Scanning SEC Filings for {ticker}</h3>
                            <p className="text-gray-500 text-sm">Fetching 10-Ks, 10-Qs, and earnings transcripts...</p>
                        </div>
                    </div>
                ) : error ? (
                    <div className="py-24 bg-red-50 border border-red-100 rounded-[40px] text-center p-12 max-w-2xl mx-auto shadow-2xl shadow-red-500/5">
                        <div className="bg-red-500 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
                            <AlertTriangle className="w-8 h-8 text-white" />
                        </div>
                        <h3 className="text-2xl text-red-900 mb-2 font-headings">Analysis Failed</h3>
                        <p className="text-red-700/70 mb-8 leading-relaxed">{error}</p>
                        <Button variant="secondary" onClick={generateReport} className="border-red-200">
                            Try Again
                        </Button>
                    </div>
                ) : !hasReport ? (
                    <div className="py-32 bg-white rounded-[40px] border border-gray-100 text-center p-12 max-w-3xl mx-auto shadow-sm">
                        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 w-24 h-24 rounded-3xl flex items-center justify-center mx-auto mb-8">
                            <BarChart3 className="w-12 h-12 text-blue-500" />
                        </div>
                        <h3 className="text-2xl text-primary mb-3 font-headings">No Report Active</h3>
                        <p className="text-gray-500 mb-8 leading-relaxed">Enter a public company ticker symbol above to generate a comprehensive AI earnings prep report.</p>
                        <div className="flex flex-col sm:flex-row gap-3 justify-center">
                            {['AAPL', 'TSLA', 'NVDA'].map(t => (
                                <button
                                    key={t}
                                    onClick={() => setTicker(t)}
                                    className="px-4 py-2 bg-gray-100 hover:bg-blue-50 rounded-xl text-sm font-bold transition-colors"
                                >
                                    {t}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <>
                        {/* Stats Cards */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                            <StatCard
                                label="Ticker"
                                value={ticker}
                                icon={BarChart3}
                                trend="neutral"
                            />
                            <StatCard
                                label="Sentiment"
                                value={fetchData?.sentiment?.sentiment || 'Neutral'}
                                icon={TrendingUp}
                                trend={fetchData?.sentiment?.sentiment?.toLowerCase() === 'positive' ? 'up' : 'neutral'}
                                valueClassName={getSentimentColor(fetchData?.sentiment?.sentiment)}
                            />
                            <StatCard
                                label="Positive Signals"
                                value={fetchData?.sentiment?.positive_count || 0}
                                icon={CheckCircle2}
                                trend="up"
                            />
                            <StatCard
                                label="Risk Factors"
                                value={fetchData?.sentiment?.negative_count || 0}
                                icon={AlertTriangle}
                                trend="down"
                            />
                        </div>

                        {/* Tabs */}
                        <div className="bg-white rounded-[32px] border border-gray-100 shadow-sm overflow-hidden mb-12">
                            <div className="border-b border-gray-100">
                                <div className="flex">
                                    {['summary', 'questions', 'contradictions'].map((tab) => (
                                        <button
                                            key={tab}
                                            onClick={() => setActiveTab(tab)}
                                            className={`flex-1 py-5 px-6 text-sm font-bold capitalize transition-colors ${
                                                activeTab === tab
                                                    ? 'text-blue-600 bg-blue-50/50 border-b-2 border-blue-500'
                                                    : 'text-gray-400 hover:text-gray-600'
                                            }`}
                                        >
                                            {tab.replace('_', ' ')}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="p-8">
                                {activeTab === 'summary' && (
                                    <ReportSection
                                        title="Executive Summary"
                                        icon={FileSearch}
                                        content={reportData?.summary || 'No summary available.'}
                                    />
                                )}
                                {activeTab === 'questions' && (
                                    <ReportSection
                                        title="Anticipated Analyst Questions"
                                        icon={MessageSquare}
                                        content={reportData?.questions || 'No questions available.'}
                                    />
                                )}
                                {activeTab === 'contradictions' && (
                                    <ReportSection
                                        title="Potential Contradictions"
                                        icon={AlertTriangle}
                                        content={reportData?.contradictions || 'No contradictions found.'}
                                    />
                                )}
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex gap-4">
                            <Button variant="secondary" icon={Download}>
                                Export PDF
                            </Button>
                            <Button variant="secondary" icon={Share2}>
                                Share Report
                            </Button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
