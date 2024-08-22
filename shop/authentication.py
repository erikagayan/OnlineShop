import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MicroserviceUser:
    def __init__(self, user_data):
        self.user_data = user_data
        self.is_authenticated = True

    def __getattr__(self, item):
        return self.user_data.get(item, None)

    def __str__(self):
        return self.user_data.get('email', 'Unknown')


class MicroserviceJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Попытка получить токен из сессии
        token = request.session.get('auth_token')
        if not token:
            # Если токен не найден в сессии, пробуем получить его из заголовков запроса
            token = request.headers.get('Authorization')
            if not token:
                return None

            # Удаляем префикс "Bearer ", если он есть
            token = token.split(' ')[-1]

            try:
                # Отправляем запрос к микросервису для аутентификации
                response = requests.get('http://localhost:8000/api/users/me/',
                                        headers={'Authorization': f'Bearer {token}'})
                response.raise_for_status()
                user_data = response.json()

                # Сохраняем токен в сессии
                request.session['auth_token'] = token
                request.session['user_data'] = user_data

            except requests.exceptions.RequestException:
                raise AuthenticationFailed('Failed to authenticate with microservice')

        else:
            # Если токен есть в сессии, используем сохраненные данные пользователя
            user_data = request.session.get('user_data')

        return (MicroserviceUser(user_data), None)
