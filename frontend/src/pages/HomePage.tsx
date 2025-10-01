import React, { useState } from 'react';
import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';

export const HomePage = () => {
    const [value, setValue] = useState('');
    console.log("HomePage component is rendering!");
    return (
        <div>
            <h1 className="text-3xl font-bold underline" >Welcome to the Cross-Posting App!</h1>
            <ReactQuill theme="snow" value={value} onChange={setValue} />;
            <p>This is the home page.</p>
        </div>
    );
};