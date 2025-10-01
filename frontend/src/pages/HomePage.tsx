// frontend/src/pages/HomePage.tsx

import { useRef } from 'react';
import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';
import { usePostForm } from '../hooks/posts/usePostsForm';

const Spinner = () => (
    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
);

export const HomePage = () => {
    // --- THE FIX ---
    // 1. Create the ref here, in the component that owns the editor.
    const quillRef = useRef<ReactQuill>(null);

    // 2. The hook is now simple and doesn't need the ref.
    const { content, setContent, error, isLoading, handleSubmit } = usePostForm();

    // 3. Create a new click handler here in the component.
    const handleCreatePost = () => {
        // 4. Get the plain text from the editor *right here*.
        //    We use a check to make sure the ref is connected.
        const editor = quillRef.current?.getEditor();
        const contentText = editor ? editor.getText() : '';
        
        // 5. Pass the plain text to the hook's handleSubmit function.
        handleSubmit(contentText);
    };

    return (
        <div className="max-w-4xl mx-auto p-4 bg-white rounded-lg shadow-md">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Create a New Post</h1>
            
            <div className="mb-4">
                <ReactQuill 
                    ref={quillRef} // The ref is attached here
                    theme="snow" 
                    value={content} 
                    onChange={setContent}
                    className="bg-white"
                />
            </div>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            <div className="flex justify-end">
                {/* 6. The button now calls our new click handler. */}
                <button
                    type="button"
                    onClick={handleCreatePost} 
                    disabled={isLoading}
                    className="flex items-center justify-center rounded-md ..."
                >
                    {isLoading ? <Spinner /> : 'Create Post'}
                </button>
            </div>
        </div>
    );
};