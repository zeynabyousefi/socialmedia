from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name="profile"),
    path('follow/<int:user_id>/', UserFollow.as_view(), name="follow"),
    path('unfollow/<int:user_id>/', UserUnfollow.as_view(), name="unfollow"),
]
