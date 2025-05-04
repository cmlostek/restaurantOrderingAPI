import React, { useEffect, useState } from "react";
import axios from "axios";

// Types for your data
interface Order { order_id: number; user_id: number | null; dish_id: number; order_date: string; total_price: number; is_guest: number; }
interface Payment { payment_id: number; user_id: number; promotion_id: number | null; amount: number; created_at: string; }
interface Review { review_id: number; user_id: number | null; order_id: number; rating: number; comment: string; }

export default function AdminDashboard() {
  const [section, setSection] = useState<"orders" | "payments" | "reviews">("orders");
  const [orders, setOrders] = useState<Order[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);

  // Fetch data based on section
  useEffect(() => {
    if (section === "orders") {
      axios.get<Order[]>("http://localhost:8000/orders/")
        .then(r => setOrders(r.data))
        .catch(console.error);
    } else if (section === "payments") {
      axios.get<Payment[]>("http://localhost:8000/payments/")
        .then(r => setPayments(r.data))
        .catch(console.error);
    } else if (section === "reviews") {
      axios.get<Review[]>("http://localhost:8000/reviews/")
        .then(r => setReviews(r.data))
        .catch(console.error);
    }
  }, [section]);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Admin Dashboard</h1>
      <div className="flex space-x-4 mb-6">
        {(["orders", "payments", "reviews"] as const).map(s => (
          <button
            key={s}
            onClick={() => setSection(s)}
            className={`px-4 py-2 rounded ${section === s ? "bg-red-600 text-white" : "bg-gray-200"}`}
          >
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {section === "orders" && (
        <table className="w-full table-auto bg-white border rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-2 py-1">ID</th>
              <th className="px-2 py-1">User</th>
              <th className="px-2 py-1">Dish</th>
              <th className="px-2 py-1">Date</th>
              <th className="px-2 py-1">Total</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.order_id} className="border-t">
                <td className="px-2 py-1">{o.order_id}</td>
                <td className="px-2 py-1">{o.user_id ?? 'Guest'}</td>
                <td className="px-2 py-1">{o.dish_id}</td>
                <td className="px-2 py-1">{new Date(o.order_date).toLocaleString()}</td>
                <td className="px-2 py-1">${o.total_price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {section === "payments" && (
        <table className="w-full table-auto bg-white border rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-2 py-1">Payment ID</th>
              <th className="px-2 py-1">User</th>
              <th className="px-2 py-1">Promotion</th>
              <th className="px-2 py-1">Amount</th>
              <th className="px-2 py-1">Date</th>
            </tr>
          </thead>
          <tbody>
            {payments.map(p => (
              <tr key={p.payment_id} className="border-t">
                <td className="px-2 py-1">{p.payment_id}</td>
                <td className="px-2 py-1">{p.user_id}</td>
                <td className="px-2 py-1">{p.promotion_id ?? '—'}</td>
                <td className="px-2 py-1">${p.amount.toFixed(2)}</td>
                <td className="px-2 py-1">{new Date(p.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {section === "reviews" && (
        <table className="w-full table-auto bg-white border rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-2 py-1">Review ID</th>
              <th className="px-2 py-1">User</th>
              <th className="px-2 py-1">Order ID</th>
              <th className="px-2 py-1">Rating</th>
              <th className="px-2 py-1">Comment</th>
            </tr>
          </thead>
          <tbody>
            {reviews.map(r => (
              <tr key={r.review_id} className="border-t">
                <td className="px-2 py-1">{r.review_id}</td>
                <td className="px-2 py-1">{r.user_id ?? '—'}</td>
                <td className="px-2 py-1">{r.order_id}</td>
                <td className="px-2 py-1">{r.rating}</td>
                <td className="px-2 py-1">{r.comment}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}