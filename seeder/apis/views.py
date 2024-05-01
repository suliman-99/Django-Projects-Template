from django_seeding.apis.views import RegisteredSeederViewSet, AppliedSeederViewSet 
from common.rest_framework.permissions import IsSuperuser


class RegisteredSeederViewSet(RegisteredSeederViewSet):
    permission_classes = (IsSuperuser, )


class AppliedSeederViewSet(AppliedSeederViewSet):
    permission_classes = (IsSuperuser, )
