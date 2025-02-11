import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { Typography, Button, List, ListItem, ListItemText, Link } from "@mui/material";
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
    axios
      .get<Product[]>("http://localhost:8000/api/shop/products/", {
        withCredentials: true,
      })
      .then((response) => {
        setProducts(response.data);
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
      <Typography variant="h4" gutterBottom>
        List of Products
      </Typography>
      <Button variant="contained" onClick={toggleCreateForm}>
        Create Product
      </Button>
      {showCreateForm && <CreateProductForm />}
      <List>
        {products.map((product) => (
          <ListItem key={product.id}>
            <ListItemText
              primary={<Link component={RouterLink} to={`/shop/products/${product.id}`}>{product.title}</Link>}
              secondary={
                <>
                  <Typography component="span" variant="body2">Price: {product.price}$</Typography>
                  <br />
                  <Typography component="span" variant="body2">Category: {product.category}</Typography>
                </>
              }
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default ProductsList;
