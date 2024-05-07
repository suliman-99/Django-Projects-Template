"""
URL configuration for Project_Name project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from common.rest_framework.drf_spectacular import (
    CustomSpectacularAPIView,
    CustomSpectacularRedocView,
    CustomSpectacularSwaggerView,
)

app_patterns = [
    path('seeder/', include('seeder.urls')),
    path('logger/', include('logger.urls')),
    path('content-type/', include('content_type.urls')),
    path('users/', include('users.urls')),
    path('translation/', include('translation.urls')),
    path('notification/', include('notification.urls')),
    path('backup/', include('backup.urls')),
    path('test-app/', include('test_app.urls')),
]


docs_patterns = [
    path('schema/', CustomSpectacularAPIView.as_view(), name='schema'),
    path('redoc/', CustomSpectacularRedocView.as_view(), name='redoc'),
    path('swagger/', CustomSpectacularSwaggerView.as_view(), name='swagger'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/(v(?P<version>\d+)/)?', include(app_patterns)),
]


if settings.DEBUG:
    urlpatterns += [
        path('docs/', include(docs_patterns)),
        path('__debug__/', include('debug_toolbar.urls')),
    ] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
