import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';

export interface CartItem {
  dish_id: number;
  dish_name: string;
  price: number;
  quantity: number;
  category: string;
}

interface CartContextType {
  cart: CartItem[];
  addToCart: (item: CartItem) => void;
  removeFromCart: (dish_id: number) => void;
  updateQuantity: (dish_id: number, quantity: number) => void;
  clearCart: () => void;
  getTotalPrice: () => number;
  getTotalItems: () => number;
}

const CartContext = createContext<CartContextType>({} as CartContextType);

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [cart, setCart] = useState<CartItem[]>(() => {
    // Load cart from localStorage on mount
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  const addToCart = (item: CartItem) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(cartItem => cartItem.dish_id === item.dish_id);
      
      if (existingItem) {
        // If item exists, update quantity
        return prevCart.map(cartItem =>
          cartItem.dish_id === item.dish_id
            ? { ...cartItem, quantity: cartItem.quantity + item.quantity }
            : cartItem
        );
      } else {
        // If item doesn't exist, add it to cart
        return [...prevCart, item];
      }
    });
  };

  const removeFromCart = (dish_id: number) => {
    setCart(prevCart => prevCart.filter(item => item.dish_id !== dish_id));
  };

  const updateQuantity = (dish_id: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(dish_id);
      return;
    }
    
    setCart(prevCart =>
      prevCart.map(item =>
        item.dish_id === dish_id ? { ...item, quantity } : item
      )
    );
  };

  const clearCart = () => {
    setCart([]);
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  const getTotalItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cart,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalPrice,
      getTotalItems
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
