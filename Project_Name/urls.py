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
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


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
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(app_patterns)),
]


if settings.DEBUG:
    urlpatterns += [
        path('docs/', include(docs_patterns)),
        path('__debug__/', include('debug_toolbar.urls')),
    ] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
