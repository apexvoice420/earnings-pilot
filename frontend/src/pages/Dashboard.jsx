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
    CheckCircle2
} from 'lucide-react';
import StatCard from '../components/StatCard';
import ReportSection from '../components/ReportSection';
import Button from '../components/Button';

const Dashboard = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [ticker, setTicker] = useState('AAPL');
    const [hasReport, setHasReport] = useState(false);
    const [activeTab, setActiveTab] = useState('summary');

    const generateReport = () => {
        setLoading(true);
        setError(null);
        setHasReport(false);

        // Simulate API call
        setTimeout(() => {
            setLoading(false);
            setHasReport(true);
        }, 2500);
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
                            System Ready · Version 2.4.1
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
                    /* Loading State */
                    <div className="py-32 flex flex-col items-center justify-center space-y-8 animate-pulse">
                        <div className="relative">
                            <div className="w-24 h-24 border-4 border-blue-100 border-t-blue-500 rounded-full animate-spin" />
                            <Zap className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-blue-500" />
                        </div>
                        <div className="text-center space-y-2">
                            <h3 className="text-xl font-bold text-primary">Scanning Filings for {ticker}</h3>
                            <p className="text-gray-500 text-sm">Our AI is parsing 10-Ks, 10-Qs, and historical transcripts...</p>
                        </div>
                    </div>
                ) : error ? (
                    /* Error State */
                    <div className="py-24 bg-red-50 border border-red-100 rounded-[40px] text-center p-12 max-w-2xl mx-auto shadow-2xl shadow-red-500/5">
                        <div className="bg-red-500 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6">
                            <AlertTriangle className="w-8 h-8 text-white" />
                        </div>
                        <h3 className="text-2xl text-red-900 mb-2 font-headings">Analysis Failed</h3>
                        <p className="text-red-700/70 mb-8 leading-relaxed">We couldn't retrieve filings for ticker "{ticker}". This may be due to a connection issue or an invalid ticker symbol.</p>
                        <Button variant="secondary" onClick={generateReport} className="border-red-200">
                            Try Again
                        </Button>
                    </div>
                ) : !hasReport ? (
                    /* Empty State */
                    <div className="py-32 bg-white/50 border border-dashed border-gray-200 rounded-[40px] text-center px-12 animate-fade-in-up">
                        <div className="bg-blue-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-8">
                            <FileSearch className="w-10 h-10 text-blue-500" />
                        </div>
                        <h3 className="text-2xl text-primary font-headings mb-3">No Report Active</h3>
                        <p className="text-gray-500 max-w-md mx-auto mb-10">Start by entering a public company ticker symbol above to generate a comprehensive AI earnings prep report.</p>
                        <div className="flex justify-center gap-6 text-xs font-bold uppercase tracking-widest text-gray-400">
                            <span className="flex items-center"><CheckCircle2 className="w-3.5 h-3.5 mr-2" /> 10-K Data</span>
                            <span className="flex items-center"><CheckCircle2 className="w-3.5 h-3.5 mr-2" /> Transcripts</span>
                            <span className="flex items-center"><CheckCircle2 className="w-3.5 h-3.5 mr-2" /> Q&A Deck</span>
                        </div>
                    </div>
                ) : (
                    /* Report State */
                    <div className="animate-fade-in-up space-y-10">
                        {/* Stats Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            <StatCard label="Analyst Sentiment" value="Bullish" trend={+14} icon={TrendingUp} />
                            <StatCard label="Strategic Risks" value="5 New" trend={-2} icon={AlertTriangle} colorClass="bg-warning-gradient" />
                            <StatCard label="Q&A Readiness" value="92%" icon={MessageSquare} />
                            <StatCard label="Data Sources" value="1,240 pg" icon={BarChart3} colorClass="bg-slate-700" />
                        </div>

                        {/* Main Content Layout */}
                        <div className="flex flex-col lg:flex-row gap-8">
                            {/* Report Viewer */}
                            <div className="flex-grow">
                                <div className="bg-white rounded-3xl border border-gray-100 overflow-hidden shadow-sm">
                                    <div className="border-b border-gray-100 bg-gray-50/50 p-2 flex justify-between items-center">
                                        <div className="flex gap-1">
                                            {[
                                                { id: 'summary', label: 'Executive' },
                                                { id: 'qa', label: 'Analyst Q&A' },
                                                { id: 'bench', label: 'Competitors' }
                                            ].map(tab => (
                                                <button
                                                    key={tab.id}
                                                    onClick={() => setActiveTab(tab.id)}
                                                    className={`px-6 py-3 rounded-2xl text-xs font-bold uppercase tracking-widest transition-all ${activeTab === tab.id
                                                            ? 'bg-white text-blue-600 shadow-sm shadow-blue-500/10'
                                                            : 'text-gray-400 hover:text-primary hover:bg-gray-100'
                                                        }`}
                                                >
                                                    {tab.label}
                                                </button>
                                            ))}
                                        </div>
                                        <div className="flex gap-2 pr-2">
                                            <Button variant="ghost" className="p-2 border-none">
                                                <Download className="w-4 h-4" />
                                            </Button>
                                            <Button variant="ghost" className="p-2 border-none">
                                                <Share2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>

                                    <div className="p-4 lg:p-8 bg-background/30">
                                        {activeTab === 'summary' && (
                                            <ReportSection
                                                title={`${ticker}: Strategic Positioning & Risk Factors`}
                                                content={
                                                    <>
                                                        <p>
                                                            Microsoft's latest 10-K indicates a significant reallocation of capital toward **GPU-integrated data centers**, with a projected <span className="text-blue-600 font-bold">22% increase in Capex</span> for FY2025. This move suggests a dominant push into generative AI infrastructure, potentially outpacing AWS in server-side LLM capacity.
                                                        </p>
                                                        <p>
                                                            Key risks identified involve the tightening regulatory environment in the EU. Unlike the previous quarter, there is a new focus on **interoperability compliance** within Azure's core services, which may impact margin retention in the mid-market segment.
                                                        </p>
                                                    </>
                                                }
                                                citations={[
                                                    { source: "SEC 10-K / Azure Segment", page: "P. 14" },
                                                    { source: "Transcript Q3 2024", page: "L. 240" }
                                                ]}
                                            />
                                        )}

                                        {activeTab === 'qa' && (
                                            <div className="space-y-6">
                                                {[
                                                    { q: "How do you project the ROI on the latest $10B silicon expansion given the current energy constraints?", a: "Discuss the 15% efficiency gain in M3-silicon and the long-term energy contracts reducing variable COGS." },
                                                    { q: "What is the expected churn rate for the Co-Pilot seat licenses among SMB customers?", a: "Focus on the high retention in enterprise and the cross-sell momentum into the security stack." }
                                                ].map((item, idx) => (
                                                    <div key={idx} className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
                                                        <h4 className="font-bold text-primary mb-2">Analyst Question: {item.q}</h4>
                                                        <p className="text-gray-500 text-sm leading-relaxed italic">Prep: {item.a}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        )}

                                        {activeTab === 'bench' && (
                                            <div className="text-center py-20 bg-white rounded-3xl border border-gray-100">
                                                <div className="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center mx-auto mb-6">
                                                    <BarChart3 className="w-8 h-8 text-blue-500" />
                                                </div>
                                                <h3 className="text-xl font-bold">Competitor Insights Ready</h3>
                                                <p className="text-gray-500 text-sm mb-6">Benchmarked against Amazon and Google Cloud.</p>
                                                <Button variant="secondary" className="px-8">View Benchmarking Deck</Button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Sidebar Info */}
                            <div className="lg:w-80 space-y-8">
                                <div className="bg-primary p-8 rounded-[40px] text-white space-y-6 shadow-2xl overflow-hidden relative">
                                    <div className="absolute top-0 right-0 w-32 h-32 bg-accent-gradient opacity-30 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
                                    <div className="relative z-10">
                                        <h4 className="text-xs font-bold uppercase tracking-widest text-white/50 mb-6">Export Readiness</h4>
                                        <div className="space-y-4">
                                            {['PDF Briefing', 'PowerPoint Deck', 'Markdown Summary'].map((item, idx) => (
                                                <button key={idx} className="w-full flex justify-between items-center text-sm font-semibold hover:text-blue-400 transition-colors">
                                                    {item}
                                                    <ArrowUpRight className="w-4 h-4 opacity-40" />
                                                </button>
                                            ))}
                                        </div>
                                        <Button className="w-full mt-10 bg-white text-primary hover:bg-gray-100 border-none shadow-none">
                                            Download All
                                        </Button>
                                    </div>
                                </div>

                                <div className="bg-white p-8 rounded-[40px] border border-gray-100 shadow-sm space-y-6">
                                    <h4 className="text-xs font-bold uppercase tracking-widest text-gray-400">Next Earnings Event</h4>
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center font-bold text-blue-600">
                                            Oct
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-primary">Q4 Earnings Call</p>
                                            <p className="text-xs text-gray-400">Oct 24, 2024 · 5:00 PM EST</p>
                                        </div>
                                    </div>
                                    <button className="w-full text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center">
                                        Add to Outlook / Calendar <ChevronRight className="w-3 h-3 ml-1" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
