import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
          headers: {
            Authorization: `Bearer YOUR_ACCESS_TOKEN`
          }
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
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container mt-5">
      <h2>User Profile</h2>
      {profileData && (
        <div className="profile-info">
          <p><strong>ID:</strong> {profileData.id}</p>
          <p><strong>Username:</strong> {profileData.username}</p>
          <p><strong>Email:</strong> {profileData.email}</p>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
