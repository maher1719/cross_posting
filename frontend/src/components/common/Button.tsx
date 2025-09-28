// A future Button.tsx component, inspired by your thinking
/*
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority'; // A popular library for this pattern

// 1. Define the "Theme API" for the button
const buttonVariants = cva(
  // Base classes that all buttons share
  'inline-flex items-center justify-center rounded-md font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2',
  {
    variants: {
      // "intent" defines the color theme
      intent: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-slate-200 text-slate-900 hover:bg-slate-300 focus:ring-slate-400',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      },
      // "size" defines the padding and text size
      size: {
        small: 'py-1 px-2 text-xs',
        medium: 'py-2 px-4 text-sm',
        large: 'py-3 px-6 text-lg',
      },
    },
    // Default values if no props are provided
    defaultVariants: {
      intent: 'primary',
      size: 'medium',
    },
  }
);

// 2. Define the props for the component, which now includes our theme variants
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {}

// 3. The Button component itself is now incredibly simple
const Button: React.FC<ButtonProps> = ({ className, intent, size, ...props }) => {
  return <button className={buttonVariants({ intent, size, className })} {...props} />;
};

export default Button;
*/