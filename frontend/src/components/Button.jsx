import React from 'react';

const Button = ({
    children,
    variant = 'primary',
    className = '',
    onClick,
    disabled = false,
    type = 'button',
    icon: Icon
}) => {
    const baseStyles = 'inline-flex items-center justify-center transition-all duration-300 font-semibold active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed';

    const variants = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
        outline: 'btn-outline',
        ghost: 'text-primary hover:bg-primary/5 px-4 py-2 rounded-lg'
    };

    const selectedVariant = variants[variant] || variants.primary;

    return (
        <button
            type={type}
            className={`${baseStyles} ${selectedVariant} ${className}`}
            onClick={onClick}
            disabled={disabled}
        >
            {Icon && <Icon className="w-5 h-5 mr-2" />}
            {children}
        </button>
    );
};

export default Button;
