// src/pages/CustomerDashboard.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "./AuthContext";

interface Order {
  order_id: number;
  user_id: number | null;
  dish_id: number;
  order_date: string;
  total_price: number;
  is_guest: number;
}

interface Dish {
  dish_id: number;
  dish: string;
  price: number;
  category: string;
}

export default function CustomerDashboard() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [menu, setMenu] = useState<Dish[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    setLoading(true);
    Promise.all([
      axios.get<Order[]>("http://localhost:8000/orders/"),
      axios.get<Dish[]>("http://localhost:8000/menu/"),
    ])
      .then(([ordersRes, menuRes]) => {
        setOrders(ordersRes.data);
        setMenu(menuRes.data);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load your orders.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [user]);

  if (!user) return null; // should never happen behind ProtectedRoute

  const myOrders = orders.filter((o) => o.user_id === user.user_id);
  console.log(myOrders);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">My Orders</h1>

      {loading && <p>Loading your orders…</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && myOrders.length === 0 && (
        <p>You have no orders yet.</p>
      )}

      {!loading && !error && myOrders.length > 0 && (
        <table className="w-full table-auto bg-white border rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-3 py-2 text-left">Order ID</th>
              <th className="px-3 py-2 text-left">Dish</th>
              <th className="px-3 py-2 text-left">Date</th>
              <th className="px-3 py-2 text-left">Total</th>
            </tr>
          </thead>
          <tbody>
            {myOrders.map((o) => {
              const dish = menu.find((d) => d.dish_id === o.dish_id);
              return (
                <tr key={o.order_id} className="border-t">
                  <td className="px-3 py-2">{o.order_id}</td>
                  <td className="px-3 py-2">{dish?.dish ?? "Unknown"}</td>
                  <td className="px-3 py-2">
                    {new Date(o.order_date).toLocaleString()}
                  </td>
                  <td className="px-3 py-2">${o.total_price.toFixed(2)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}