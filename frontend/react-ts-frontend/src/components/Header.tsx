import React from "react";
import { Link } from "react-router-dom";

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto flex items-center justify-between p-4">
        <div className="text-2xl font-bold text-red-600">Hungry Cow</div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/" className="hover:text-red-500">Home</Link>
          </li>
          <li>
            <Link to="/menu" className="hover:text-red-500">Menu</Link>
          </li>
          <li>
            <Link to="/order" className="hover:text-red-500">Order</Link>
          </li>
          <li>
            <Link to="/team" className="hover:text-red-500">Meet the Team</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;