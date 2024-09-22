from rest_framework_simplejwt.views import TokenObtainPairView
from common.rest_framework.throttling import (
    SecondlyAuthThrottle,
    MinutelyAuthThrottle,
    HourlyAuthThrottle,
    DailyAuthThrottle,
)


class BaseAuthView(TokenObtainPairView):
    throttle_classes  = (
        SecondlyAuthThrottle,
        MinutelyAuthThrottle,
        HourlyAuthThrottle,
        DailyAuthThrottle,
    )
