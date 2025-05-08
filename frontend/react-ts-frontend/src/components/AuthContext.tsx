import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export interface User {
  user_id: number;
  user_name: string;
  user_role: 'admin' | 'customer' | string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string) => Promise<void>;
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

  const login = async (username: string) => {
    // fetch all users, match by username
    const res = await axios.get<User[]>('http://localhost:8000/users/');
    const found = res.data.find(u => u.user_name === username)
    
    


    if (found) {
      
      setUser(found);
      localStorage.setItem('user', JSON.stringify(found));

      navigate(
        found.user_role.toLowerCase().trim() === 'admin' ? '/admin' : '/customer',
        {state: {message: `Welcome back, ${found.user_name}!`}}
      );

      return;
    }
    // if not found, redirect to signup
    navigate('/signup');
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