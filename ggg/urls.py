from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import HomeView


urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),
    url(
        '',
        HomeView.as_view(),
        name="admin.home",
    ),
    path('admin/', admin.site.urls),
    path('accounts/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^profesionales/', include('profesionales.urls')),
    url(r'^turnos/', include('calendario.urls')),
    url(r'^obras-sociales/', include('obras_sociales.urls')),
]
