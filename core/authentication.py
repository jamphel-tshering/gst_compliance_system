from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to authenticate using email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Try to find user by email
            user = User.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user
            User().set_password(password)
        return None