import React from 'react';
import { Check } from 'lucide-react';
import Button from './Button';

const PricingCard = ({
    tier,
    price,
    subtitle,
    features,
    ctaText = 'Get Started',
    highlighted = false,
    onCtaClick
}) => {
    return (
        <div className={`relative glass-card p-10 flex flex-col h-full border-gray-100 transition-all duration-500 ${highlighted ? 'ring-2 ring-blue-500 scale-105 z-10 shadow-blue-500/10' : 'hover:-translate-y-2'
            }`}>
            {highlighted && (
                <div className="absolute top-0 right-10 -translate-y-1/2 bg-accent-gradient text-white text-[10px] font-bold uppercase tracking-[0.2em] px-5 py-2 rounded-full shadow-xl">
                    Most Popular
                </div>
            )}

            <h3 className="text-2xl text-primary font-headings mb-2">{tier}</h3>

            <div className="flex items-baseline mb-4">
                <span className="text-5xl font-bold text-primary tracking-tighter">{price}</span>
                {price !== 'Custom' && <span className="text-gray-400 ml-2 font-medium">/call</span>}
            </div>

            <p className="text-gray-500 text-sm mb-10 min-h-[40px] leading-relaxed">
                {subtitle}
            </p>

            <div className="flex-grow space-y-5 mb-12">
                {features.map((feature, index) => (
                    <div key={index} className="flex items-start text-sm text-gray-600">
                        <div className="bg-blue-50 p-1 rounded-full mr-4 mt-0.5">
                            <Check className="w-3.5 h-3.5 text-blue-600 stroke-[3]" />
                        </div>
                        <span>{feature}</span>
                    </div>
                ))}
            </div>

            <Button
                variant={highlighted ? 'primary' : 'secondary'}
                className="w-full py-4 text-sm font-bold uppercase tracking-widest"
                onClick={onCtaClick}
            >
                {ctaText}
            </Button>
        </div>
    );
};

export default PricingCard;
