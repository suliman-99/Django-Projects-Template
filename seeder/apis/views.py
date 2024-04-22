from django_seeding.apis.views import RegisteredSeederViewSet, AppliedSeederViewSet 
from common.permissions import IsSuperuser


class RegisteredSeederViewSet(RegisteredSeederViewSet):
    permission_classes = (IsSuperuser, )


class AppliedSeederViewSet(AppliedSeederViewSet):
    permission_classes = (IsSuperuser, )
