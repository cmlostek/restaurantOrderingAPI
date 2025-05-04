
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "./AuthContext";

interface Dish {
  dish_id: number;
  dish: string;
  price: number;
  category: string;
}

interface Promotion {
  promotion_id: number;
  code: string;
  discount_percentage: number;
  valid_until: string;
}

interface Receipt {
  order_id: number;
  dishName: string;
  originalPrice: number;
  discountPercent: number;
  totalPaid: number;
  promoCode?: string;
  note?: string;
  status: string;
}

export default function OrderPage() {
  const [menu, setMenu] = useState<Dish[]>([]);
  const [promos, setPromos] = useState<Promotion[]>([]);
  const [selectedDishId, setSelectedDishId] = useState<number | null>(null);
  const [promoCode, setPromoCode] = useState<string>("");
  const [note, setNote] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [message, setMessage] = useState<string>("");
  const {user} = useAuth();

  useEffect(() => {
    // load menu
    axios
      .get<Dish[]>("http://localhost:8000/menu/")
      .then((r) => setMenu(r.data))
      .catch(() => setMessage("Failed to load menu."));
    // load promotions
    axios
      .get<Promotion[]>("http://localhost:8000/promotions/")
      .then((r) => setPromos(r.data))
      .catch(() => {}); // optional
  }, []);

  const handleSubmit = async () => {
    if (selectedDishId === null) {
      setMessage("Please select a dish first.");
      return;
    }

    setLoading(true);
    setMessage("");

    // find dish
    const dish = menu.find((d) => d.dish_id === selectedDishId)!;
    let finalPrice = dish.price;
    let discountPercent = 0;
    let appliedCode: string | undefined;

    // apply promo if any
    if (promoCode.trim()) {
      const match = promos.find(
        (p) => p.code.toLowerCase() === promoCode.trim().toLowerCase()
      );
      if (match) {
        discountPercent = match.discount_percentage;
        appliedCode = match.code;
        finalPrice = finalPrice * (1 - discountPercent / 100);
      } else {
        setMessage("Promo code invalid, proceeding without discount.");
      }
    }

    const userId = user ? user.user_id : null;
    try {
      // 1) create order
      const orderRes = await axios.post("http://localhost:8000/orders/", {
        user_id:  userId,
        dish_id: selectedDishId,
        order_date: new Date().toISOString(),
        total_price: parseFloat(finalPrice.toFixed(2)),
        is_guest: 1,
      });
      const orderId = orderRes.data.order_id;

      // 2) create order detail
      await axios.post(
        `http://localhost:8000/orders/${orderId}/details/`,
        {
          order_id: orderId,
          dish_id: selectedDishId,
          payment_id: 1,
          order_details: note.trim() || "No special instructions", 
          order_status: "Pending",
        }
      );

      // 3) show receipt
      setReceipt({
        order_id: orderId,
        dishName: dish.dish,
        originalPrice: dish.price,
        discountPercent,
        totalPaid: parseFloat(finalPrice.toFixed(2)),
        promoCode: appliedCode,
        note: note.trim() || undefined,
        status: "Pending",
      });
    } catch (err) {
      console.error(err);
      setMessage("Failed to place order. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (receipt) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
        <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full text-center">
          <h2 className="text-2xl font-bold mb-4 text-green-600">
            🎉 Order Confirmed!
          </h2>
          <p className="mb-2">
            <strong>Order ID:</strong> {receipt.order_id}
          </p>
          <p className="mb-2">
            <strong>Dish:</strong> {receipt.dishName}
          </p>
          <p className="mb-2">
            <strong>Original Price:</strong> ${receipt.originalPrice.toFixed(2)}
          </p>
          {receipt.promoCode && (
            <>
              <p className="mb-2">
                <strong>Promo:</strong> {receipt.promoCode} (
                {receipt.discountPercent}%)
              </p>
            </>
          )}
          <p className="mb-4">
            <strong>Total Paid:</strong> ${receipt.totalPaid.toFixed(2)}
          </p>
          {receipt.note && (
            <p className="italic mb-4">Note: {receipt.note}</p>
          )}
          <p className="text-sm text-gray-600">
            Status: <strong>{receipt.status}</strong>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-10">
      <h1 className="text-3xl md:text-5xl font-bold text-red-600 text-center mb-8">
        Place Your Order
      </h1>

      {message && (
        <div className="max-w-md mx-auto text-center text-red-600 mb-6">
          {message}
        </div>
      )}

      <div className="max-w-3xl mx-auto grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
        {menu.map((d) => (
          <button
            key={d.dish_id}
            onClick={() => setSelectedDishId(d.dish_id)}
            className={`border-2 p-4 rounded-lg transition ${
              selectedDishId === d.dish_id
                ? "border-red-500 bg-red-100"
                : "border-gray-300 hover:border-red-400"
            }`}
          >
            <h2 className="font-semibold text-lg">{d.dish}</h2>
            <p className="text-red-600 font-medium">${d.price.toFixed(2)}</p>
          </button>
        ))}
      </div>

      <div className="max-w-3xl mx-auto space-y-4">
        <input
          type="text"
          placeholder="Enter promo code (optional)"
          value={promoCode}
          onChange={(e) => setPromoCode(e.target.value)}
          className="w-full border border-gray-300 rounded-md px-4 py-2"
        />

        <textarea
          placeholder="Add a note or customization (optional)"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          rows={3}
          className="w-full border border-gray-300 rounded-md px-4 py-2 resize-none"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className={`w-full py-3 rounded-lg text-white font-semibold transition ${
            loading ? "bg-red-200" : "bg-red-500 hover:bg-red-600"
          }`}
        >
          {loading ? "Placing Order…✨" : "Submit Order"}
        </button>
      </div>
    </div>
  );
}