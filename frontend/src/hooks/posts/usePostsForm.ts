// frontend/src/hooks/usePostForm.ts

import { useState } from 'react';
import { createPost } from '../../api/postApi';
import { useAuthStore } from '../../store'; // <-- 1. Import the auth store

export const usePostForm = () => {
  const [content, setContent] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // --- 2. THIS IS THE MAJOR ENHANCEMENT ---
  // We get the entire 'user' object from our global state.
  // This hook will automatically re-render if the user logs in or out.
  const currentUser = useAuthStore((state) => state.user);

  const handleSubmit = async () => {
    // --- 3. ADD A "GUARD CLAUSE" FOR SECURITY ---
    // This check prevents a non-logged-in user from even trying to submit.
    if (!currentUser) {
      setError('You must be logged in to create a post.');
      return;
    }

    if (!content || content === '<p><br></p>') {
      setError('Post content cannot be empty.');
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      // --- 4. USE THE REAL USER ID FROM THE STORE! ---
      // We pass the 'id' from the currentUser object.
      await createPost({ content, user_id: currentUser.id });
      
      // On success, we can clear the form and celebrate
      setContent('');
      alert('Post created successfully!');
      // In a real app, you would also trigger a refresh of the post list here.

    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create post.');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    content,
    setContent,
    error,
    isLoading,
    handleSubmit,
  };
};