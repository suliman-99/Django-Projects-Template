from rest_framework import routers
from .views import (
    OsTypeReadOnlyViewSet,
    RoleReadOnlyViewSet,
    GenderReadOnlyViewSet,
    FCMTypeReadOnlyViewSet,
)


router = routers.DefaultRouter()

router.register('os-types', OsTypeReadOnlyViewSet, 'os-types')
router.register('role', RoleReadOnlyViewSet, 'role')
router.register('gender', GenderReadOnlyViewSet, 'gender')
router.register('fcm-type', FCMTypeReadOnlyViewSet, 'fcm-type')

urlpatterns = router.urls
