from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    path('', admin.site.urls),
    url(r'^profesionales/', include('profesionales.urls')),
]
