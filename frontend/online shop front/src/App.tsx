import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
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
      <div className="App container mt-5">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <div className="container-fluid">
            <a className="navbar-brand" href="#">
              Online Shop
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link to="/user/login" className="nav-link">
                    Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/user/register" className="nav-link">
                    Registration
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/user/profile" className="nav-link">
                    Profile
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/shop/categories" className="nav-link">
                    Categories
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/shop/products" className="nav-link">
                    Products
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/shop/carts" className="nav-link">
                    Cart
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        <Routes>
          <Route path="/user/login" element={<LoginForm />} />
          <Route path="/user/register" element={<RegistrationForm />} />
          <Route path="/user/profile" element={<UserProfile />} />
          <Route path="/shop/categories" element={<Categories />} />
          <Route path="/shop/products" element={<ProductsList />} />
          <Route path="/shop/products/:id" element={<DetailProduct />} />
          <Route path="/shop/carts" element={<Cart />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
