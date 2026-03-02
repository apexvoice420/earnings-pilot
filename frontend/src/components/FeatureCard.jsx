import React from 'react';

const FeatureCard = ({ icon: Icon, title, description, badge }) => {
    return (
        <div className="glass-card p-10 card-hover group h-full flex flex-col items-start text-left border-gray-100">
            <div className="bg-accent-gradient w-16 h-16 rounded-2xl flex items-center justify-center mb-8 shadow-2xl shadow-blue-500/30 group-hover:rotate-[10deg] transition-transform duration-500">
                <Icon className="w-8 h-8 text-white" />
            </div>

            {badge && (
                <span className="mb-4 inline-block px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold uppercase tracking-widest rounded-full">
                    {badge}
                </span>
            )}

            <h3 className="text-2xl mb-4 text-primary leading-tight font-headings tracking-tight">
                {title}
            </h3>

            <p className="text-gray-500 leading-relaxed font-sans text-sm">
                {description}
            </p>
        </div>
    );
};

export default FeatureCard;
