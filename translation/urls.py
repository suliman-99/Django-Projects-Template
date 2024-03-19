from rest_framework import routers
from translation.views import LanguageViewSet


router = routers.DefaultRouter()

router.register('languages', LanguageViewSet, 'languages')

urlpatterns = router.urls
