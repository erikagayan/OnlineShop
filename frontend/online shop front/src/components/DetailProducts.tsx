import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Typography, CircularProgress, Card, CardContent } from "@mui/material";
import axios from "axios"; // Импорт axios

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
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get<Product>(`http://localhost:8000/api/shop/products/${id}/`, {
          withCredentials: true,
        });
        setProduct(response.data);
      } catch (error) {
        console.error("Error fetching product details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        <CircularProgress />
      </div>
    );
  }

  if (!product) {
    return (
      <Typography variant="h6" color="text.secondary">
        Product not found.
      </Typography>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div">
          Detailed product information
        </Typography>
        <Typography variant="h6" component="div">
          {product.title}
        </Typography>
        <Typography color="text.secondary">Price: {product.price}$</Typography>
        <Typography variant="body2">Description: {product.description || "No description available"}</Typography>
        <Typography variant="body2">Manufacturer: {product.manufacturer || "Not specified"}</Typography>
        <Typography variant="body2">Category: {product.category}</Typography>
        <Typography variant="body2">Inventory: {product.inventory}</Typography>
      </CardContent>
    </Card>
  );
};

export default DetailProduct;
