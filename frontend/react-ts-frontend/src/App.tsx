// src/App.tsx
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

import { AuthProvider } from './components/AuthContext';

import Header            from './components/Header';
import Footer            from './components/Footer';
import Home              from './components/Home';
import Menu              from './components/Menu';
import Order             from './components/Order';
import Team              from './components/Team';
import Login             from './components/Login';
import SignUp            from './components/SignUp';
import CustomerDashboard from './components/CustomerDashboard';
import AdminDashboard    from './components/AdminDashboard';

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  in:      { opacity: 1, y: 0 },
  out:     { opacity: 0, y: -20 },
};
const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.5,
};

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/"      element={<PageWrapper><Home/></PageWrapper>} />
        <Route path="/menu"  element={<PageWrapper><Menu/></PageWrapper>} />
        <Route path="/order" element={<PageWrapper><Order/></PageWrapper>} />
        <Route path="/team"  element={<PageWrapper><Team/></PageWrapper>} />

        {/* auth */}
        <Route path="/login"  element={<PageWrapper><Login/></PageWrapper>} />
        <Route path="/signup" element={<PageWrapper><SignUp/></PageWrapper>} />

        {/* dashboards */}
        <Route
          path="/customer"
          element={<PageWrapper><CustomerDashboard/></PageWrapper>}
        />
        <Route
          path="/admin"
          element={<PageWrapper><AdminDashboard/></PageWrapper>}
        />

        {/* fallback */}
        <Route path="*" element={<PageWrapper><Home/></PageWrapper>} />
      </Routes>
    </AnimatePresence>
  );
}

function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={pageTransition}
      className="w-full h-full"
    >
      {children}
    </motion.div>
  );
}

const App: React.FC = () => (
  <Router>
    <AuthProvider>
      <div className="flex flex-col min-h-screen bg-gray-50 text-gray-800">
        <Header />

        <main className="flex-grow w-full">
          <AnimatedRoutes />
        </main>

        <Footer />
      </div>
    </AuthProvider>
  </Router>
);

export default App;