from rest_framework.routers import DefaultRouter
from content_type.views import ContentTypeViewSet


router = DefaultRouter()

router.register('content-types', ContentTypeViewSet, 'content-types')

urlpatterns = router.urls
