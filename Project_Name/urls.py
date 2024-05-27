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
from common.rest_framework.api_versioning import OPTIONAL_VERSION
from common.rest_framework.drf_spectacular import (
    CustomSpectacularAPIView,
    CustomSpectacularRedocView,
    CustomSpectacularSwaggerView,
)

structure_app_patterns = [
    path('seeder/', include('seeder.urls')),
    path('logger/', include('logger.urls')),
    path('content-type/', include('content_type.urls')),
    path('translation/', include('translation.urls')),
    path('notification/', include('notification.urls')),
    path('backup/', include('backup.urls')),
    path('test-app/', include('test_app.urls')),
    path('users/', include('users.urls')),
    path('system-info/', include('system_info.urls')),
    path('feedback/', include('feedback.urls')),
]

custom_app_patterns = [

]

app_patterns = structure_app_patterns + custom_app_patterns

docs_patterns = [
    path('schema/', CustomSpectacularAPIView.as_view(), name='schema'),
    path('redoc/', CustomSpectacularRedocView.as_view(), name='redoc'),
    path('swagger/', CustomSpectacularSwaggerView.as_view(), name='swagger'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(rf'^api/{OPTIONAL_VERSION}', include(app_patterns)),
]

if settings.DEBUG:
    urlpatterns += [
        path('docs/', include(docs_patterns)),
        path('__debug__/', include('debug_toolbar.urls')),
    ] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
