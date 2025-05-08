// src/components/Login.tsx

import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';
import { LockClosedIcon } from '@heroicons/react/24/solid';
import hungryCowImg from '../assets/hungry_cow.png';

export default function Login() {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    console.log('handleSubmit', username);
    e.preventDefault();
    setError('');
    try {
      await login(username.trim());
    } catch {
      setError('Invalid username. Please try again.');
    }
  };

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2">
      {/* Left side: Illustration or marketing */}
      <div className="hidden md:flex flex-col justify-center items-center bg-red-600 text-white p-10">
        <h1 className="text-5xl font-extrabold mb-4">Hungry Cow</h1>
        <p className="text-lg max-w-md text-center">
          Welcome back! Log in to order your favorite dishes, track previous orders, and more.
        </p>
        <img
          src={hungryCowImg}
          alt="Hungry Cow"
          className="mt-8 w-64 h-auto"
        />
      </div>

      {/* Right side: Form */}
      <div className="flex flex-col justify-center items-center bg-gray-50 p-6">
        <div className="w-full max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
          <div className="bg-white px-8 py-6 flex items-center justify-center">
            <LockClosedIcon className="h-8 w-8 text-red-600 mr-2" />
            <h2 className="text-2xl font-bold text-gray-800">Sign In</h2>
          </div>
          <form onSubmit={handleSubmit} className="px-8 py-6">
            {error && (
              <div className="bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-2 mb-4">
                {error}
              </div>
            )}
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-1">Username</label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                required
                placeholder="Enter your username"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400 transition"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 transition flex items-center justify-center"
            >
              <LockClosedIcon className="h-5 w-5 mr-2 text-white" />
              Sign In
            </button>
            <p className="mt-4 text-center text-gray-600">
              Don’t have an account?{' '}
              <span
                onClick={() => navigate('/signup')}
                className="text-red-600 hover:underline cursor-pointer"
              >
                Sign Up
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
