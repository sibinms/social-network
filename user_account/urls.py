from django.urls import path
from user_account.views import EmailLoginAPIView, EmailSignupAPIView, SearchUsersView

urlpatterns = [
    path('users/login/', EmailLoginAPIView.as_view(), name='user-login'),
    path('users/signup/', EmailSignupAPIView.as_view(), name='user-signup'),
    path('users/search/', SearchUsersView.as_view(), name='user-search'),
]
