import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';

export interface Favorite {
  dish_id: number;
  dish_name: string;
  price: number;
  category: string;
  calories: number;
  ingredients: number[];
}

interface FavoritesContextType {
  favorites: Favorite[];
  addToFavorites: (item: Favorite) => void;
  removeFromFavorites: (dish_id: number) => void;
  isFavorite: (dish_id: number) => boolean;
  toggleFavorite: (item: Favorite) => void;
  getFavoriteCount: () => number;
}

const FavoritesContext = createContext<FavoritesContextType>({} as FavoritesContextType);

export const FavoritesProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [favorites, setFavorites] = useState<Favorite[]>(() => {
    // Load favorites from localStorage on mount
    const savedFavorites = localStorage.getItem('favorites');
    return savedFavorites ? JSON.parse(savedFavorites) : [];
  });

  // Save favorites to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('favorites', JSON.stringify(favorites));
  }, [favorites]);

  const addToFavorites = (item: Favorite) => {
    setFavorites(prevFavorites => {
      const existing = prevFavorites.find(fav => fav.dish_id === item.dish_id);
      if (!existing) {
        return [...prevFavorites, item];
      }
      return prevFavorites;
    });
  };

  const removeFromFavorites = (dish_id: number) => {
    setFavorites(prevFavorites => prevFavorites.filter(fav => fav.dish_id !== dish_id));
  };

  const isFavorite = (dish_id: number) => {
    return favorites.some(fav => fav.dish_id === dish_id);
  };

  const toggleFavorite = (item: Favorite) => {
    if (isFavorite(item.dish_id)) {
      removeFromFavorites(item.dish_id);
    } else {
      addToFavorites(item);
    }
  };

  const getFavoriteCount = () => {
    return favorites.length;
  };

  return (
    <FavoritesContext.Provider value={{
      favorites,
      addToFavorites,
      removeFromFavorites,
      isFavorite,
      toggleFavorite,
      getFavoriteCount
    }}>
      {children}
    </FavoritesContext.Provider>
  );
};

export const useFavorites = () => useContext(FavoritesContext);
