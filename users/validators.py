from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CustomPasswordValidator:
    def validate_password(self, password, user=None):
        try:
            validate_password(password, user)
        except ValidationError as e:
            return list(e.messages)
        return None
