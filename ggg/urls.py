from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import HomeView


urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^profesionales/', include('profesionales.urls')),
    url(r'^turnos/', include('calendario.urls')),
    url(r'^obras-sociales/', include('obras_sociales.urls')),
    url(r'^centros-de-salud/', include('centros_de_salud.urls')),
    url(r'^recupero/', include('recupero.urls')),
    url(
        r'^ciudadano/',
        HomeView.as_view(),
        name="admin.ciudadano-home",
    ),
    url(
        r'^$',
        HomeView.as_view(),
        name="admin.home",
    ),
]
