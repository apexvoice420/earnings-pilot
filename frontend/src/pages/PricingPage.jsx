import React from 'react';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import PricingCard from '../components/PricingCard';
import { CheckCircle, X, HelpCircle } from 'lucide-react';

const PricingPage = () => {
    const navigate = useNavigate();

    const tiers = [
        {
            name: 'Starter',
            price: '$19',
            period: '/month',
            description: 'Perfect for retail investors and casual researchers.',
            features: [
                { text: '5 ticker analyses per month', included: true },
                { text: 'Executive summaries with citations', included: true },
                { text: 'PDF export', included: true },
                { text: 'Basic sentiment analysis', included: true },
                { text: 'Historical comparisons', included: false },
                { text: 'Excel export', included: false },
                { text: 'API access', included: false },
            ],
            cta: 'Start Free Trial',
            highlighted: false,
        },
        {
            name: 'Pro',
            price: '$49',
            period: '/month',
            description: 'For serious analysts who need deep insights daily.',
            features: [
                { text: 'Unlimited ticker analyses', included: true },
                { text: 'Full earnings prep reports', included: true },
                { text: 'Sentiment trend tracking (4 quarters)', included: true },
                { text: 'PDF + Excel export', included: true },
                { text: 'Real-time alerts', included: true },
                { text: 'Priority support', included: true },
                { text: 'API access', included: false },
            ],
            cta: 'Start Pro Trial',
            highlighted: true,
            badge: 'Most Popular',
        },
        {
            name: 'Enterprise',
            price: 'Custom',
            period: '',
            description: 'For funds and IR teams who need institutional-grade tools.',
            features: [
                { text: 'Everything in Pro', included: true },
                { text: 'API access with rate limits', included: true },
                { text: 'White-label reports', included: true },
                { text: 'SSO & advanced security', included: true },
                { text: 'Custom model training', included: true },
                { text: 'Dedicated account manager', included: true },
                { text: 'SLA guarantee', included: true },
            ],
            cta: 'Contact Sales',
            highlighted: false,
        },
    ];

    const faqs = [
        {
            question: 'How accurate are the AI summaries?',
            answer: 'Every claim includes a citation linking directly to the source in the 10-K or transcript. If our AI cannot find information in the filings, it explicitly says "Not disclosed" rather than guessing.',
        },
        {
            question: 'Can I try before I buy?',
            answer: 'Yes! Both Starter and Pro plans include a 7-day free trial. No credit card required to start.',
        },
        {
            question: 'How fast are reports generated?',
            answer: 'Reports are typically generated in 30-60 seconds. We fetch live data from SEC EDGAR, so speed depends on filing size and current load.',
        },
        {
            question: 'What tickers are supported?',
            answer: 'We support all US-listed public companies with SEC filings. Currently optimized for: AAPL, TSLA, NVDA, MSFT, GOOGL, AMZN, META, and 500+ more.',
        },
        {
            question: 'Can I cancel anytime?',
            answer: 'Absolutely. No long-term contracts. Cancel anytime from your account settings.',
        },
    ];

    const competitors = [
        { name: 'Earnings Copilot', starter: '$19', pro: '$49', sentiment: '✅', citations: '✅', excel: '✅' },
        { name: 'Seeking Alpha Premium', starter: '$20', pro: '-', sentiment: '❌', citations: '❌', excel: '❌' },
        { name: 'FinChat.io', starter: '$24', pro: '$64', sentiment: '✅', citations: '✅', excel: '✅' },
        { name: 'Quartr', starter: 'Free', pro: '$30', sentiment: '✅', citations: '❌', excel: '❌' },
        { name: 'ChatGPT Plus', starter: '$20', pro: '-', sentiment: '❌', citations: '❌', excel: '❌' },
    ];

    return (
        <div>
            <Hero
                badgeText="Simple, Transparent Pricing"
                title={
                    <>
                        Enterprise-grade analysis<br />
                        <span className="gradient-text">at retail prices</span>
                    </>
                }
                subtitle="Start free. Upgrade when you need more. Cancel anytime."
            />

            {/* Pricing Cards */}
            <section className="py-16 bg-white/50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {tiers.map((tier, idx) => (
                            <div
                                key={idx}
                                className={`relative bg-white rounded-[32px] p-8 border ${
                                    tier.highlighted
                                        ? 'border-blue-500 shadow-xl shadow-blue-500/10'
                                        : 'border-gray-100 shadow-sm'
                                }`}
                            >
                                {tier.badge && (
                                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-500 text-white text-xs font-bold rounded-full">
                                        {tier.badge}
                                    </div>
                                )}

                                <div className="mb-6">
                                    <h3 className="text-xl font-bold text-gray-900">{tier.name}</h3>
                                    <p className="text-sm text-gray-500 mt-1">{tier.description}</p>
                                </div>

                                <div className="mb-6">
                                    <span className="text-4xl font-bold text-gray-900">{tier.price}</span>
                                    <span className="text-gray-500">{tier.period}</span>
                                </div>

                                <ul className="space-y-3 mb-8">
                                    {tier.features.map((feature, fidx) => (
                                        <li key={fidx} className="flex items-center gap-3">
                                            {feature.included ? (
                                                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                            ) : (
                                                <X className="w-5 h-5 text-gray-300 flex-shrink-0" />
                                            )}
                                            <span className={feature.included ? 'text-gray-700' : 'text-gray-400'}>
                                                {feature.text}
                                            </span>
                                        </li>
                                    ))}
                                </ul>

                                <button
                                    onClick={() => tier.name === 'Enterprise' ? navigate('/contact') : navigate('/dashboard')}
                                    className={`w-full py-3 px-6 rounded-xl font-bold transition-all ${
                                        tier.highlighted
                                            ? 'bg-blue-500 text-white hover:bg-blue-600'
                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                    }`}
                                >
                                    {tier.cta}
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Competitor Comparison */}
            <section className="py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-2xl font-bold text-center mb-8">How we compare</h2>
                    <div className="overflow-x-auto">
                        <table className="w-full bg-white rounded-2xl border border-gray-100 overflow-hidden">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-900">Tool</th>
                                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-900">Starter</th>
                                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-900">Pro</th>
                                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-900">Sentiment</th>
                                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-900">Citations</th>
                                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-900">Excel</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {competitors.map((comp, idx) => (
                                    <tr key={idx} className={comp.name === 'Earnings Copilot' ? 'bg-blue-50' : ''}>
                                        <td className={`px-6 py-4 text-sm font-medium ${comp.name === 'Earnings Copilot' ? 'text-blue-600' : 'text-gray-700'}`}>
                                            {comp.name}
                                        </td>
                                        <td className="px-6 py-4 text-center text-sm text-gray-600">{comp.starter}</td>
                                        <td className="px-6 py-4 text-center text-sm text-gray-600">{comp.pro}</td>
                                        <td className="px-6 py-4 text-center">{comp.sentiment}</td>
                                        <td className="px-6 py-4 text-center">{comp.citations}</td>
                                        <td className="px-6 py-4 text-center">{comp.excel}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            {/* FAQ */}
            <section className="py-16 bg-white/50">
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-2xl font-bold text-center mb-12">Frequently Asked Questions</h2>
                    <div className="space-y-4">
                        {faqs.map((faq, idx) => (
                            <details key={idx} className="group bg-white rounded-2xl border border-gray-100 overflow-hidden">
                                <summary className="flex items-center justify-between p-6 cursor-pointer">
                                    <span className="font-medium text-gray-900">{faq.question}</span>
                                    <HelpCircle className="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform" />
                                </summary>
                                <div className="px-6 pb-6 text-gray-600">
                                    {faq.answer}
                                </div>
                            </details>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-16">
                <div className="max-w-4xl mx-auto px-4 text-center">
                    <h2 className="text-3xl font-bold mb-4">Ready to try it?</h2>
                    <p className="text-gray-500 mb-8">Start your free trial today. No credit card required.</p>
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="px-8 py-4 bg-blue-500 text-white font-bold rounded-xl hover:bg-blue-600 transition-colors"
                    >
                        Start Free Trial
                    </button>
                </div>
            </section>
        </div>
    );
};

export default PricingPage;
