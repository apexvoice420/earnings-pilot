import React from 'react';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import FeatureCard from '../components/FeatureCard';
import PricingCard from '../components/PricingCard';
import { FileText, MessageSquare, Shield, BarChart3, Search, Zap, Download } from 'lucide-react';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div>
            <Hero
                badgeText="V2.0 Now Live — Enhanced AI Models"
                title={
                    <>
                        Prepare for Earnings Calls in <br />
                        <span className="gradient-text">Hours, Not Days</span>
                    </>
                }
                subtitle="AI-powered analysis of 10-Ks, transcripts, and competitor filings. Built for modern IR teams who demand precision and speed."
                primaryCTA="Start Free Trial"
                secondaryCTA="Watch Demo"
                onPrimaryClick={() => navigate('/dashboard')}
                onSecondaryClick={() => navigate('/dashboard')}
            />

            {/* Features Grid */}
            <section className="py-24 bg-white/50 border-y border-gray-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-20 animate-fade-in-up">
                        <h2 className="text-4xl font-headings text-primary mb-4 tracking-tight">Enterprise-Grade Financial Intelligence</h2>
                        <p className="text-gray-500 max-w-2xl mx-auto">Get the insights you need to command every earnings call with confidence.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <FeatureCard
                            icon={FileText}
                            title="Executive Summaries"
                            description="Get 2-page summaries with cited sources for every macro financial shift and strategic pivot."
                        />
                        <FeatureCard
                            icon={MessageSquare}
                            title="Analyst Questions"
                            description="10 anticipated questions based on sentiment trends with suggested data-backed responses."
                        />
                        <FeatureCard
                            icon={Shield}
                            title="Contradiction Detection"
                            description="Instantly find gaps between current 10-K risks and recent transcript-based public claims."
                        />
                        <FeatureCard
                            icon={BarChart3}
                            title="Competitor Benchmarking"
                            description="Compare your strategic positioning across top 3 rivals with real-time filing data."
                        />
                    </div>
                </div>
            </section>

            {/* How it Works */}
            <section className="py-32 relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col lg:flex-row items-center gap-20">
                        <div className="flex-1 space-y-12">
                            <h2 className="text-4xl font-headings text-primary tracking-tight">Three steps to <span className="gradient-text">total clarity</span></h2>

                            <div className="space-y-10">
                                {[
                                    { step: '01', title: 'Enter ticker symbol', desc: 'Input any public company ticker. We fetch all latest filings and audio transcripts automatically.', icon: Search },
                                    { step: '02', title: 'AI analyzes filings & transcripts', desc: 'Our specialized LLMs process thousands of pages to identify risks, opportunities, and sentiment shifts.', icon: Zap },
                                    { step: '03', title: 'Download your prep report', desc: 'Export a professional briefing deck with citations, Q&A, and competitive intelligence.', icon: Download }
                                ].map((item, idx) => (
                                    <div key={idx} className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 rounded-2xl bg-white border border-gray-100 shadow-sm flex items-center justify-center font-headings font-bold text-2xl text-blue-600 transition-all group-hover:bg-accent-gradient group-hover:text-white group-hover:shadow-blue-500/20">
                                            {item.step}
                                        </div>
                                        <div>
                                            <h4 className="text-xl font-bold mb-2 flex items-center">
                                                <item.icon className="w-5 h-5 mr-3 text-blue-500" />
                                                {item.title}
                                            </h4>
                                            <p className="text-gray-500 leading-relaxed text-sm max-w-md">{item.desc}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="flex-1 w-full">
                            <div className="glass-card p-4 aspect-[4/3] bg-primary relative group overflow-hidden shadow-2xl">
                                <img
                                    src="https://images.unsplash.com/photo-1640161704729-cbe966a08476?auto=format&fit=crop&q=80&w=2072"
                                    className="w-full h-full object-cover rounded-2xl opacity-60 group-hover:scale-110 transition-transform duration-1000"
                                    alt="Copilot Dashboard"
                                />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-2xl cursor-pointer hover:scale-110 transition-transform">
                                        <Zap className="w-8 h-8 text-blue-600 fill-blue-600" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing Preview */}
            <section className="py-24 bg-gray-50/50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16 animate-fade-in-up">
                        <h3 className="text-3xl font-headings text-primary mb-4 tracking-tight">Flexible Plans for Every Team</h3>
                        <p className="text-gray-500">Scale your intelligence as your portfolio or company grows.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <PricingCard
                            tier="Starter"
                            price="$19"
                            subtitle="Perfect for retail investors."
                            features={["5 tickers/month", "Executive summaries", "PDF export", "Basic sentiment"]}
                            onCtaClick={() => navigate('/pricing')}
                        />
                        <PricingCard
                            tier="Pro"
                            price="$49"
                            subtitle="For serious analysts."
                            highlighted
                            badge="Most Popular"
                            features={["Unlimited tickers", "Full prep reports", "Sentiment tracking", "Excel export", "Priority support"]}
                            onCtaClick={() => navigate('/pricing')}
                        />
                        <PricingCard
                            tier="Enterprise"
                            price="Custom"
                            subtitle="For institutions."
                            features={["Everything in Pro", "API access", "White-label", "Dedicated support", "SLA guarantee"]}
                            onCtaClick={() => navigate('/pricing')}
                        />
                    </div>
                </div>
            </section>

            {/* CTA Final */}
            <section className="py-24 px-4">
                <div className="max-w-5xl mx-auto bg-primary rounded-[40px] p-12 lg:p-24 text-center text-white relative overflow-hidden shadow-2xl">
                    <div className="absolute top-0 right-0 w-96 h-96 bg-accent-gradient opacity-20 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2" />
                    <h2 className="text-4xl lg:text-5xl font-headings mb-8 relative z-10 leading-tight">Ready to save days <br />of preparation time?</h2>
                    <p className="text-white/60 text-lg mb-12 max-w-2xl mx-auto relative z-10">
                        Join 200+ Investor Relations departments leveraging AI to command the market narrative.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center relative z-10">
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="btn-primary py-4 px-10 text-lg"
                        >
                            Start Free Trial
                        </button>
                        <button className="bg-white/10 hover:bg-white/20 border border-white/10 text-white font-bold py-4 px-10 rounded-xl transition-all">
                            Schedule Demo
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;
