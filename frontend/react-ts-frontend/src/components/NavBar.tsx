// src/components/NavBar.tsx

import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

export default function NavBar() {
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const baseLinkClasses = 'text-lg font-medium transition';
  const activeClasses = 'text-red-600';
  const inactiveClasses = 'text-gray-700 hover:text-red-600';

  const renderLink = (to: string, label: string) => (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `${baseLinkClasses} ${isActive ? activeClasses : inactiveClasses}`
      }
      onClick={() => setMobileOpen(false)}
    >
      {label}
    </NavLink>
  );

  return (
    <header className="sticky top-0 bg-white shadow-md z-50">
      <div className="max-w-screen-xl mx-auto flex items-center justify-between px-6 py-4">
        {/* Logo & Title */}
        {renderLink('/', 'HungryCow')}

        {/* Desktop Nav Links */}
        <nav className="hidden lg:flex space-x-6">
          {renderLink('/', 'Home')}
          {renderLink('/menu', 'Menu')}
          {renderLink('/order', 'Order')}
          {renderLink('/team', 'Team')}
          {user?.user_role === 'customer' && renderLink('/customer', 'My Orders')}
          {user?.user_role === 'admin' && renderLink('/admin', 'Admin Dashboard')}
        </nav>

        {/* Auth Actions */}
        <div className="hidden lg:flex items-center space-x-4">
          {user ? (
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              Logout
            </button>
          ) : (
            <>
              <NavLink
                to="/login"
                className={({ isActive }) =>
                  `${baseLinkClasses} ${isActive ? activeClasses : inactiveClasses}`
                }
              >
                Login
              </NavLink>
              <NavLink
                to="/signup"
                className={({ isActive }) =>
                  `px-4 py-2 rounded-lg transition ${
                    isActive ? 'bg-red-600 text-white' : 'bg-red-600 text-white hover:bg-red-700'
                  }`
                }
              >
                Sign Up
              </NavLink>
            </>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          className="lg:hidden p-2 text-gray-700 hover:text-red-600"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}        
        </button>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileOpen && (
        <nav className="lg:hidden bg-white border-t px-6 py-4 space-y-3">
          {renderLink('/', 'Home')}
          {renderLink('/menu', 'Menu')}
          {renderLink('/order', 'Order')}
          {user?.user_role === 'customer' && renderLink('/customer', 'My Orders')}
          {user?.user_role === 'admin' && renderLink('/admin', 'Admin Dashboard')}
          <div className="pt-3 border-t">
            {user ? (
              <button
                onClick={() => { logout(); setMobileOpen(false); }}
                className="w-full text-left text-gray-700 hover:text-red-600 transition"
              >
                Logout
              </button>
            ) : (
              <>
                {renderLink('/login', 'Login')}
                {renderLink('/signup', 'Sign Up')}
              </>
            )}
          </div>
        </nav>
      )}
    </header>
  );
}
