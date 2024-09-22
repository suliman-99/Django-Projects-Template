from rest_framework import routers
from .views import CustomFCMDeviceAuthorizedViewSet


router = routers.DefaultRouter()

router.register('devices', CustomFCMDeviceAuthorizedViewSet, 'devices')

urlpatterns = router.urls
