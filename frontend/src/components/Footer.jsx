import React from 'react';
import { Link } from 'react-router-dom';
import { Layout, Twitter, Linkedin, Github, Mail } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="bg-primary pt-24 pb-12 text-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
                    {/* Brand */}
                    <div className="col-span-1 md:col-span-1">
                        <Link to="/" className="flex items-center mb-6">
                            <div className="bg-accent-gradient p-2 rounded-xl mr-3 shadow-lg">
                                <Layout className="h-6 w-6 text-white" />
                            </div>
                            <span className="text-xl font-headings font-bold">Earnings Copilot</span>
                        </Link>
                        <p className="text-gray-400 text-sm leading-relaxed mb-6">
                            The AI-standard for investor relations and earnings call preparation. Built for CFOs who demand precision.
                        </p>
                        <div className="flex space-x-4">
                            <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors border border-white/10">
                                <Twitter className="w-4 h-4" />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors border border-white/10">
                                <Linkedin className="w-4 h-4" />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors border border-white/10">
                                <Github className="w-4 h-4" />
                            </a>
                        </div>
                    </div>

                    {/* Product */}
                    <div>
                        <h4 className="text-xs font-bold uppercase tracking-[0.2em] text-white/40 mb-8">Product</h4>
                        <ul className="space-y-4 text-sm text-gray-400">
                            <li><Link to="/" className="hover:text-white transition-colors">Platform Overview</Link></li>
                            <li><Link to="/pricing" className="hover:text-white transition-colors">Pricing Plans</Link></li>
                            <li><a href="#" className="hover:text-white transition-colors">Security & Trust</a></li>
                            <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div>
                        <h4 className="text-xs font-bold uppercase tracking-[0.2em] text-white/40 mb-8">Company</h4>
                        <ul className="space-y-4 text-sm text-gray-400">
                            <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                            <li><a href="#" className="hover:text-white transition-colors">IR Resources</a></li>
                            <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                            <li><a href="#" className="hover:text-white transition-colors">Contact Support</a></li>
                        </ul>
                    </div>

                    {/* Newsletter */}
                    <div>
                        <h4 className="text-xs font-bold uppercase tracking-[0.2em] text-white/40 mb-8">Stay Ahead</h4>
                        <p className="text-gray-400 text-sm mb-6">Weekly insights on financial AI delivered to your inbox.</p>
                        <div className="flex gap-2">
                            <input
                                type="email"
                                placeholder="Email address"
                                className="bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
                            />
                            <button className="bg-white text-primary p-2.5 rounded-xl hover:bg-gray-100 transition-colors">
                                <Mail className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>

                <div className="pt-12 border-t border-white/10 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0 text-[10px] font-bold uppercase tracking-widest text-white/30">
                    <p>© 2024 Earnings Copilot Inc. All rights reserved.</p>
                    <div className="flex space-x-8">
                        <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
                        <a href="#" className="hover:text-white transition-colors">Cookie Policy</a>
                        <a href="#" className="hover:text-white transition-colors">Compliance</a>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
