# from django.contrib.auth.backends import ModelBackend
# from .models import User

# class EmailOrPhoneBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = None
#             if '@' in username:
#                 user = User.objects.get(email=username)
#             else:
#                 user = User.objects.get(phone_number=username)
#         except User.DoesNotExist:
#             return None

#         if user and user.check_password(password):
#             return user
#         return None
