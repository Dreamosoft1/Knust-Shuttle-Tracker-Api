from django.urls import path
from .views import *
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [
    path('get-user-token/', get_user_token, name="get_token"),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('update/<id>/', UserUpdateView.as_view(), name='user-update'),
    path('password/reset/', reset_password_request_token, name='password_reset'),
    path('passwordreset/confirm/', reset_password_confirm, name='password_reset_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
]