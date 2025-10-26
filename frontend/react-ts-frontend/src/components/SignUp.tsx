// src/components/SignUp.tsx

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function SignUp() {
  const [username,    setUsername]    = useState('');
  const [password,    setPassword]    = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email,       setEmail]       = useState('');
  const [phone,       setPhone]       = useState('');
  const [address,     setAddress]     = useState('');
  const [role,        setRole]        = useState<'customer'|'staff'|'admin'>('customer');
  const [paymentInfo, setPaymentInfo] = useState<'card'|'paypal'|'internal'>('card');
  const [review,      setReview]      = useState('');
  const [rating,      setRating]      = useState(5);
  const [error,       setError]       = useState('');
  const [success,     setSuccess]     = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    // Validate password length
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    try {
      await axios.post('http://localhost:8000/users/', {
        username:     username,
        password:     password,
        email,
        phone_number: phone,
        address,
        user_role:    role,
        payment_info: paymentInfo,
        review,
        rating:       rating.toString(),
      });
      setSuccess('🎉 Account created successfully! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Signup failed. Please check your input and try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center p-6">
      <div className="max-w-xl w-full bg-white shadow-2xl rounded-xl overflow-hidden">
        {/* Header */}
        <div className="bg-red-600 px-8 py-6 text-white">
          <h2 className="text-4xl font-extrabold tracking-tight">Sign Up</h2>
          <p className="mt-1 text-red-200">Create your free account to start ordering</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="px-8 py-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {error && (
            <div className="col-span-2 bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-2">
              {error}
            </div>
          )}
          {success && (
            <div className="col-span-2 bg-green-100 border-l-4 border-green-500 text-green-700 px-4 py-2">
              {success}
            </div>
          )}

          <div className="col-span-2">
            <label className="block text-gray-800 font-semibold mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
              placeholder="Enter your username"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              required
              placeholder="Confirm your password"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Phone</label>
            <input
              type="tel"
              value={phone}
              onChange={e => setPhone(e.target.value)}
              placeholder="(123) 456-7890"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div className="col-span-2">
            <label className="block text-gray-800 font-semibold mb-1">Address</label>
            <input
              type="text"
              value={address}
              onChange={e => setAddress(e.target.value)}
              placeholder="123 Main St, City, State"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Role</label>
            <select
              value={role}
              onChange={e => setRole(e.target.value as any)}
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            >
              <option value="customer">Customer</option>
              <option value="staff">Staff</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Payment Method</label>
            <select
              value={paymentInfo}
              onChange={e => setPaymentInfo(e.target.value as any)}
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            >
              <option value="card">Credit Card</option>
              <option value="paypal">PayPal</option>
              <option value="internal">Internal</option>
            </select>
          </div>

          <div className="col-span-2">
            <label className="block text-gray-800 font-semibold mb-1">Review</label>
            <textarea
              value={review}
              onChange={e => setReview(e.target.value)}
              rows={4}
              placeholder="Share your thoughts (optional)"
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition resize-y"
            />
          </div>

          <div>
            <label className="block text-gray-800 font-semibold mb-1">Rating</label>
            <input
              type="number"
              min={1}
              max={5}
              value={rating}
              onChange={e => setRating(Number(e.target.value))}
              className="w-full rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 px-4 py-2 transition"
            />
          </div>

          <div className="col-span-2 text-center mt-4">
            <button
              type="submit"
              disabled={!!success}
              className="w-3/4 md:w-1/2 bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-full transition disabled:opacity-50"
            >
              {success ? 'Redirecting...' : 'Create Account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
