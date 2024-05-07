from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


class BaseDocsView:
    authentication_classes = []


class CustomSpectacularAPIView(BaseDocsView, SpectacularAPIView):
    pass


class CustomSpectacularSwaggerView(BaseDocsView, SpectacularSwaggerView):
    pass


class CustomSpectacularRedocView(BaseDocsView, SpectacularRedocView):
    pass
