import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Typography, CircularProgress, Alert, Button, Link } from '@mui/material';

interface UserProfileData {
  id: number;
  username: string;
  email: string;
  telegram_chat_id: string | null; // Добавляем поле для Telegram
}

const UserProfile: React.FC = () => {
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/me/', {
          withCredentials: true, // Отправляем cookies для аутентификации
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

  // Функция для подключения Telegram
  const handleConnectTelegram = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/users/telegram-link/', {
        withCredentials: true, // Отправляем cookies
      });
      const { telegram_link } = response.data;
      // Перенаправляем пользователя на ссылку Telegram
      window.location.href = telegram_link;
    } catch (error) {
      setError('Ошибка при получении ссылки для Telegram.');
    }
  };

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
          <Typography variant="body1" sx={{ mt: 2 }}>
            <strong>Telegram:</strong>{' '}
            {profileData.telegram_chat_id ? (
              <>
                Подключен{' '}
                <Link href="https://t.me/online_shop_django_bot" target="_blank" rel="noopener">
                  Перейти к боту
                </Link>
              </>
            ) : (
              <>
                Не подключен{' '}
                <Button variant="contained" color="primary" onClick={handleConnectTelegram}>
                  Подключить Telegram
                </Button>
              </>
            )}
          </Typography>
        </div>
      )}
    </Container>
  );
};

export default UserProfile;