from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authentication via JWT stored in httpOnly cookie.
    """

    def authenticate(self, request):
        # Trying to get a token from a cookie
        token = request.COOKIES.get('access')

        if token is not None:
            # Verify and validate the token (same logic as in the base class)
            validated_token = self.get_validated_token(token)
            return (self.get_user(validated_token), validated_token)

        # If no cookie is present, fallback to standard way via header (optional)
        return super().authenticate(request)
