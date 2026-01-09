from django.urls import path
from .views import api_home
from .views import register_user, verify_code
from .views import forgot_password, reset_password

urlpatterns = [
    path('register/', register_user, name='register'),
    path('verify/', verify_code, name='verify'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
]

