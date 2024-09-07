from django.urls import path
from user_account.views import EmailLoginAPIView, EmailSignupAPIView

urlpatterns = [
    path('users/login/', EmailLoginAPIView.as_view(), name='login'),
    path('users/signup/', EmailSignupAPIView.as_view(), name='signup'),
]
