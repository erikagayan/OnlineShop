import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AppBar from '@mui/material/AppBar';  // navbar
import Toolbar from '@mui/material/Toolbar';  // container for placing items inside the AppBar
import Typography from '@mui/material/Typography';  //component for outputting text with different styles.
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';

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
      <AppBar
        position="static"
        sx={{
          backgroundColor: "#e0dfde",
          color: "#000",
        }}
      >
        <Toolbar
          sx={{
            minHeight: 0,
            padding: 0
          }}
        >

          <Typography variant="h6" sx={{ ml: 2, mr: 2 }}>
            Online Shop
          </Typography>


          <Box
            sx={{
              flexGrow: 1,                  
              display: "flex",
              justifyContent: "center",     
              gap: 2                         
            }}
          >
            <Button color="inherit" component={Link} to="/shop/categories">
              Categories
            </Button>
            <Button color="inherit" component={Link} to="/shop/products">
              Products
            </Button>
            <Button color="inherit" component={Link} to="/shop/carts">
              Cart
            </Button>
          </Box>

          <Box sx={{ mr: 2 }}>
            <Button color="inherit" component={Link} to="/user/login">
              Login
            </Button>
            <Button color="inherit" component={Link} to="/user/register">
              Registration
            </Button>
            <Button color="inherit" component={Link} to="/user/profile">
              Profile
            </Button>
          </Box>
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
    </Router>
  );
};


export default App;
