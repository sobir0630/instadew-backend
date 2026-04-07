from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views.users_W import (
    UserViewSet, UserLoginViewSet, 
    check_password_view,
    change_password_view
)
from users.views.msc import RegisterUserViews

router = DefaultRouter()
router.register(r'register', UserViewSet, basename='user-register')
router.register(r'login', UserLoginViewSet, basename='user-login')
router.register(r'user-view', RegisterUserViews, basename="register-views")


urlpatterns = [
    path('', include(router.urls)),
    path('check-password/', check_password_view, name="check-password"),
    path('change-password/', change_password_view, name="change-password"),
]