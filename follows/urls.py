from django.urls import path, include
from rest_framework.routers import DefaultRouter
from follows.views import FolowViews


router = DefaultRouter()
router.register(r'follows', FolowViews, basename="follows")

urlpatterns = [
    path('', include(router.urls)),
]