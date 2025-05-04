import React, { useState } from "react";
import Header from "./components/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Menu from "./components/Menu";
import Order from "./components/Order";

const App: React.FC = () => {
  return (
    <Router>
      <div className="font-sans min-h-screen bg-gray-50 text-gray-800">
        <Header />
        <main className="container mx-auto p-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/menu" element={<Menu />} />
            <Route path="/order" element={<Order />} />
            {/* <Route path="/team" element={<Team />} /> */}
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;