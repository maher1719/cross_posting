// frontend/src/pages/HomePage.tsx

import React from 'react';
import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';
import { usePostForm } from '../hooks/posts'; // Import our new hook

// A simple loading spinner component for a better UX
const Spinner = () => (
    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
);

export const HomePage = () => {
    // Get all the logic and state from our custom hook
    const { content, setContent, error, isLoading, handleSubmit } = usePostForm();

    return (
        <div className="max-w-4xl mx-auto p-4 bg-white rounded-lg shadow-md">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Create a New Post</h1>
            
            {/* The Rich Text Editor */}
            <div className="mb-4">
                <ReactQuill 
                    theme="snow" 
                    value={content} 
                    onChange={setContent}
                    className="bg-white"
                />
            </div>

            {/* Display any submission errors */}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            {/* The Submit Button */}
            <div className="flex justify-end">
                <button
                    type="button"
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="flex items-center justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-300 disabled:cursor-not-allowed"
                >
                    {isLoading ? <Spinner /> : 'Create Post'}
                </button>
            </div>

            {/* Later, you will add a component here to display all existing posts */}
        </div>
    );
};