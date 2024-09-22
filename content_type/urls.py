from rest_framework.routers import DefaultRouter
from .views import ContentTypeViewSet


router = DefaultRouter()

router.register('content-types', ContentTypeViewSet, 'content-types')

urlpatterns = router.urls
