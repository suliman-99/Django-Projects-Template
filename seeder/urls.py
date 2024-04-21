from rest_framework import routers
from seeder.views import AppliedSeederViewSet

router = routers.DefaultRouter()

router.register('applied-seeders', AppliedSeederViewSet, 'applied-seeders')

urlpatterns = router.urls 
