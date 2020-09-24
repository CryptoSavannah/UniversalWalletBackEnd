from django.urls import path, include
from .views.user_view import LoginView, UserListView, UserSpecificView

urlpatterns = [
    path('authenticate/', LoginView.as_view(), name="auth-login"),
    path('users', UserListView.as_view(), name="user-create"),
    path('users/<int:pk>', UserSpecificView.as_view(), name="user-specific")
]