import React, { useEffect, useState } from "react";
import axios from "axios";

interface CartItem {
  id: number;
  item_title: string;
  quantity: number;
  total_cost: number;
  created_at: number;
  updated_at: number;
  user: string;
}

interface Product {
  id: number;
  title: string;
  price: number;
}

const Cart = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<number | undefined>(undefined);
  const [quantity, setQuantity] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchCartItems = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/shop/carts/");
        setCartItems(response.data);
      } catch (error) {
        console.error("Ошибка при получении данных корзины:", error);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/shop/products/");
        setProducts(response.data);
      } catch (error) {
        console.error("Ошибка при получении списка продуктов:", error);
      }
    };

    fetchCartItems();
    fetchProducts().then(() => setIsLoading(false));
  }, []);

  const handleAddToCart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedProductId === undefined) {
      alert("Please select a product");
      return;
    }

    try {
      await axios.post("http://localhost:8000/api/shop/carts/", {
        items: selectedProductId,
        quantity,
      });
      alert("Product added to cart");
    } catch (error) {
      console.error("Ошибка при добавлении товара в корзину:", error);
    }
  };

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Your cart</h2>
      <ul>
        {cartItems.map((item) => (
          <li key={item.id}>
            <ul>
              <li><b>{item.item_title}</b></li>
              <li><b>Count:</b> {item.quantity}</li>
              <li><b>Total cost:</b> {item.total_cost}$</li>
              <li><b>Created at:</b> {new Date(item.created_at).toLocaleString()}</li>
              <li><b>Updated at:</b> {new Date(item.updated_at).toLocaleString()}</li>
              <li><b>User:</b> {item.user}</li>
            </ul>
          </li>
        ))}
      </ul>

      <h3>Add product to cart</h3>
      <form onSubmit={handleAddToCart}>
        <div>
          <label>Product:</label>
          <select value={selectedProductId} onChange={e => setSelectedProductId(Number(e.target.value))}>
            <option value="">Select a product</option>
            {products.map(product => (
              <option key={product.id} value={product.id}>{product.title}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Quantity:</label>
          <input type="number" value={quantity} onChange={e => setQuantity(Number(e.target.value))} min="1" />
        </div>
        <button type="submit">Add to Cart</button>
      </form>
    </div>
  );
};

export default Cart;
