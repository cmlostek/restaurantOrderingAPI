// src/App.tsx
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Menu from './components/Menu';
import Order from './components/Order';
import Team from './components/Team';
import Login from './components/Login';
import Signup from './components/SignUp';

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
    <AnimatePresence>

      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Home />
            </motion.div>
          }
        />
        <Route
          path="/menu"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Menu />
            </motion.div>
          }
        />
        <Route
          path="/order"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Order />
            </motion.div>
          }
        />
        <Route
          path="/team"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Team />
            </motion.div>
          }
        />
        {/* 🔥 Add these two back in: */}
        <Route
          path="/login"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Login />
            </motion.div>
          }
        />
        <Route
          path="/signup"
          element={
            <motion.div
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Signup />
            </motion.div>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}

const App: React.FC = () => (
  <Router>
    <div className="flex flex-col min-h-screen bg-gray-50 text-gray-800">
      <Header />

      <main className="">
        <AnimatedRoutes />
      </main>

      <Footer />
    </div>
  </Router>
);

export default App;