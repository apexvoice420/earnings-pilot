import React from 'react';
import Button from './Button';
import { ArrowRight } from 'lucide-react';

const Hero = ({
    title,
    subtitle,
    primaryCTA,
    secondaryCTA,
    onPrimaryClick,
    onSecondaryClick,
    badgeText
}) => {
    return (
        <div className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
            {/* Background Decor */}
            <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-[1000px] h-[1000px] bg-blue-50/50 rounded-full blur-[120px] -z-10" />
            <div className="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-cyan-50/30 rounded-full blur-[100px] -z-10" />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                {badgeText && (
                    <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-blue-50 border border-blue-100 mb-8 animate-fade-in-up">
                        <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
                        <span className="text-xs font-bold text-blue-600 uppercase tracking-widest">{badgeText}</span>
                    </div>
                )}

                <h1 className="text-5xl lg:text-8xl mb-8 tracking-tighter leading-[0.95] animate-fade-in-up">
                    {title}
                </h1>

                <p className="text-xl lg:text-2xl text-gray-600 max-w-3xl mx-auto mb-12 leading-relaxed animate-fade-in-up [animation-delay:200ms]">
                    {subtitle}
                </p>

                <div className="flex flex-col sm:flex-row items-center justify-center gap-5 animate-fade-in-up [animation-delay:400ms]">
                    {primaryCTA && (
                        <Button onClick={onPrimaryClick} className="w-full sm:w-auto px-10 py-5 text-lg">
                            {primaryCTA}
                            <ArrowRight className="ml-2 w-6 h-6" />
                        </Button>
                    )}
                    {secondaryCTA && (
                        <Button variant="secondary" onClick={onSecondaryClick} className="w-full sm:w-auto px-10 py-5 text-lg">
                            {secondaryCTA}
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Hero;
