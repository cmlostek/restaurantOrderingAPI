import React, { useState } from "react";
import axios from "axios";
import { useCart } from "../context/CartContext";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

const Cart: React.FC = () => {
  const { cart, removeFromCart, updateQuantity, clearCart, getTotalPrice, getTotalItems } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleCheckout = async () => {
    if (!user) {
      navigate("/login");
      return;
    }

    if (cart.length === 0) {
      setError("Your cart is empty!");
      return;
    }

    setIsCheckingOut(true);
    setError(null);

    try {
      // Create orders for each cart item
      const orderPromises = cart.map(item =>
        axios.post("http://localhost:8000/orders/", {
          user_id: user.user_id,
          dish_id: item.dish_id,
          order_date: new Date().toISOString(),
          total_price: (item.price * item.quantity).toFixed(2),
          is_guest: 0
        })
      );

      await Promise.all(orderPromises);
      
      // Clear cart and show success
      clearCart();
      setSuccess(true);
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        setSuccess(false);
        navigate(user.user_role === "admin" ? "/admin" : "/customer");
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to place order. Please try again.");
    } finally {
      setIsCheckingOut(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Your Cart is Empty</h2>
          <p className="text-gray-600 mb-8">Add some delicious items from our menu!</p>
          <button
            onClick={() => navigate("/menu")}
            className="bg-red-600 text-white px-8 py-3 rounded-lg hover:bg-red-700 font-semibold transition"
          >
            Browse Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">Shopping Cart</h1>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-3 mb-6 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-100 border-l-4 border-green-500 text-green-700 px-4 py-3 mb-6 rounded">
            ✅ Order placed successfully! Redirecting...
          </div>
        )}

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b">
                <h2 className="text-2xl font-bold">Cart Items ({getTotalItems()})</h2>
              </div>
              <div className="divide-y">
                {cart.map(item => (
                  <div key={item.dish_id} className="p-6 flex items-center justify-between hover:bg-gray-50 transition">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-800">{item.dish_name}</h3>
                      <p className="text-sm text-gray-500 capitalize">{item.category}</p>
                      <p className="text-lg font-bold text-green-600 mt-2">
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="flex items-center border rounded-lg">
                        <button
                          onClick={() => updateQuantity(item.dish_id, item.quantity - 1)}
                          className="px-3 py-1 hover:bg-gray-100"
                          disabled={item.quantity <= 1}
                        >
                          −
                        </button>
                        <span className="px-4 py-1 min-w-[3rem] text-center font-semibold">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => updateQuantity(item.dish_id, item.quantity + 1)}
                          className="px-3 py-1 hover:bg-gray-100"
                        >
                          +
                        </button>
                      </div>
                      
                      <button
                        onClick={() => removeFromCart(item.dish_id)}
                        className="text-red-600 hover:text-red-800 font-bold text-xl"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-6">
              <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal ({getTotalItems()} items)</span>
                  <span className="font-semibold">${getTotalPrice().toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Tax</span>
                  <span className="font-semibold">${(getTotalPrice() * 0.08).toFixed(2)}</span>
                </div>
                <div className="border-t pt-4">
                  <div className="flex justify-between text-xl font-bold">
                    <span>Total</span>
                    <span className="text-green-600">${(getTotalPrice() * 1.08).toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {!user ? (
                <>
                  <p className="text-sm text-gray-600 mb-4">Please login to checkout</p>
                  <button
                    onClick={() => navigate("/login")}
                    className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 font-semibold transition mb-2"
                  >
                    Login to Checkout
                  </button>
                </>
              ) : (
                <button
                  onClick={handleCheckout}
                  disabled={isCheckingOut}
                  className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCheckingOut ? "Processing..." : "Proceed to Checkout"}
                </button>
              )}

              <button
                onClick={clearCart}
                className="w-full mt-2 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 font-semibold transition"
              >
                Clear Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
