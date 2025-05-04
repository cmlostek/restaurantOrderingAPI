// src/components/Home.tsx

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

interface Dish {
  dish_id: number;
  dish: string;
  price: number;
  ingredients: number[];
  calories: number;
  category: string;
}

export default function Home() {
  const [menu, setMenu] = useState<Dish[]>([]);

  // fetch first few menu items for preview
  useEffect(() => {
    axios
      .get<Dish[]>("http://localhost:8000/menu/")
      .then((res) => setMenu(res.data.slice(0, 4)))
      .catch(console.error);
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero */}
      <section className="relative flex-grow overflow-hidden bg-gradient-to-br from-red-50 to-white py-28">
        <div className="absolute inset-0">
          <svg
            className="w-full h-full"
            xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="xMidYMid slice"
            viewBox="0 0 1463 360"
          >
            <defs>
              <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#fde68a" />
                <stop offset="100%" stopColor="#fca5a5" />
              </linearGradient>
            </defs>
            <path
              fill="url(#bgGrad)"
              fillOpacity="0.4"
              d="M0,64L80,90.7C160,117,320,171,480,186.7C640,203,800,181,960,170.7C1120,160,1280,160,1360,160L1463,160L1463,360L1360,360C1280,360,1120,360,960,360C800,360,640,360,480,360C320,360,160,360,80,360L0,360Z"
            />
          </svg>
        </div>
        <div className="relative z-10 container mx-auto px-6 md:px-12 text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold text-red-800 mb-4">
            Hungry Cow 🐄
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-gray-700 mb-8">
            Moo-licious meals made fresh for you! Browse our menu or place an order
            online for delivery or pickup.
          </p>
          <div className="space-x-4">
            <Link
              to="/menu"
              className="px-8 py-3 bg-red-600 text-white rounded-lg shadow hover:bg-red-700 transition transform hover:-translate-y-1"
            >
              View Menu
            </Link>
            <Link
              to="/order"
              className="px-8 py-3 border-2 border-red-600 text-red-600 bg-white rounded-lg shadow hover:bg-red-50 transition transform hover:-translate-y-1"
            >
              Place Order
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-6 md:px-12">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Why Choose Us
          </h2>
          <div className="grid gap-8 md:grid-cols-3">
            {[
              {
                icon: '🚀',
                title: 'Fast Delivery',
                desc: 'Get your food hot and fresh in record time.',
              },
              {
                icon: '🥗',
                title: 'Fresh Ingredients',
                desc: 'We use only the highest quality produce and meats.',
              },
              {
                icon: '💰',
                title: 'Great Value',
                desc: 'Delicious meals at prices you’ll love.',
              },
            ].map((f) => (
              <div key={f.title} className="text-center p-6 border rounded-lg hover:shadow-lg transition">
                <div className="text-4xl mb-4">{f.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
                <p className="text-gray-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Menu Preview */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-6 md:px-12">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Our Favorites
          </h2>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {menu.map((dish) => (
              <div key={dish.dish_id} className="bg-white rounded-lg overflow-hidden shadow hover:shadow-lg transition">
                <div className="h-32 bg-cover bg-center" style={{ backgroundImage: `url(/images/dish_${dish.dish_id}.jpg)` }} />
                <div className="p-4">
                  <h3 className="font-semibold text-lg mb-2">{dish.dish}</h3>
                  <p className="text-red-600 font-bold mb-2">${dish.price.toFixed(2)}</p>
                  <Link
                    to="/menu"
                    className="text-sm text-red-600 hover:underline"
                  >
                    View Full Menu
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-red-600 text-white py-8">
        <div className="container mx-auto px-6 md:px-12 text-center">
          <p className="mb-4">© {new Date().getFullYear()} Hungry Cow. All rights reserved.</p>
          <div className="space-x-4">
            <Link to="/" className="hover:underline">Home</Link>
            <Link to="/menu" className="hover:underline">Menu</Link>
            <Link to="/order" className="hover:underline">Order</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
