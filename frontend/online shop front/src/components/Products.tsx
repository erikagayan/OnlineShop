import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import CreateProductForm from "./CreateProductForm";

interface Product {
  id: number;
  title: string;
  price: number;
  description: string | null;
  manufacturer: string | null;
  category: number;
}

const ProductsList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/shop/products/")
      .then((response) => response.json())
      .then((data) => {
        setProducts(data);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  }, []);

  const toggleCreateForm = () => {
    setShowCreateForm(!showCreateForm);
  };

  return (
    <div>
      <h2>List of products</h2>
      <button className="btn btn-primary" onClick={toggleCreateForm}>Create Product</button>
      {showCreateForm && <CreateProductForm />}
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            <Link to={`/shop/products/${product.id}`}>{product.title}</Link>
            <ul>
              <li>Price: {product.price}$ </li>
              <li>Category: {product.category}</li>
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductsList;
