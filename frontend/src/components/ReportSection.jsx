import React from 'react';
import { Quote } from 'lucide-react';

const ReportSection = ({ title, content, citations = [] }) => {
    return (
        <div className="bg-white rounded-3xl border border-gray-100 p-8 lg:p-12 mb-8 animate-fade-in-up">
            <div className="flex items-center space-x-3 mb-8">
                <div className="w-1 h-8 bg-accent-gradient rounded-full" />
                <h2 className="text-2xl font-headings text-primary">{title}</h2>
            </div>

            <div className="prose prose-blue max-w-none text-gray-600 leading-relaxed space-y-6 text-lg">
                {content}
            </div>

            {citations.length > 0 && (
                <div className="mt-12 pt-8 border-t border-gray-100 space-y-4">
                    <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-400 flex items-center">
                        <Quote className="w-3 h-3 mr-2 text-blue-500" />
                        Verified Citations
                    </h4>
                    <div className="flex flex-wrap gap-4">
                        {citations.map((cite, index) => (
                            <div
                                key={index}
                                className="group flex items-center px-4 py-2 bg-gray-50 rounded-xl border border-gray-100 hover:border-blue-200 transition-colors cursor-pointer"
                            >
                                <div className="w-2 h-2 rounded-full bg-blue-500 mr-3 opacity-50 group-hover:opacity-100" />
                                <span className="text-xs font-bold text-gray-500 group-hover:text-blue-600">
                                    {cite.source} · {cite.page}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ReportSection;
