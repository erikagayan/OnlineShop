import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link as RouterLink } from "react-router-dom";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';

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
        setErrorMessage("Error: Tokens not received.");
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setErrorMessage(
          "Login attempt failed. Please check your credentials."
        );
      } else {
        setErrorMessage("Network or server error.");
      }
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={6} sx={{ mt: 8, p: 3 }}>
        <Typography component="h1" variant="h5">
          Log in
        </Typography>
        {errorMessage && (
          <Alert severity="error">{errorMessage}</Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
            value={formData.email}
            onChange={handleChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Login
          </Button>
        </Box>
        {tokens && (
          <Box sx={{ wordBreak: "break-all", backgroundColor: 'success.light', p: 2, mt: 2 }}>
            <Typography variant="body1" component="p">
              Access Token: <Typography component="span" color="text.primary" variant="body1" fontWeight="fontWeightBold">{tokens.access}</Typography>
            </Typography>
            <Typography variant="body1" component="p">
              Refresh Token: <Typography component="span" color="text.primary" variant="body1" fontWeight="fontWeightBold">{tokens.refresh}</Typography>
            </Typography>
          </Box>
        )}
        <Typography variant="body2" color="textSecondary" align="center" sx={{ mt: 3 }}>
          No account?{' '}
          <Link component={RouterLink} to="/user/register" variant="body2">
            Sign up
          </Link>
        </Typography>
      </Paper>
    </Container>
  );
};

export default LoginForm;
