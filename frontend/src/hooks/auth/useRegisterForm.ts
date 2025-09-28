// frontend/src/hooks/useRegisterForm.ts

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../../api/userApi';

export const useRegisterForm = () => {
  // 1. All the state management lives here now.
  const [username, setUsername] = useState('');
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
      const result=await registerUser({ username, email, password });
      // On success, redirect the user to the login page
      console.log(result);
      navigate('/login');
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
    username,
    setUsername,
    email,
    setEmail,
    password,
    setPassword,
    error,
    isLoading,
    handleSubmit,
  };
};