from rest_framework import throttling 


class BaseAuthThrottle(throttling.SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.rate,
            'ident': self.get_ident(request)
        }


class SecondlyAuthThrottle(BaseAuthThrottle):
    rate = '2/s'


class MinutelyAuthThrottle(BaseAuthThrottle):
    rate = '20/m'


class HourlyAuthThrottle(BaseAuthThrottle):
    rate = '40/h'


class DailyAuthThrottle(BaseAuthThrottle):
    rate = '50/d'
