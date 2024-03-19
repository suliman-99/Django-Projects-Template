from django.urls import path
from rest_framework import routers
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from notification.views import NotificationViewSet, MyNotificationViewSet


router = routers.DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet, 'devices')
router.register('notifications', NotificationViewSet, 'notifications')
router.register('my-notifications', MyNotificationViewSet, 'my-notifications')

urlpatterns = router.urls
