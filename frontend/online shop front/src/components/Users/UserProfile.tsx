import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, CircularProgress, Alert } from '@mui/material';

interface UserProfileData {
  id: number;
  username: string;
  email: string;
}

const UserProfile: React.FC = () => {
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/me/', {
          // ВАЖНО: включаем отправку и приём cookie
          withCredentials: true
        });
        setProfileData(response.data);
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          setError('Ошибка при получении данных профиля.');
        } else {
          setError('Ошибка сети или сервера.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  if (isLoading) {
    return <Container><CircularProgress /></Container>;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4" component="h2" gutterBottom>
        User Profile
      </Typography>
      {profileData && (
        <div>
          <Typography variant="body1"><strong>ID:</strong> {profileData.id}</Typography>
          <Typography variant="body1"><strong>Username:</strong> {profileData.username}</Typography>
          <Typography variant="body1"><strong>Email:</strong> {profileData.email}</Typography>
        </div>
      )}
    </Container>
  );
};

export default UserProfile;
