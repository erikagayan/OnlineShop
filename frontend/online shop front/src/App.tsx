import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';

// Ваши импорты компонентов остаются без изменений
import RegistrationForm from "./components/Users/RegistrationForm";
import LoginForm from "./components/Users/LoginForm";
import UserProfile from "./components/Users/UserProfile";
import Categories from "./components/Categories";
import ProductsList from "./components/Products";
import DetailProduct from "./components/DetailProducts";
import Cart from "./components/Cart";

const App: React.FC = () => {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Online Shop
            </Typography>
            <Button color="inherit" component={Link} to="/user/login">Login</Button>
            <Button color="inherit" component={Link} to="/user/register">Registration</Button>
            <Button color="inherit" component={Link} to="/user/profile">Profile</Button>
            <Button color="inherit" component={Link} to="/shop/categories">Categories</Button>
            <Button color="inherit" component={Link} to="/shop/products">Products</Button>
            <Button color="inherit" component={Link} to="/shop/carts">Cart</Button>
          </Toolbar>
        </AppBar>
        <Container>
          <Routes>
            <Route path="/user/login" element={<LoginForm />} />
            <Route path="/user/register" element={<RegistrationForm />} />
            <Route path="/user/profile" element={<UserProfile />} />
            <Route path="/shop/categories" element={<Categories />} />
            <Route path="/shop/products" element={<ProductsList />} />
            <Route path="/shop/products/:id" element={<DetailProduct />} />
            <Route path="/shop/carts" element={<Cart />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
};

export default App;
