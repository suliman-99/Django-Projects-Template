from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()

# --------------------------------------------- Django Admin Login Backends ---------------------------------------------

class AdminEmailBackend(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass


class AdminPhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass
        