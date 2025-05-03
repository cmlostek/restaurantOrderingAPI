import React from "react";

const Home: React.FC = () => {
  return (
    <section className="text-center py-20 bg-red-50">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-5xl font-bold text-red-700 mb-4">Welcome to Hungry Cow 🐄</h1>
        <p className="text-lg text-gray-700 mb-8">
          Moo-licious meals made fresh for you! Dive into our delicious menu or place an order online.
        </p>
        <a
          href="/menu"
          className="inline-block px-6 py-3 bg-red-600 text-white rounded-lg shadow hover:bg-red-700 transition"
        >
          View Menu
        </a>
      </div>
    </section>
  );
};

export default Home;
