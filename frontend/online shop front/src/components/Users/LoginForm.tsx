import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [tokens, setTokens] = useState<{ access: string, refresh: string } | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/users/login/",
        formData
      );
      if (response.data.access && response.data.refresh) {
        setTokens({ access: response.data.access, refresh: response.data.refresh });
      } else {
        setErrorMessage("Ошибка: токены не получены.");
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setErrorMessage(
          "Ошибка при попытке входа. Проверьте введенные данные."
        );
      } else {
        setErrorMessage("Ошибка сети или сервера.");
      }
    }
  };

  return (
    <div className="container mt-5">
      <h2>Log in</h2>
      {errorMessage && (
        <div className="alert alert-danger" role="alert">
          {errorMessage}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
      {tokens && (
        <div className="alert alert-success mt-3" role="alert" style={{ wordWrap: "break-word" }}>
          <p style={{ color: "black" }}>Access Token: <b>{tokens.access}</b></p>
          <p style={{ color: "black" }}>Refresh Token: <b>{tokens.refresh}</b></p>
        </div>
      )}
      <div className="mt-3">
        No account? <Link to="/user/register">Sign up</Link>
      </div>
    </div>
  );
};

export default LoginForm;
