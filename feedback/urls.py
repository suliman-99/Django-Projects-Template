from rest_framework import routers
from .views import FeedbackViewSet, AdminFeedbackViewSet

router = routers.DefaultRouter()

router.register('feedbacks', FeedbackViewSet, 'feedbacks')
router.register('admin-feedbacks', AdminFeedbackViewSet, 'admin-feedbacks')

urlpatterns = router.urls
