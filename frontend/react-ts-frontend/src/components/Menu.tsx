import React, { useEffect, useState } from "react";
import axios from "axios";

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

  return (
    <section className="py-12 px-4">
      <h2 className="text-4xl font-bold text-center text-red-600 mb-8">Our Menu</h2>
      {loading ? (
        <p className="text-center text-gray-500">Loading menu...</p>
      ) : (
        <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {dishes.map(dish => (
            <div
              key={dish.dish_id}
              className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
            >
              <h3 className="text-2xl font-semibold text-red-700 mb-1">{dish.dish}</h3>
              <p className="text-sm text-gray-500 italic mb-2">Category: {dish.category}</p>
              <p className="text-gray-600 mb-2">Calories: {dish.calories}</p>
              <p className="mb-2">
                <span className="font-medium">Ingredients:</span>{" "}
                {getIngredientNames(dish.ingredients).join(", ")}
              </p>
              <p className="text-lg font-bold text-red-600">${dish.price.toFixed(2)}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default Menu;
