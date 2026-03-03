import React, { useState } from 'react';
import Hero from '../components/Hero';
import PricingCard from '../components/PricingCard';
import Button from '../components/Button';
import { ChevronDown, ChevronUp, CheckCircle2 } from 'lucide-react';

const FAQItem = ({ question, answer }) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className={`bg-white rounded-[32px] border ${isOpen ? 'border-blue-500/20 shadow-xl shadow-blue-500/5' : 'border-gray-100'} overflow-hidden transition-all duration-300 mb-4`}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full p-8 flex justify-between items-center text-left"
            >
                <span className="text-lg font-bold text-primary pr-8">{question}</span>
                <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${isOpen ? 'bg-blue-500 text-white' : 'bg-gray-50 text-gray-400'}`}>
                    {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                </div>
            </button>

            {isOpen && (
                <div className="px-8 pb-8 animate-fade-in-up">
                    <p className="text-gray-500 leading-relaxed max-w-2xl">{answer}</p>
                </div>
            )}
        </div>
    );
};

const PricingPage = () => {
    return (
        <div className="bg-background min-h-screen">
            <Hero
                badgeText="Simple, Predictable Costs"
                title={
                    <>
                        Plans for Teams of <br />
                        <span className="gradient-text">Every Size</span>
                    </>
                }
                subtitle="No hidden fees. No complex contracts. Strategic intelligence built to scale with your IR needs."
            />

            <section className="pb-32">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-40">
                        <PricingCard
                            tier="Starter"
                            price="$497"
                            subtitle="Perfect for deep-dives into single target companies."
                            features={[
                                "1 Strategic Report / Mo",
                                "Standard Executive Summary",
                                "Basic Q&A Preparation",
                                "Email Report Delivery",
                                "PDF Download"
                            ]}
                        />
                        <PricingCard
                            tier="Quarterly"
                            price="$1,497"
                            subtitle="Full coverage for IR teams managing internal communications."
                            highlighted
                            features={[
                                "5 Company Analyses / Qtr",
                                "Full Prep Deck (PPT/PDF)",
                                "Citation Verification",
                                "Priority AI Generation",
                                "Analyst Sentiment Trends",
                                "Dedicated Support Link"
                            ]}
                        />
                        <PricingCard
                            tier="Enterprise"
                            price="$4,997"
                            subtitle="Global solution for institutions and Fortune 500 IR teams."
                            features={[
                                "Unlimited Analyses",
                                "White-Glove Support",
                                "Custom LLM Fine-Tuning",
                                "SSO & Role-Based Access",
                                "Direct API Access",
                                "Strategic Account Manager"
                            ]}
                        />
                    </div>

                    {/* FAQ Section */}
                    <div className="max-w-3xl mx-auto">
                        <div className="text-center mb-16">
                            <h2 className="text-3xl font-headings text-primary mb-4 tracking-tight">Frequently Asked Questions</h2>
                            <p className="text-gray-500">Need more information? Reach out to our sales team.</p>
                        </div>

                        <div className="space-y-4">
                            <FAQItem
                                question="How does the AI ensure accuracy in financial reporting?"
                                answer="Our models are specialized financial-LLMs that use Retrieval Augmented Generation (RAG). Every data point is directly linked to an SEC Edgar filing or official transcript with page and line number citations."
                            />
                            <FAQItem
                                question="Can I upgrade my plan in the middle of a quarter?"
                                answer="Yes, you can upgrade at any time from your dashboard. Most users transition from Starter to Quarterly once their coverage list exceeds 3 tickers."
                            />
                            <FAQItem
                                question="Is my proprietary internal data used to train the models?"
                                answer="No. Your internal notes, uploads, and queries are strictly siloed. We never use client data to train our shared base models, ensuring SOC2-compliant data privacy."
                            />
                            <FAQItem
                                question="Which exchanges and filings do you support?"
                                answer="We currently support all major US exchanges (NYSE, NASDAQ). Our engine parses 10-Ks, 10-Qs, 8-Ks, and S-1s, as well as publicly available earnings transcripts."
                            />
                            <FAQItem
                                question="Do you offer custom pricing for non-profits or education?"
                                answer="We offer discounted Enterprise rates for educational institutions and smaller IR non-profits. Please contact sales@earningscopilot.com for more info."
                            />
                        </div>
                    </div>
                </div>
            </section>

            {/* Trust Quote */}
            <section className="py-24 bg-primary text-white overflow-hidden relative">
                <div className="absolute top-0 right-0 w-64 h-64 bg-accent-gradient opacity-10 rounded-full blur-[100px]" />
                <div className="max-w-4xl mx-auto px-4 text-center space-y-8 relative z-10">
                    <h4 className="text-xs font-bold uppercase tracking-[0.3em] text-white/40">Trusted by Professionals</h4>
                    <p className="text-3xl lg:text-4xl font-headings leading-tight italic">
                        "Earnings Copilot has effectively saved our IR team over 40 hours of manual lookup every quarter. The Q&A prep is eerily accurate."
                    </p>
                    <div className="flex items-center justify-center space-x-4">
                        <div className="w-12 h-12 rounded-full bg-blue-500/20 border border-white/10" />
                        <div className="text-left">
                            <p className="font-bold">Director of IR</p>
                            <p className="text-xs text-white/40">Fortune 500 Technology Leader</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Support CTA */}
            <section className="py-24 text-center px-4">
                <h3 className="text-2xl font-bold text-primary mb-6">Still have questions?</h3>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button variant="secondary" className="px-10">Chat with Sales</Button>
                    <Button variant="outline" className="px-10">View Documentation</Button>
                </div>
            </section>
        </div>
    );
};

export default PricingPage;
