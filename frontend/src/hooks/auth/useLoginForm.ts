// frontend/src/hooks/auth/useLoginForm.ts
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../../api/userApi';
import { useAuthStore } from '../../store';

export const useLoginForm = () => {
  // 1. All the state management lives here now.
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuthStore();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  // 2. The event handler logic lives here.
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {

      // On success, redirect the user to the login page
      
      const responseData = await loginUser({ email, password });
      
      // --- THIS IS THE ENHANCEMENT ---
      // Call the login action with both the token and the user object
      login(responseData.access_token, responseData.user);
      console.log(responseData);

      navigate('/');
      
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