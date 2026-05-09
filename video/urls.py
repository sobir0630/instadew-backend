from rest_framework.routers import DefaultRouter
from video.views.views import VideoViewSet
from video.views.reals_W import RealsVideoViewSet


router = DefaultRouter()
router.register(r"video", VideoViewSet, basename="video")
router.register(r"reals-videos", RealsVideoViewSet, basename="reals-videos")
urlpatterns = router.urls