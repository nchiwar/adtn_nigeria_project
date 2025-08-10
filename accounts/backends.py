# Temporarily disabled Firebase backend
# import firebase_admin
# from firebase_admin import credentials, auth
# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser
# import logging
#
# logger = logging.getLogger(__name__)
#
# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('serviceAccountKey.json')  # Path to your JSON file
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred)
#
# class FirebaseBackend(ModelBackend):
#     def authenticate(self, request, id_token=None, **kwargs):
#         try:
#             decoded_token = auth.verify_id_token(id_token)
#             uid = decoded_token['uid']
#             
#             try:
#                 user = CustomUser.objects.get(username=uid)
#             except CustomUser.DoesNotExist:
#                 email = decoded_token.get('email', f'firebase_{uid}@example.com')
#                 user = CustomUser.objects.create_user(
#                     username=uid,
#                     email=email,
#                     password='firebase_auth',  # Dummy password
#                     is_approved=True,
#                 )
#                 logger.info(f"New user created with UID: {uid}")
#             
#             return user
#         except Exception as e:
#             logger.error(f"Firebase authentication error: {str(e)}")
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return CustomUser.objects.get(pk=user_id)
#         except CustomUser.DoesNotExist:
#             return None