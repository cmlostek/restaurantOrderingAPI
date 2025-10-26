import React, { useState } from "react";
import { useFavorites, Favorite } from "../context/FavoritesContext";
import { useCart } from "../context/CartContext";
import { HeartIcon, ShoppingCartIcon } from "@heroicons/react/24/solid";
import { HeartIcon as HeartOutline } from "@heroicons/react/24/outline";

const Favorites: React.FC = () => {
  const { favorites, toggleFavorite } = useFavorites();
  const { addToCart } = useCart();
  const [loading, setLoading] = useState(false);

  const handleQuickOrder = async (favorite: Favorite) => {
    setLoading(true);
    try {
      // Add to cart
      addToCart({
        dish_id: favorite.dish_id,
        dish_name: favorite.dish_name,
        price: favorite.price,
        quantity: 1,
        category: favorite.category
      });
      
      // Show success message (you could use a toast library here)
      alert(`${favorite.dish_name} added to cart!`);
    } catch (error) {
      console.error("Error adding to cart:", error);
    } finally {
      setLoading(false);
    }
  };

  if (favorites.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
        <div className="text-center">
          <HeartOutline className="h-24 w-24 text-gray-300 mx-auto mb-4" />
          <h2 className="text-4xl font-bold text-gray-800 mb-4">No Favorites Yet</h2>
          <p className="text-gray-600 mb-8">Start adding dishes to your favorites from the menu!</p>
          <a
            href="/menu"
            className="bg-red-600 text-white px-8 py-3 rounded-lg hover:bg-red-700 font-semibold transition inline-block"
          >
            Browse Menu
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 flex items-center gap-3">
              <HeartIcon className="h-10 w-10 text-red-600" />
              My Favorites
            </h1>
            <p className="text-gray-600 mt-2">{favorites.length} saved {favorites.length === 1 ? 'dish' : 'dishes'}</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map((favorite) => (
            <div
              key={favorite.dish_id}
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition flex flex-col"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-2xl font-bold text-red-700 flex-1">{favorite.dish_name}</h3>
                <button
                  onClick={() => toggleFavorite(favorite)}
                  className="ml-2 text-red-600 hover:text-red-800 transition"
                >
                  <HeartIcon className="h-6 w-6" />
                </button>
              </div>
              
              <p className="text-sm text-gray-500 italic mb-2 capitalize">Category: {favorite.category}</p>
              <p className="text-gray-600 mb-2">🔥 {favorite.calories} calories</p>
              
              <div className="mt-auto pt-4 flex items-center justify-between border-t">
                <p className="text-2xl font-bold text-green-600">${favorite.price.toFixed(2)}</p>
                <button
                  onClick={() => handleQuickOrder(favorite)}
                  disabled={loading}
                  className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 font-semibold transition disabled:opacity-50 flex items-center gap-2"
                >
                  <ShoppingCartIcon className="h-5 w-5" />
                  Quick Order
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="mt-12 bg-white rounded-lg shadow p-6">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">Quick Actions</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <button
              onClick={() => {
                favorites.forEach(fav => {
                  addToCart({
                    dish_id: fav.dish_id,
                    dish_name: fav.dish_name,
                    price: fav.price,
                    quantity: 1,
                    category: fav.category
                  });
                });
                alert(`Added all ${favorites.length} favorites to cart!`);
              }}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold transition"
            >
              Add All to Cart
            </button>
            <a
              href="/menu"
              className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 font-semibold transition text-center"
            >
              Browse More Dishes
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Favorites;
