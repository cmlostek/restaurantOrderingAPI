import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Types for your data
interface Order { order_id: number; user_id: number | null; dish_id: number; order_date: string; total_price: number; is_guest: number; }
interface Payment { payment_id: number; user_id: number; promotion_id: number | null; amount: number; created_at: string; }
interface Review { review_id: number; user_id: number | null; order_id: number; rating: number; comment: string; }

interface OverviewStats {
  total_users: number;
  total_orders: number;
  total_revenue: number;
  average_rating: number;
  today_orders: number;
  today_revenue: number;
}

interface TopDish {
  dish_id: number;
  dish_name: string;
  order_count: number;
  total_revenue: number;
}

interface TopCustomer {
  user_id: number;
  username: string;
  order_count: number;
  total_spent: number;
}

interface SalesTrend {
  date: string;
  revenue: number;
  order_count: number;
}

interface CategoryPerformance {
  category: string;
  revenue: number;
  order_count: number;
}

export default function AdminDashboard() {
  const [section, setSection] = useState<"analytics" | "orders" | "payments" | "reviews">("analytics");
  const [orders, setOrders] = useState<Order[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  
  // Analytics state
  const [overviewStats, setOverviewStats] = useState<OverviewStats | null>(null);
  const [topDishes, setTopDishes] = useState<TopDish[]>([]);
  const [topCustomers, setTopCustomers] = useState<TopCustomer[]>([]);
  const [salesTrends, setSalesTrends] = useState<SalesTrend[]>([]);
  const [categoryPerformance, setCategoryPerformance] = useState<CategoryPerformance[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch analytics data
  useEffect(() => {
    if (section === "analytics") {
      setLoading(true);
      Promise.all([
        axios.get<OverviewStats>("http://localhost:8000/analytics/overview"),
        axios.get<TopDish[]>("http://localhost:8000/analytics/top-dishes?limit=10"),
        axios.get<TopCustomer[]>("http://localhost:8000/analytics/top-customers?limit=10"),
        axios.get<SalesTrend[]>("http://localhost:8000/analytics/sales-trends?days=7"),
        axios.get<CategoryPerformance[]>("http://localhost:8000/analytics/category-performance"),
      ])
        .then(([overviewRes, dishesRes, customersRes, trendsRes, categoriesRes]) => {
          setOverviewStats(overviewRes.data);
          setTopDishes(dishesRes.data);
          setTopCustomers(customersRes.data);
          setSalesTrends(trendsRes.data);
          setCategoryPerformance(categoriesRes.data);
        })
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [section]);

  // Fetch other sections
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
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-4xl font-bold mb-6 text-gray-800">Admin Dashboard</h1>
      
      <div className="flex space-x-4 mb-6">
        {(["analytics", "orders", "payments", "reviews"] as const).map(s => (
          <button
            key={s}
            onClick={() => setSection(s)}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              section === s 
                ? "bg-red-600 text-white shadow-lg" 
                : "bg-white text-gray-700 hover:bg-gray-100"
            }`}
          >
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      {/* Analytics Section */}
      {section === "analytics" && (
        <div className="space-y-6">
          {loading ? (
            <p className="text-center py-12">Loading analytics...</p>
          ) : (
            <>
              {/* Overview Stats Cards */}
              {overviewStats && (
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Total Users</div>
                    <div className="text-3xl font-bold text-gray-900">{overviewStats.total_users}</div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Total Orders</div>
                    <div className="text-3xl font-bold text-gray-900">{overviewStats.total_orders}</div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Total Revenue</div>
                    <div className="text-3xl font-bold text-green-600">${overviewStats.total_revenue.toFixed(2)}</div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Avg Rating</div>
                    <div className="text-3xl font-bold text-yellow-500">{overviewStats.average_rating.toFixed(1)}</div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Today's Orders</div>
                    <div className="text-3xl font-bold text-blue-600">{overviewStats.today_orders}</div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-4">
                    <div className="text-gray-600 text-sm font-medium">Today's Revenue</div>
                    <div className="text-3xl font-bold text-green-600">${overviewStats.today_revenue.toFixed(2)}</div>
                  </div>
                </div>
              )}

              {/* Sales Trends */}
              {salesTrends.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-2xl font-bold mb-4 text-gray-800">Sales Trends (Last 7 Days)</h2>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={salesTrends.map(t => ({
                        date: new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                        revenue: t.revenue,
                        orders: t.order_count
                      }))}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                        <Legend />
                        <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={3} name="Revenue ($)" />
                        <Line yAxisId="right" type="monotone" dataKey="orders" stroke="#3b82f6" strokeWidth={3} name="Orders" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {/* Top Dishes */}
              {topDishes.length > 0 && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-2xl font-bold mb-4 text-gray-800">Top Selling Dishes (Revenue)</h2>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={topDishes.slice(0, 8).map(d => ({
                          name: d.dish_name.length > 15 ? d.dish_name.substring(0, 12) + '...' : d.dish_name,
                          revenue: d.total_revenue
                        }))}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                          <YAxis />
                          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                          <Bar dataKey="revenue" fill="#10b981" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-2xl font-bold mb-4 text-gray-800">Top Selling Dishes (Orders)</h2>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={topDishes.slice(0, 8).map(d => ({
                          name: d.dish_name.length > 15 ? d.dish_name.substring(0, 12) + '...' : d.dish_name,
                          orders: d.order_count
                        }))}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="orders" fill="#3b82f6" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              )}

              {/* Top Customers */}
              {topCustomers.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-2xl font-bold mb-4 text-gray-800">Top Customers by Spending</h2>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={topCustomers.slice(0, 10).map(c => ({
                        name: c.username.length > 10 ? c.username.substring(0, 8) + '...' : c.username,
                        spent: c.total_spent,
                        orders: c.order_count
                      }))}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                        <YAxis />
                        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                        <Legend />
                        <Bar dataKey="spent" fill="#10b981" name="Total Spent ($)" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {/* Category Performance */}
              {categoryPerformance.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-2xl font-bold mb-4 text-gray-800">Category Performance</h2>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={categoryPerformance.map(cat => ({
                            category: cat.category,
                            revenue: cat.revenue
                          }))}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={(entry: any) => `${entry.category}: $${entry.revenue.toFixed(0)}`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="revenue"
                        >
                          {categoryPerformance.map((_, index) => {
                            const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
                            return <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />;
                          })}
                        </Pie>
                        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Orders Section */}
      {section === "orders" && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left">ID</th>
                <th className="px-4 py-3 text-left">User</th>
                <th className="px-4 py-3 text-left">Dish</th>
                <th className="px-4 py-3 text-left">Date</th>
                <th className="px-4 py-3 text-right">Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.order_id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-3">{o.order_id}</td>
                  <td className="px-4 py-3">{o.user_id ?? 'Guest'}</td>
                  <td className="px-4 py-3">{o.dish_id}</td>
                  <td className="px-4 py-3">{new Date(o.order_date).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right">${o.total_price.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Payments Section */}
      {section === "payments" && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left">Payment ID</th>
                <th className="px-4 py-3 text-left">User</th>
                <th className="px-4 py-3 text-left">Promotion</th>
                <th className="px-4 py-3 text-right">Amount</th>
                <th className="px-4 py-3 text-left">Date</th>
              </tr>
            </thead>
            <tbody>
              {payments.map(p => (
                <tr key={p.payment_id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-3">{p.payment_id}</td>
                  <td className="px-4 py-3">{p.user_id}</td>
                  <td className="px-4 py-3">{p.promotion_id ?? '—'}</td>
                  <td className="px-4 py-3 text-right font-semibold text-green-600">${p.amount.toFixed(2)}</td>
                  <td className="px-4 py-3">{new Date(p.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Reviews Section */}
      {section === "reviews" && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left">Review ID</th>
                <th className="px-4 py-3 text-left">User</th>
                <th className="px-4 py-3 text-left">Order ID</th>
                <th className="px-4 py-3 text-center">Rating</th>
                <th className="px-4 py-3 text-left">Comment</th>
              </tr>
            </thead>
            <tbody>
              {reviews.map(r => (
                <tr key={r.review_id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-3">{r.review_id}</td>
                  <td className="px-4 py-3">{r.user_id ?? '—'}</td>
                  <td className="px-4 py-3">{r.order_id}</td>
                  <td className="px-4 py-3 text-center">
                    <span className="text-yellow-500 font-bold">{r.rating}⭐</span>
                  </td>
                  <td className="px-4 py-3">{r.comment}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}