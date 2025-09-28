import React from 'react';

export const HomePage = () => {
    console.log("HomePage component is rendering!");
    return (
        <div>
            <h1 className="text-3xl font-bold underline" >Welcome to the Cross-Posting App!</h1>
            <p>This is the home page.</p>
        </div>
    );
};