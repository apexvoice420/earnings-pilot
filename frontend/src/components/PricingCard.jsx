import React from 'react';

const PricingCard = ({ tier, price, subtitle, features, highlighted, onCtaClick, badge }) => {
    return (
        <div className={`relative p-8 rounded-[32px] border transition-all ${
            highlighted
                ? 'bg-white border-blue-500 shadow-xl shadow-blue-500/10'
                : 'bg-white border-gray-100 shadow-sm'
        }`}>
            {badge && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-500 text-white text-xs font-bold rounded-full">
                    {badge}
                </div>
            )}
            
            <div className="mb-4">
                <h3 className="text-xl font-bold text-gray-900">{tier}</h3>
                <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
            </div>
            
            <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">{price}</span>
                {price !== 'Custom' && <span className="text-gray-500">/mo</span>}
            </div>
            
            <ul className="space-y-3 mb-8">
                {features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-3 text-sm">
                        <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-gray-600">{feature}</span>
                    </li>
                ))}
            </ul>
            
            <button
                onClick={onCtaClick}
                className={`w-full py-3 px-6 rounded-xl font-bold transition-all ${
                    highlighted
                        ? 'bg-blue-500 text-white hover:bg-blue-600'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
            >
                {price === 'Custom' ? 'Contact Sales' : 'Start Free Trial'}
            </button>
        </div>
    );
};

export default PricingCard;
