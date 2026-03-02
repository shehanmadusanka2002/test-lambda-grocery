"use client";
import { useState, useEffect } from "react";

interface Product {
  id?: number;
  name: string;
  price: number;
  description: string;
}

export default function GroceryShop() {
  const [products, setProducts] = useState<Product[]>([]);
  const [formData, setFormData] = useState<Product>({ name: "", price: 0, description: "" });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://zan5ixaehox3ipzynj4mjuupzu0puqrm.lambda-url.us-east-1.on.aws"; //

  // 1. Fetch Products (Read)
  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_URL}/products`);
      const data = await res.json();
      setProducts(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchProducts(); }, []);

  // 2. Add or Update Product (Create/Update)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const method = editingId ? "PUT" : "POST";
    const url = editingId ? `${API_URL}/products/${editingId}` : `${API_URL}/products`;

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    setFormData({ name: "", price: 0, description: "" });
    setEditingId(null);
    fetchProducts();
  };

  // 3. Delete Product (Delete)
  const handleDelete = async (id: number) => {
    if (confirm("Are you sure?")) {
      await fetch(`${API_URL}/products/${id}`, { method: "DELETE" });
      fetchProducts();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">🛒 Grocery Shop Admin</h1>

        {/* Product Form */}
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md mb-8 grid grid-cols-1 md:grid-cols-3 gap-4 border border-gray-200">
          <input type="text" placeholder="Product Name" className="p-2 border rounded text-gray-700 focus:ring-2 focus:ring-blue-500 outline-none" 
            value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required />
          <input type="number" placeholder="Price" className="p-2 border rounded text-gray-700 focus:ring-2 focus:ring-blue-500 outline-none" 
            value={formData.price} onChange={(e) => setFormData({...formData, price: Number(e.target.value)})} required />
          <input type="text" placeholder="Description" className="p-2 border rounded text-gray-700 focus:ring-2 focus:ring-blue-500 outline-none" 
            value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} />
          <button type="submit" className={`md:col-span-3 py-2 rounded font-semibold transition ${editingId ? "bg-yellow-500 hover:bg-yellow-600" : "bg-green-600 hover:bg-green-700"} text-white`}>
            {editingId ? "Update Product" : "Add Product"}
          </button>
        </form>

        {/* Product List */}
        {loading ? <p className="text-center text-gray-500">Loading inventory...</p> : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {products.map((p) => (
              <div key={p.id} className="bg-white p-5 rounded-lg shadow border border-gray-100 flex justify-between items-center hover:shadow-lg transition">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{p.name}</h3>
                  <p className="text-blue-600 font-semibold">Rs. {p.price}.00</p>
                  <p className="text-gray-500 text-sm">{p.description}</p>
                </div>
                <div className="flex flex-col gap-2">
                  <button onClick={() => {setEditingId(p.id!); setFormData(p);}} className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded">Edit</button>
                  <button onClick={() => handleDelete(p.id!)} className="text-sm bg-red-50 hover:bg-red-100 text-red-600 py-1 px-3 rounded">Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}