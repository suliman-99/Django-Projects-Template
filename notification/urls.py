from rest_framework import routers
from .views import NotificationViewSet, MyNotificationViewSet, NotificationTemplateViewSet


router = routers.DefaultRouter()

router.register('notifications', NotificationViewSet, 'notifications')
router.register('my-notifications', MyNotificationViewSet, 'my-notifications')
router.register('notification-templates', NotificationTemplateViewSet, 'notification-templates')

urlpatterns = router.urls
