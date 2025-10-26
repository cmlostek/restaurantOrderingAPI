import React, { useEffect, useState, useMemo } from "react";
import axios from "axios";
import { useCart, CartItem } from "../context/CartContext";
import { useFavorites } from "../context/FavoritesContext";
import { MagnifyingGlassIcon, FunnelIcon } from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolid } from "@heroicons/react/24/solid";

interface Dish {
  dish_id: number;
  dish: string;
  price: number;
  ingredients: number[];
  calories: number;
  category: string;
}

interface Resource {
  resource_id: number;
  resource_name: string;
  resource_type: string;
  quantity_available: number;
}

const Menu: React.FC = () => {
  const [dishes, setDishes] = useState<Dish[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [maxPrice, setMaxPrice] = useState<number>(100);
  const [sortBy, setSortBy] = useState<string>("name");
  const [dietFilter, setDietFilter] = useState<string>("all");
  const [showFilters, setShowFilters] = useState(false);
  const { addToCart } = useCart();
  const { toggleFavorite, isFavorite } = useFavorites();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dishesRes, resourcesRes] = await Promise.all([
          axios.get("http://localhost:8000/menu"),
          axios.get("http://localhost:8000/resources")
        ]);

        setDishes(dishesRes.data);
        setResources(resourcesRes.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getIngredientNames = (ids: number[]) => {
    return ids.map(id => {
      const match = resources.find(res => res.resource_id === id);
      return match ? match.resource_name : "Unknown Ingredient";
    });
  };

  const handleAddToCart = (dish: Dish) => {
    const cartItem: CartItem = {
      dish_id: dish.dish_id,
      dish_name: dish.dish,
      price: dish.price,
      quantity: 1,
      category: dish.category
    };
    addToCart(cartItem);
  };

  // Memoized filtering logic
  const filteredDishes = useMemo(() => {
    let result = [...dishes];

    // Search filter
    if (searchTerm) {
      result = result.filter(dish =>
        dish.dish.toLowerCase().includes(searchTerm.toLowerCase()) ||
        getIngredientNames(dish.ingredients).some(ing =>
          ing.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Category filter
    if (selectedCategory !== "all") {
      result = result.filter(dish => dish.category === selectedCategory);
    }

    // Price filter
    result = result.filter(dish => dish.price <= maxPrice);

    // Dietary filters
    if (dietFilter !== "all") {
      result = result.filter(dish => {
        const ingredients = getIngredientNames(dish.ingredients).map(i => i.toLowerCase());
        if (dietFilter === "vegetarian") {
          const meatKeywords = ["chicken", "beef", "pork", "fish", "meat"];
          return !ingredients.some(ing => meatKeywords.some(keyword => ing.includes(keyword)));
        }
        if (dietFilter === "vegan") {
          const nonVeganKeywords = ["chicken", "beef", "pork", "fish", "meat", "cheese", "milk", "dairy"];
          return !ingredients.some(ing => nonVeganKeywords.some(keyword => ing.includes(keyword)));
        }
        if (dietFilter === "gluten-free") {
          return !ingredients.some(ing => ing.includes("wheat") || ing.includes("bread"));
        }
        return true;
      });
    }

    // Sorting
    result.sort((a, b) => {
      switch (sortBy) {
        case "price-low":
          return a.price - b.price;
        case "price-high":
          return b.price - a.price;
        case "calories-low":
          return a.calories - b.calories;
        case "calories-high":
          return b.calories - a.calories;
        case "name":
        default:
          return a.dish.localeCompare(b.dish);
      }
    });

    return result;
  }, [dishes, searchTerm, selectedCategory, maxPrice, sortBy, dietFilter, resources]);

  const categories = useMemo(
    () => ["all", ...Array.from(new Set(dishes.map(d => d.category)))],
    [dishes]
  );

  return (
    <section className="py-12 px-4 max-w-7xl mx-auto">
      <h2 className="text-4xl font-bold text-center text-red-600 mb-8">Our Menu</h2>

      {/* Search Bar */}
      <div className="mb-8 max-w-2xl mx-auto">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
          <input
            type="text"
            placeholder="Search dishes or ingredients..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 outline-none transition"
          />
        </div>
      </div>

      {/* Filter Controls */}
      <div className="mb-8 space-y-4">
        {/* Toggle Filters Button */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 text-gray-700 hover:text-red-600 transition"
        >
          <FunnelIcon className="h-5 w-5" />
          <span className="font-semibold">{showFilters ? "Hide" : "Show"} Filters</span>
        </button>

        {/* Advanced Filters */}
        {showFilters && (
          <div className="bg-white rounded-lg shadow p-6 grid md:grid-cols-3 gap-6">
            {/* Category Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Category</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 outline-none"
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            {/* Price Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Max Price: ${maxPrice.toFixed(2)}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                step="1"
                value={maxPrice}
                onChange={(e) => setMaxPrice(Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Sort Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 outline-none"
              >
                <option value="name">Name (A-Z)</option>
                <option value="price-low">Price (Low to High)</option>
                <option value="price-high">Price (High to Low)</option>
                <option value="calories-low">Calories (Low to High)</option>
                <option value="calories-high">Calories (High to Low)</option>
              </select>
            </div>

            {/* Dietary Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Dietary</label>
              <select
                value={dietFilter}
                onChange={(e) => setDietFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 outline-none"
              >
                <option value="all">All</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="gluten-free">Gluten-Free</option>
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Results Count */}
      {!loading && (
        <div className="mb-6 text-gray-600">
          Showing {filteredDishes.length} dish{filteredDishes.length !== 1 ? "es" : ""}
        </div>
      )}

      {loading ? (
        <p className="text-center text-gray-500">Loading menu...</p>
      ) : filteredDishes.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-xl text-gray-500">No dishes found matching your criteria.</p>
          <button
            onClick={() => {
              setSearchTerm("");
              setSelectedCategory("all");
              setMaxPrice(100);
              setDietFilter("all");
            }}
            className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDishes.map(dish => (
            <div
              key={dish.dish_id}
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition flex flex-col relative"
            >
              {/* Favorite Button */}
              <button
                onClick={() => toggleFavorite({
                  dish_id: dish.dish_id,
                  dish_name: dish.dish,
                  price: dish.price,
                  category: dish.category,
                  calories: dish.calories,
                  ingredients: dish.ingredients
                })}
                className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-600 transition"
              >
                {isFavorite(dish.dish_id) ? (
                  <HeartSolid className="h-6 w-6 text-red-600" />
                ) : (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                )}
              </button>
              
              <h3 className="text-2xl font-bold text-red-700 mb-2 pr-10">{dish.dish}</h3>
              <p className="text-sm text-gray-500 italic mb-2 capitalize">Category: {dish.category}</p>
              <p className="text-gray-600 mb-2">🔥 {dish.calories} calories</p>
              <p className="mb-4 text-sm text-gray-700">
                <span className="font-medium">Ingredients:</span>{" "}
                {getIngredientNames(dish.ingredients).join(", ")}
              </p>
              <div className="mt-auto pt-4 flex items-center justify-between border-t">
                <p className="text-2xl font-bold text-green-600">${dish.price.toFixed(2)}</p>
                <button
                  onClick={() => handleAddToCart(dish)}
                  className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 font-semibold transition"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default Menu;