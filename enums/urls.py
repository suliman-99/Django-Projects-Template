from rest_framework import routers
from .views import (
    OsTypeReadOnlyViewSet,
    RoleReadOnlyViewSet,
    GenderReadOnlyViewSet,
)


router = routers.DefaultRouter()

router.register('os-types', OsTypeReadOnlyViewSet, 'os-types')
router.register('role', RoleReadOnlyViewSet, 'role')
router.register('gender', GenderReadOnlyViewSet, 'gender')

urlpatterns = router.urls
