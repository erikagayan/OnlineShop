from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CustomPasswordValidator:
    def validate_password(self, password, user=None):
        try:
            # Проверка пароля с использованием валидаторов Django
            validate_password(password, user)
        except ValidationError as e:
            # Возвращаем ошибки валидации
            return list(e.messages)
        return None

