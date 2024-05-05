from rest_framework import throttling 


class SecondlyAuthThrottle(throttling.UserRateThrottle):
    scope = 'secondly_auth'


class MinutelyAuthThrottle(throttling.UserRateThrottle):
    scope = 'minutely_auth'


class HourlyAuthThrottle(throttling.UserRateThrottle):
    scope = 'hourly_auth'


class DailyAuthThrottle(throttling.UserRateThrottle):
    scope = 'daily_auth'
