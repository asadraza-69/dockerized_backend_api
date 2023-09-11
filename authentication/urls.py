from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)
from .views import *


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', UserRegisterView.as_view(), name='user_register_view'),
    path('signin/', UserLoginView.as_view(), name='login_view'),
    path('signout/', LogoutAPIView.as_view(), name='logout_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
