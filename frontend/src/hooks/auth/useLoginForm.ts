// frontend/src/hooks/auth/useLoginForm.ts
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../../api/userApi';
import { useAuthStore } from '../../store';

export const useLoginForm = () => {
  // 1. All the state management lives here now.
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // 2. The event handler logic lives here.
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await loginUser({ email, password });
      // On success, redirect the user to the login page
      
      if (response.access_token) {
        useAuthStore.getState().login(response.access_token);
        console.log(response.access_token)
        navigate('/home');
      }
      
    } catch (err: any) {
      setError(err.response?.data?.error || 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  // 3. Return everything the UI needs to function.
  // We return an object containing the state values, the state setters,
  // and the event handler function.
  return {
    email,
    setEmail,
    password,
    setPassword,
    error,
    isLoading,
    handleSubmit,
  };
};