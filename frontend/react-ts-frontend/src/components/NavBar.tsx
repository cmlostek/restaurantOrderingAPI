import { Link } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function NavBar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white border-b p-4 flex justify-between items-center">
      <div className="flex space-x-4">
        <Link to="/" className="text-lg font-semibold hover:text-red-600">Home</Link>
        <Link to="/menu" className="text-lg font-semibold hover:text-red-600">Menu</Link>
        <Link to="/order" className="text-lg font-semibold hover:text-red-600">Order</Link>
        {user?.user_role === "customer" && (
          <Link to="/customer" className="text-lg font-semibold hover:text-red-600">My Orders</Link>
        )}
        {user?.user_role === "admin" && (
          <Link to="/admin" className="text-lg font-semibold hover:text-red-600">Admin Dashboard</Link>
        )}
      </div>
      <div>
        {user ? (
          <button
            onClick={logout}
            className="text-sm text-gray-600 hover:text-gray-800"
          >
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" className="text-sm text-gray-600 hover:text-gray-800 mr-4">Login</Link>
            <Link to="/signup" className="text-sm text-gray-600 hover:text-gray-800">Sign Up</Link>
          </>
        )}
      </div>
    </nav> 
    );
}