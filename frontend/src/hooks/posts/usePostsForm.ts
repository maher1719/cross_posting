// frontend/src/hooks/usePostForm.ts

import { useState } from 'react';
import { createPost } from '../../api/postApi';
import { useAuthStore } from '../../store';

// --- THE BIG CHANGE: The hook no longer accepts the ref ---
export const usePostForm = () => {
  const [content, setContent] = useState(''); // This is the HTML content
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const currentUser = useAuthStore((state) => state.user);
  const [generateForTwitter, setGenerateForTwitter] = useState(false);

  // --- The submit function now takes the plain text as an argument ---
  const handleSubmit = async (contentText: string) => {
    if (!currentUser) {
      setError('You must be logged in to create a post.');
      return;
    }

    if (!contentText.trim()) {
      setError('Post content cannot be empty.');
      return;
    }
    
    setError(null);
    setIsLoading(true);

    try {
      // The hook now receives both versions of the content when it's needed
      await createPost({ 
        content_html: content, 
        content_text: contentText, 
        user_id: currentUser.id,
        generate_for_twitter: generateForTwitter 
      });
      
      setContent('');
      alert('Post created successfully!');
      
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create post.');
    } finally {
      setIsLoading(false);
    }
  };

  return { content, setContent, generateForTwitter, setGenerateForTwitter, error, isLoading, handleSubmit,  };
};