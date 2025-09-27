// frontend/src/pages/RegisterPage.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For redirecting after success
import { registerUser } from '../api/userApi';

export const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    try {
      const newUser = await registerUser({ username, email, password });
      console.log('Registration successful!', newUser);
      
      // On success, redirect the user to the login page
      navigate('/login');

    } catch (err: any) {
      // Handle errors from the API (like "Email already registered")
      console.error('Registration failed:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('An unknown error occurred.');
      }
    }
  };

  return (
    <div>
      <h1>Create Your Account</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {/* Display any errors from the server */}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        <button type="submit">Register</button>
      </form>
    </div>
  );
};