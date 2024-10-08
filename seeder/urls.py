from rest_framework import routers
from .apis.views import AppliedSeederViewSet, RegisteredSeederViewSet

router = routers.DefaultRouter()

router.register('registered-seeders', RegisteredSeederViewSet, 'registered-seeders')
router.register('applied-seeders', AppliedSeederViewSet, 'applied-seeders')

urlpatterns = router.urls 
