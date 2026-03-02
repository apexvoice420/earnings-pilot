import React, { useState, useEffect } from 'react';
import { NavLink, Link, useLocation } from 'react-router-dom';
import { Layout, Menu as MenuIcon, X, LogIn } from 'lucide-react';
import Button from './Button';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
    const location = useLocation();

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close mobile menu on route change
    useEffect(() => {
        setIsOpen(false);
    }, [location]);

    return (
        <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/80 backdrop-blur-lg border-b border-gray-100 py-3' : 'bg-transparent py-5'
            }`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center">
                    {/* Logo */}
                    <Link to="/" className="flex items-center group">
                        <div className="bg-accent-gradient p-2 rounded-xl mr-3 group-hover:rotate-12 transition-transform duration-300 shadow-lg shadow-blue-500/20">
                            <Layout className="h-6 w-6 text-white" />
                        </div>
                        <span className="text-xl font-headings font-bold text-primary">
                            Earnings Copilot
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-10">
                        <NavLink to="/" className={({ isActive }) =>
                            `text-sm font-semibold transition-colors hover:text-blue-600 ${isActive ? 'text-blue-600' : 'text-gray-600'}`
                        }>
                            Platform
                        </NavLink>
                        <NavLink to="/dashboard" className={({ isActive }) =>
                            `text-sm font-semibold transition-colors hover:text-blue-600 ${isActive ? 'text-blue-600' : 'text-gray-600'}`
                        }>
                            Dashboard
                        </NavLink>
                        <NavLink to="/pricing" className={({ isActive }) =>
                            `text-sm font-semibold transition-colors hover:text-blue-600 ${isActive ? 'text-blue-600' : 'text-gray-600'}`
                        }>
                            Pricing
                        </NavLink>
                        <a href="#" className="text-sm font-semibold text-gray-600 hover:text-blue-600 transition-colors">Resources</a>
                    </div>

                    {/* Actions */}
                    <div className="hidden md:flex items-center space-x-4">
                        <button className="text-sm font-bold text-primary hover:opacity-70 transition-opacity flex items-center">
                            <LogIn className="w-4 h-4 mr-2" />
                            Sign In
                        </button>
                        <Link to="/dashboard">
                            <Button className="px-6 py-2.5 text-sm">Launch App</Button>
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="p-2 text-primary hover:bg-gray-100 rounded-lg"
                        >
                            {isOpen ? <X className="w-6 h-6" /> : <MenuIcon className="w-6 h-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Navigation Dropdown */}
            {isOpen && (
                <div className="md:hidden absolute top-full left-0 right-0 bg-white border-b border-gray-100 shadow-xl p-4 animate-fade-in-up">
                    <div className="flex flex-col space-y-4">
                        <Link to="/" className="text-lg font-semibold text-gray-600 p-2">Platform</Link>
                        <Link to="/dashboard" className="text-lg font-semibold text-gray-600 p-2">Dashboard</Link>
                        <Link to="/pricing" className="text-lg font-semibold text-gray-600 p-2">Pricing</Link>
                        <hr className="border-gray-100" />
                        <div className="flex flex-col space-y-3">
                            <button className="text-primary font-bold p-2 text-left">Sign In</button>
                            <Link to="/dashboard" className="w-full">
                                <Button className="w-full py-4">Launch App</Button>
                            </Link>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
