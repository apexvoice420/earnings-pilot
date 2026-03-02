import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ label, value, trend, icon: Icon, colorClass = 'bg-accent-gradient' }) => {
    return (
        <div className="bg-white p-6 rounded-3xl border border-gray-100 flex items-center justify-between shadow-sm hover:shadow-md transition-shadow duration-300">
            <div className="space-y-2">
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-400">
                    {label}
                </p>
                <div className="flex items-center">
                    <h4 className="text-3xl font-bold text-primary tracking-tight">
                        {value}
                    </h4>
                    {trend !== undefined && (
                        <div className={`ml-3 flex items-center text-xs font-bold px-2 py-0.5 rounded-full ${trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'
                            }`}>
                            {trend > 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                            {Math.abs(trend)}%
                        </div>
                    )}
                </div>
            </div>
            <div className={`p-4 rounded-2xl ${colorClass} shadow-lg`}>
                <Icon className="w-6 h-6 text-white" />
            </div>
        </div>
    );
};

export default StatCard;
