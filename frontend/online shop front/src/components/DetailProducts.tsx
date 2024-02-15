import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";


interface Product {
  id: number;
  title: string;
  price: number;
  description: string | null;
  manufacturer: string | null;
  category: number;
  inventory: number;
}

const DetailProduct: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/shop/products/${id}/`)
      .then((response) => response.json())
      .then((data) => {
        setProduct(data);
      })
      .catch((error) => {
        console.error("Error fetching product details:", error);
      });
  }, [id]);

  if (!product) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Detailed product information</h2>
      <h3>{product.title}</h3>
      <p>Price: {product.price}$</p>
      <p>Description: {product.description || "Нет описания"}</p>
      <p>Manufacturer: {product.manufacturer || "Не указан"}</p>
      <p>Category: {product.category}</p>
      <p>Inventory: {product.inventory}</p>
    </div>
  );
};

export default DetailProduct;
