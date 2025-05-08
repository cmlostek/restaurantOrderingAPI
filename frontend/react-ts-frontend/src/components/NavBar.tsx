// src/components/NavBar.tsx
import { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const links = [
  { to: '/',    label: 'Home' },
  { to: '/menu',   label: 'Menu' },
  { to: '/order',  label: 'Order' },
  { to: '/team',   label: 'Meet the Team' },
];

export default function NavBar() {
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `block px-3 py-2 rounded-md text-base font-medium transition ${
      isActive
        ? 'text-red-600 bg-red-50'
        : 'text-gray-700 hover:text-red-600 hover:bg-red-50'
    }`;

  return (
    <nav className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Brand */}
          <Link to="/" className="text-2xl font-bold text-red-600">
            Hungry Cow
          </Link>

          {/* Desktop Links */}
          <div className="hidden md:flex md:space-x-4 md:items-center">
            {links.map(({ to, label }) => (
              <NavLink key={to} to={to} className={linkClasses}>
                {label}
              </NavLink>
            ))}

            {/* role‐based dashboards */}
            {user?.user_role === 'customer' && (
              <NavLink to="/customer" className={linkClasses}>
                My Orders
              </NavLink>
            )}
            {user?.user_role === 'admin' && (
              <NavLink to="/admin" className={linkClasses}>
                Admin Dashboard
              </NavLink>
            )}
          </div>

          {/* Auth buttons desktop */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            {user ? (
              <button
                onClick={logout}
                className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-red-600 transition"
              >
                Logout
              </button>
            ) : (
              <>
                <NavLink
                  to="/login"
                  className="text-sm font-medium text-gray-700 hover:text-red-600 transition"
                >
                  Login
                </NavLink>
                <NavLink
                  to="/signup"
                  className="px-3 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 transition"
                >
                  Sign Up
                </NavLink>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 inline-flex items-center justify-center text-gray-700 hover:text-red-600 focus:outline-none"
            >
              {mobileOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {links.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={linkClasses}
                onClick={() => setMobileOpen(false)}
              >
                {label}
              </NavLink>
            ))}

            {/* role‐based dashboards */}
            {user?.user_role === 'customer' && (
              <NavLink
                to="/customer"
                className={linkClasses}
                onClick={() => setMobileOpen(false)}
              >
                My Orders
              </NavLink>
            )}
            {user?.user_role === 'admin' && (
              <NavLink
                to="/admin"
                className={linkClasses}
                onClick={() => setMobileOpen(false)}
              >
                Admin Dashboard
              </NavLink>
            )}

            {user ? (
              <button
                onClick={() => {
                  logout();
                  setMobileOpen(false);
                }}
                className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 transition"
              >
                Logout
              </button>
            ) : (
              <>
                <NavLink
                  to="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 transition"
                  onClick={() => setMobileOpen(false)}
                >
                  Login
                </NavLink>
                <NavLink
                  to="/signup"
                  className="block px-3 py-2 rounded-md text-base font-medium bg-red-600 text-white hover:bg-red-700 transition"
                  onClick={() => setMobileOpen(false)}
                >
                  Sign Up
                </NavLink>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}