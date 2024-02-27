import React, { useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { Container, TextField, Button, Typography, Link, Alert } from '@mui/material';

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const RegistrationForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setErrorMessage('Пароли не совпадают.');
      return;
    }

    setErrorMessage('');
    try {
      const response = await axios.post('http://localhost:8000/api/users/register/', {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });
      if (response.status === 201) {
        navigate('/user/login');
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const errors: Record<string, any> = error.response.data;
        const errorMessages = Object.entries(errors)
          .map(([key, value]) => `${key}: ${value.join(', ')}`)
          .join('\n');
        setErrorMessage(`Ошибка при регистрации: ${errorMessages}`);
      } else {
        setErrorMessage('Ошибка при регистрации. Попробуйте снова.');
      }
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        Registration
      </Typography>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <form onSubmit={handleSubmit}>
        <TextField
          label="User Name"
          variant="outlined"
          fullWidth
          name="username"
          value={formData.username}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          label="Email"
          variant="outlined"
          fullWidth
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          label="Password"
          variant="outlined"
          fullWidth
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          margin="normal"
          required
        />
        <TextField
          label="Confirm Password"
          variant="outlined"
          fullWidth
          name="confirmPassword"
          type="password"
          value={formData.confirmPassword}
          onChange={handleChange}
          margin="normal"
          required
        />
        <Button type="submit" variant="contained" sx={{ mt: 3, mb: 2 }}>
          Sign Up
        </Button>
        <Typography variant="body2">
          Already registered?{' '}
          <Link component={RouterLink} to="/user/login">
            Sign in
          </Link>
        </Typography>
      </form>
    </Container>
  );
};

export default RegistrationForm;
