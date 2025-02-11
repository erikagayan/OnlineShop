import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Typography, TextField, Button, Select, MenuItem, FormControl, InputLabel, CircularProgress, List, ListItem, ListItemText } from "@mui/material";

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
        const response = await axios.get("http://localhost:8000/api/shop/carts/", {
          withCredentials: true, // Отправка cookies
        });
        setCartItems(response.data);
      } catch (error) {
        console.error("Ошибка при получении данных корзины:", error);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/shop/products/", {
          withCredentials: true, // Отправка cookies
        });
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
      await axios.post(
        "http://localhost:8000/api/shop/carts/",
        {
          items: selectedProductId,
          quantity,
        },
        {
          withCredentials: true,
        }
      );
      alert("Product added to cart");

      // Обновляем список корзины после добавления
      const response = await axios.get("http://localhost:8000/api/shop/carts/", {
        withCredentials: true,
      });
      setCartItems(response.data);
    } catch (error) {
      console.error("Ошибка при добавлении товара в корзину:", error);
    }
  };

  if (isLoading) return <Container><CircularProgress /></Container>;

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        Your shopping cart
      </Typography>
      <List>
        {cartItems.map((item) => (
          <ListItem key={item.id} sx={{ mb: 2 }}>
            <ListItemText
              primary={item.item_title}
              secondary={`Quantity: ${item.quantity}, Total cost: ${item.total_cost}$, Created at: ${new Date(item.created_at).toLocaleString()}, Updated at: ${new Date(item.updated_at).toLocaleString()}, User: ${item.user}`}
            />
          </ListItem>
        ))}
      </List>

      <Typography variant="h5" gutterBottom>
        Add product to cart
      </Typography>
      <form onSubmit={handleAddToCart}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Product</InputLabel>
          <Select
            value={selectedProductId}
            onChange={e => setSelectedProductId(Number(e.target.value))}
            displayEmpty
          >
            <MenuItem value="">
              <em>Choose product</em>
            </MenuItem>
            {products.map(product => (
              <MenuItem key={product.id} value={product.id}>{product.title}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <TextField
            label="Quantity"
            type="number"
            value={quantity}
            onChange={e => setQuantity(Number(e.target.value))}
            InputProps={{ inputProps: { min: 1 } }}
          />
        </FormControl>
        <Button type="submit" variant="contained" color="primary">
          Add to cart
        </Button>
      </form>
    </Container>
  );
};

export default Cart;
