from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"[v0] Backend authenticate called with username: {username}")
        try:
            # username parameter actually contains phone_number
            user = CustomUser.objects.get(phone_number=username)
            print(f"[v0] Found user: {user}")
            print(f"[v0] User password hash: {user.password}")
            password_valid = user.check_password(password)
            print(f"[v0] Password check result: {password_valid}")
            if password_valid:
                return user
        except CustomUser.DoesNotExist:
            print(f"[v0] User with phone {username} does not exist")
            return None
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
