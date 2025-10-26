import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export interface User {
  user_id: number;
  username: string;
  user_role: 'admin' | 'customer' | string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) setUser(JSON.parse(stored));
  }, []);

  const login = async (username: string, password: string) => {
    try {
      // Call the login endpoint with username and password
      const res = await axios.post('http://localhost:8000/users/login', {
        username: username.trim(),
        password: password
      });
      
      const found = res.data;
      
      if (found) {
        setUser(found);
        localStorage.setItem('user', JSON.stringify(found));

        navigate(
          found.user_role.toLowerCase().trim() === 'admin' ? '/admin' : '/customer',
          {state: {message: `Welcome back, ${found.username}!`}}
        );
        return;
      }
      
      throw new Error('Login failed');
    } catch (error) {
      throw new Error('Invalid username or password');
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);