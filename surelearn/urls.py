"""
URL configuration for surelearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import FileResponse, HttpResponse
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.decorators.cache import cache_page
from django.conf import settings

from academy.sitemaps import sitemaps


def favicon_ico(request):
    response = FileResponse(open(settings.BASE_DIR / "static" / "assets" / "favicon.ico", "rb"), content_type="image/x-icon")
    response["Cache-Control"] = "public, max-age=86400"
    return response


def robots_txt(request):
    body = "\n".join([
        "User-agent: *",
        "Disallow: /admin/",
        "Allow: /",
        "",
        f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml",
        "",
    ])
    return HttpResponse(body, content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('favicon.ico', favicon_ico, name='favicon'),
    path('sitemap.xml', cache_page(60 * 60)(sitemap), {'sitemaps': sitemaps}, name='sitemap'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', include('academy.urls')),
]
